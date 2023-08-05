
/* Chrysalide - Outil d'analyse de fichiers binaires
 * storage.c - conservation hors mémoire d'objets choisis
 *
 * Copyright (C) 2020 Cyrille Bagard
 *
 *  This file is part of Chrysalide.
 *
 *  Chrysalide is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Chrysalide is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 */


#include "storage.h"


#include <assert.h>
#include <malloc.h>
#include <string.h>
#include <unistd.h>


#include "storage-int.h"
#include "../../core/logs.h"



/* Initialise la classe des conservations d'objets en place. */
static void g_object_storage_class_init(GObjectStorageClass *);

/* Initialise une instance de conservation d'objets en place. */
static void g_object_storage_init(GObjectStorage *);

/* Supprime toutes les références externes. */
static void g_object_storage_dispose(GObjectStorage *);

/* Procède à la libération totale de la mémoire. */
static void g_object_storage_finalize(GObjectStorage *);

/* Retrouve l'encadrement pour un nouveau groupe d'objets. */
static storage_backend_t *g_object_storage_find_backend(GObjectStorage *, const char *);



/* Indique le type défini pour une conservation d'objets construits. */
G_DEFINE_TYPE(GObjectStorage, g_object_storage, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des conservations d'objets en place.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_object_storage_class_init(GObjectStorageClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_object_storage_dispose;
    object->finalize = (GObjectFinalizeFunc)g_object_storage_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance de conservation d'objets en place.   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_object_storage_init(GObjectStorage *storage)
{
    storage->tpmem = g_type_memory_new();

    storage->loaded = NULL;

    storage->backends = NULL;
    storage->count = 0;
    g_mutex_init(&storage->mutex);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_object_storage_dispose(GObjectStorage *storage)
{
    g_clear_object(&storage->tpmem);

    g_clear_object(&storage->loaded);

    G_OBJECT_CLASS(g_object_storage_parent_class)->dispose(G_OBJECT(storage));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_object_storage_finalize(GObjectStorage *storage)
{
    size_t i;                               /* Boucle de parcours          */
    storage_backend_t *backend;             /* Gestionnaire à manipuler    */
    int ret;                                /* Bilan d'un appel            */

    g_mutex_lock(&storage->mutex);

    for (i = 0; i < storage->count; i++)
    {
        backend = &storage->backends[i];

        if (backend->fd != -1)
            close(backend->fd);
        else
            assert(false);

        ret = access(backend->filename, W_OK);
        if (ret == 0)
        {
            ret = unlink(backend->filename);
            if (ret != 0) LOG_ERROR_N("unlink");
        }

        free(backend->name);

        free(backend->filename);

    }

    if (storage->backends != NULL)
        free(storage->backends);

    g_mutex_unlock(&storage->mutex);

    g_mutex_clear(&storage->mutex);

    G_OBJECT_CLASS(g_object_storage_parent_class)->finalize(G_OBJECT(storage));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : loaded = contenu binaire à associer.                         *
*                                                                             *
*  Description : Crée le support d'une conservation d'objets en place.        *
*                                                                             *
*  Retour      : Mécanismes mis en place.                                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GObjectStorage *g_object_storage_new(GLoadedContent *loaded)
{
    GObjectStorage *result;                    /* Structure à retourner       */

    result = g_object_new(G_TYPE_OBJECT_STORAGE, NULL);

    result->loaded = loaded;
    g_object_ref(G_OBJECT(loaded));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = gestionnaire de conservations à compléter.         *
*                name    = désignation d'un nouveau groupe d'objets.          *
*                                                                             *
*  Description : Retrouve l'encadrement pour un nouveau groupe d'objets.      *
*                                                                             *
*  Retour      : Informations liées à un groupe ou NULL en cas d'échec.       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static storage_backend_t *g_object_storage_find_backend(GObjectStorage *storage, const char *name)
{
    storage_backend_t *result;              /* Encadrement à retourner     */
    size_t i;                               /* Boucle de parcours          */

    assert(!g_mutex_trylock(&storage->mutex));

    for (i = 0; i < storage->count; i++)
        if (strcmp(storage->backends[i].name, name) == 0)
            break;

    if (i == storage->count)
        result = NULL;
    else
        result = &storage->backends[i];

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage  = gestionnaire de conservations à compléter.        *
*                name     = désignation d'un nouveau groupe d'objets.         *
*                filename = éventuel nom de fichier à utiliser ou NULL.       *
*                                                                             *
*  Description : Ajoute le support d'un nouveau groupe d'objets construits.   *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_object_storage_add_backend(GObjectStorage *storage, const char *name, const char *filename)
{
    bool result;                            /* Bilan à retourner           */
    GBinContent *content;                   /* Contenu binaire traité      */
    const gchar *checksum;                  /* Empreinte de ce contenu     */
    char *prefix;                           /* Début de nom de fichier     */
    storage_backend_t backend;              /* Informations à intégrer     */

    result = false;

    g_mutex_lock(&storage->mutex);

    if (g_object_storage_find_backend(storage, name) != NULL)
        goto exit;

    /* Préparatifs */

    content = g_loaded_content_get_content(storage->loaded);

    checksum = g_binary_content_get_checksum(content);

    asprintf(&prefix, "%s-%s", checksum, name);

    g_object_unref(G_OBJECT(content));

    backend.fd = make_tmp_file(prefix, "cache", &backend.filename);

    free(prefix);

    if (backend.fd == -1)
        goto exit;

    /* Inscription en bonne et due forme */

    backend.name = strdup(name);

    storage->backends = realloc(storage->backends, ++storage->count * sizeof(storage_backend_t));

    storage->backends[storage->count - 1] = backend;

 exit:

    g_mutex_unlock(&storage->mutex);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = gestionnaire à manipuler.                          *
*                name    = désignation d'un nouveau groupe d'objets.          *
*                pos     = tête de lecture avant écriture.                    *
*                                                                             *
*  Description : Charge un objet à partir de données rassemblées.             *
*                                                                             *
*  Retour      : Objet restauré en mémoire ou NULL en cas d'échec.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GSerializableObject *g_object_storage_load_object(GObjectStorage *storage, const char *name, off64_t pos)
{
    GSerializableObject *result;            /* Instance à retourner        */
    bool status;                            /* Bilan d'une opération       */
    storage_backend_t *backend;             /* Informations à consulter    */
    packed_buffer_t pbuf;                   /* Tampon des données à lire   */
    off64_t new;                            /* Nouvelle position de lecture*/

    result = NULL;

    /* Chargement */

    status = false;

    g_mutex_lock(&storage->mutex);

    backend = g_object_storage_find_backend(storage, name);

    if (backend != NULL)
    {
        new = lseek64(backend->fd, pos, SEEK_SET);

        if (new == pos)
        {
            reset_packed_buffer(&pbuf);
            status = read_packed_buffer(&pbuf, backend->fd);
        }

    }

    g_mutex_unlock(&storage->mutex);

    if (!status)
        goto exit;

    /* Phase de conversion */

    result = G_SERIALIZABLE_OBJECT(g_type_memory_create_object(storage->tpmem, &pbuf));

    if (result)
    {
        status = g_serializable_object_load(result, storage, &pbuf);

        if (!status)
            g_clear_object(&result);

    }

    exit_packed_buffer(&pbuf);

 exit:

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = gestionnaire à manipuler.                          *
*                name    = désignation d'un nouveau groupe d'objets.          *
*                pbuf    = zone tampon à parcourir.                           *
*                                                                             *
*  Description : Charge un objet interne à partir de données rassemblées.     *
*                                                                             *
*  Retour      : Objet restauré en mémoire ou NULL en cas d'échec.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GSerializableObject *g_object_storage_unpack_object(GObjectStorage *storage, const char *name, packed_buffer_t *pbuf)
{
    GSerializableObject *result;            /* Instance à retourner        */
    uint64_t pos;                           /* Localisation des données    */
    bool status;                            /* Bilan d'une opération       */

    result = NULL;

    status = extract_packed_buffer(pbuf, &pos, sizeof(uint64_t), true);

    if (status)
        result = g_object_storage_load_object(storage, name, pos);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = gestionnaire à manipuler.                          *
*                name    = désignation d'un nouveau groupe d'objets.          *
*                object  = objet sérialisable à traiter.                      *
*                pos     = tête de lecture avant écriture. [OUT]              *
*                                                                             *
*  Description : Sauvegarde un object sous forme de données rassemblées.      *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_object_storage_store_object(GObjectStorage *storage, const char *name, const GSerializableObject *object, off64_t *pos)
{
    bool result;                            /* Bilan à retourner           */
    packed_buffer_t pbuf;                   /* Tampon des données à écrire */
    storage_backend_t *backend;             /* Informations à consulter    */
    off64_t tmp;                            /* Conservation éphémère       */

    /* Phase de conversion */

    init_packed_buffer(&pbuf);

    result = g_type_memory_store_object_gtype(storage->tpmem, G_OBJECT(object), &pbuf);
    if (!result) goto exit;

    result = g_serializable_object_store(object, storage, &pbuf);
    if (!result) goto exit;

    /* Enregistrement */

    result = false;

    g_mutex_lock(&storage->mutex);

    backend = g_object_storage_find_backend(storage, name);

    if (backend != NULL)
    {
        if (pos == NULL)
            pos = &tmp;

        *pos = lseek64(backend->fd, 0, SEEK_CUR);

        if (*pos != (off64_t)-1)
            result = write_packed_buffer(&pbuf, backend->fd);

    }

    g_mutex_unlock(&storage->mutex);

    /* Sortie propre */

 exit:

    exit_packed_buffer(&pbuf);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = gestionnaire à manipuler.                          *
*                name    = désignation d'un nouveau groupe d'objets.          *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Sauvegarde un object interne sous forme de données.          *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_object_storage_pack_object(GObjectStorage *storage, const char *name, const GSerializableObject *object, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    off64_t pos;                            /* Localisation des données    */

    result = g_object_storage_store_object(storage, name, object, &pos);

    if (result)
        result = extend_packed_buffer(pbuf, (uint64_t []){ pos }, sizeof(uint64_t), true);

    return result;

}
