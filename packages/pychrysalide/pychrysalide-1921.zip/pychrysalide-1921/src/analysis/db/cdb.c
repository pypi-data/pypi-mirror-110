
/* Chrysalide - Outil d'analyse de fichiers binaires
 * cdb.c - manipulation des archives au format CDB
 *
 * Copyright (C) 2014-2019 Cyrille Bagard
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
 *  along with Chrysalide.  If not, see <http://www.gnu.org/licenses/>.
 */


#include "cdb.h"


#include <assert.h>
#include <errno.h>
#include <malloc.h>
#include <poll.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>


#include <i18n.h>
#include <config.h>


#include "backend-int.h"
#include "collection.h"
#include "protocol.h"
#include "snapshot.h"
#include "../../common/compression.h"
#include "../../common/cpp.h"
#include "../../common/extstr.h"
#include "../../common/pathname.h"
#include "../../common/xml.h"
#include "../../core/collections.h"
#include "../../core/logs.h"



/* ------------------------- COEUR DE LA GESTION D'ARCHIVES ------------------------- */


/* Informations relatives à un client */
typedef struct _cdb_client
{
    SSL *tls_fd;                            /* Canal de communication      */
    char *peer_name;                        /* Désignation du correspondant*/
    char *user;                             /* Utilisateur à l'autre bout  */

    uint64_t last_time;                     /* Date de dernier envoi       */

} cdb_client;


/* Description d'une archive d'éléments utilisateur (instance) */
struct _GCdbArchive
{
    GServerBackend parent;                  /* A laisser en premier        */

    rle_string hash;                        /* Empreinte cryptographique   */

    char *filename;                         /* Chemin d'accès à l'archive  */
    char *tmpdir;                           /* Répertoire de travail       */
    char *xml_desc;                         /* Fichier de description      */

    GList *collections;                     /* Ensemble de modifications   */

    GDbSnapshot *snapshot;                  /* Instantanés de bases SQL    */
    sqlite3 *db;                            /* Base de données à manipuler */

    cdb_client *clients;                    /* Connexions en place         */
    size_t count;                           /* Quantité de clients         */
    GMutex clients_access;                  /* Verrou pour l'accès         */

};

/* Description d'une archive d'éléments utilisateur (classe) */
struct _GCdbArchiveClass
{
    GServerBackendClass parent;             /* A laisser en premier        */

};


/* Initialise la classe des archives d'éléments utilisateur. */
static void g_cdb_archive_class_init(GCdbArchiveClass *);

/* Initialise une archive d'éléments utilisateur. */
static void g_cdb_archive_init(GCdbArchive *);

/* Supprime toutes les références externes. */
static void g_cdb_archive_dispose(GCdbArchive *);

/* Procède à la libération totale de la mémoire. */
static void g_cdb_archive_finalize(GCdbArchive *);

/* Ouvre une archive avec tous les éléments à conserver. */
static DBError g_cdb_archive_read(GCdbArchive *);



/* -------------------------- MANIPULATION DES PARTIES XML -------------------------- */


/* Crée la description XML correspondant à l'archive. */
static bool g_cdb_archive_create_xml_desc(const GCdbArchive *, xmlDocPtr *, xmlXPathContextPtr *);

/* Vérifie la conformité d'une description XML avec le serveur. */
static bool g_cdb_archive_check_xml_version(const GCdbArchive *, xmlXPathContextPtr);



/* -------------------------- ACTUALISATION DE COLLECTIONS -------------------------- */


/* Crée et remplit les collections à partir de leurs bases. */
static bool g_cdb_archive_load_collections(GCdbArchive *);

/* Enregistre les signaux associés au suivi des collections. */
static void g_cdb_archive_register_signals(GCdbArchive *);

/* Réagit à une modification au sein d'une collection donnée. */
static void on_collection_extended(GDbCollection *, GDbItem *, GCdbArchive *);

/* Assure le traitement des requêtes de clients. */
static void *g_cdb_archive_process(GCdbArchive *);

/* Prend en compte une connexion nouvelle d'un utilisateur. */
static void g_cdb_archive_add_client(GCdbArchive *, SSL *, const char *, const char *);

/* Dissocie un utilisateur de l'archive. */
static void _g_cdb_archive_remove_client(GCdbArchive *, size_t);

/* Dissocie un utilisateur de l'archive. */
static void g_cdb_archive_remove_client(GCdbArchive *, size_t);

/* Envoie un paquet de données constitué à tous les clients. */
static void g_cdb_archive_send_reply_to_all_clients(GCdbArchive *, packed_buffer_t *);

/* Envoie à tous les clients la nouvelle liste d'instantanés. */
static bool g_cdb_archive_send_snapshot_update(GCdbArchive *, packed_buffer_t *);

/* Envoie à tous les clients le nouvel instantané courant. */
static bool g_cdb_archive_send_snapshot_change(GCdbArchive *, packed_buffer_t *);



/* ---------------------------------------------------------------------------------- */
/*                           COEUR DE LA GESTION D'ARCHIVES                           */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour une une archive d'éléments utilisateur. */
G_DEFINE_TYPE(GCdbArchive, g_cdb_archive, G_TYPE_SERVER_BACKEND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des archives d'éléments utilisateur.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_class_init(GCdbArchiveClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GServerBackendClass *backend;           /* Classe parente              */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_cdb_archive_dispose;
    object->finalize = (GObjectFinalizeFunc)g_cdb_archive_finalize;

    backend = G_SERVER_BACKEND_CLASS(klass);

    backend->thread_name = "cdb_archiver";
    backend->thread_func = (GThreadFunc)g_cdb_archive_process;

    backend->add_client = (add_backend_client_fc)g_cdb_archive_add_client;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une archive d'éléments utilisateur.               *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_init(GCdbArchive *archive)
{
    setup_empty_rle_string(&archive->hash);

    archive->filename = NULL;
    archive->tmpdir = NULL;

    archive->collections = create_collections_list();

    archive->snapshot = NULL;

    g_mutex_init(&archive->clients_access);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_dispose(GCdbArchive *archive)
{
    g_server_backend_stop(G_SERVER_BACKEND(archive));

    g_clear_object(&archive->snapshot);

    g_mutex_clear(&archive->clients_access);

    G_OBJECT_CLASS(g_cdb_archive_parent_class)->dispose(G_OBJECT(archive));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_finalize(GCdbArchive *archive)
{
#ifndef NDEBUG
    int ret;                                /* Bilan d'un appel            */
#endif

    if (archive->db != NULL)
    {
#ifndef NDEBUG
        ret = sqlite3_close(archive->db);
        assert(ret == SQLITE_OK);
#else
        sqlite3_close(archive->db);
#endif
    }

    if (archive->xml_desc != NULL)
        free(archive->xml_desc);

    if (archive->filename != NULL)
        free(archive->filename);

    if (archive->tmpdir != NULL)
        free(archive->tmpdir);

    exit_rle_string(&archive->hash);

    G_OBJECT_CLASS(g_cdb_archive_parent_class)->finalize(G_OBJECT(archive));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : basedir = répertoire de stockage des enregistrements.        *
*                tmpdir  = répertoire de travail temporaire.                  *
*                hash    = empreinte du binaire à représenter.                *
*                error   = indication éventuelle en cas d'échec. [OUT]        *
*                                                                             *
*  Description : Définit ou ouvre une archive d'éléments utilisateur.         *
*                                                                             *
*  Retour      : Structure mise en plae ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : Les chaînes sont assurées d'être non vides ; la procédure    *
*                assume un transfert de propriété.                            *
*                                                                             *
******************************************************************************/

GCdbArchive *g_cdb_archive_new(const char *basedir, const char *tmpdir, const rle_string *hash, DBError *error)
{
    GCdbArchive *result;                    /* Adresse à retourner         */
    int ret;                                /* Retour d'un appel           */
    struct stat finfo;                      /* Information sur l'archive   */

    result = g_object_new(G_TYPE_CDB_ARCHIVE, NULL);

    dup_into_rle_string(&result->hash, get_rle_string(hash));

    *error = DBE_SYS_ERROR;

    /* Chemin de l'archive */

    result->filename = strdup(basedir);
    result->filename = stradd(result->filename, hash->data);
    result->filename = stradd(result->filename, ".cdb.tar.xz");

    if (!mkpath(result->filename))
        goto error;

    /* Chemin des enregistrements temporaires */

    result->tmpdir = strdup(tmpdir);

    if (!mkpath(tmpdir))
        goto error;

    ret = asprintf(&result->xml_desc, "%s" G_DIR_SEPARATOR_S "%s_desc.xml", tmpdir, get_rle_string(hash));
    if (ret == -1) goto no_tmp;

    ret = ensure_path_exists(result->xml_desc);
    if (ret == -1) goto no_tmp;

    /* Création de l'archive si elle n'existe pas */

    ret = stat(result->filename, &finfo);

    if (ret != 0)
    {
        /* Le soucis ne vient pas de l'absence du fichier... */
        if (errno != ENOENT) goto error;

        result->snapshot = g_db_snapshot_new_empty(tmpdir, get_rle_string(hash), result->collections);

        if (result->snapshot == NULL)
            goto error;

        /* Récupération de la base courante */

        result->db = g_db_snapshot_get_database(result->snapshot);

        if (result->db == NULL)
        {
            *error = DBE_XML_ERROR;
            goto error;
        }

        *error = DBE_NONE;

    }

    else if (!S_ISREG(finfo.st_mode))
        goto error;

    else
    {
        /* Ouverture de l'archive */

        *error = g_cdb_archive_read(result);

        if (*error != DBE_NONE)
            goto error;

        /* Récupération de la base courante */

        result->db = g_db_snapshot_get_database(result->snapshot);

        if (result->db == NULL)
        {
            *error = DBE_XML_ERROR;
            goto error;
        }

        /* Chargement des éléments sauvegardés */

        if (!g_cdb_archive_load_collections(result))
        {
            *error = DBE_DB_LOADING_ERROR;
            goto error;
        }

    }

    /* Ultimes connexions */

    g_cdb_archive_register_signals(result);

    return result;

 no_tmp:

 error:

    g_object_unref(G_OBJECT(result));

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = informations quant à l'archive à interpréter.      *
*                                                                             *
*  Description : Ouvre une archive avec tous les éléments à conserver.        *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static DBError g_cdb_archive_read(GCdbArchive *archive)
{
    DBError result;                         /* Conclusion à retourner      */
    struct archive *in;                     /* Archive à consulter         */
    int ret;                                /* Bilan d'un appel            */
    struct archive_entry *entry;            /* Elément de l'archive        */
    const char *path;                       /* Désignation d'un fichier    */
    xmlDocPtr xdoc;                         /* Document XML à créer        */
    xmlXPathContextPtr context;             /* Contexte pour les recherches*/
    bool status;                            /* Bilan d'un chargement       */

    result = DBE_ARCHIVE_ERROR;

    in = archive_read_new();
    archive_read_support_filter_all(in);
    archive_read_support_format_all(in);

    ret = archive_read_open_filename(in, archive->filename, 10240 /* ?! */);
    if (ret != ARCHIVE_OK) goto bad_archive;

    for (ret = archive_read_next_header(in, &entry);
         ret == ARCHIVE_OK;
         ret = archive_read_next_header(in, &entry))
    {
        path = archive_entry_pathname(entry);

        if (strcmp(path, "desc.xml") == 0)
        {
            if (!dump_archive_entry_into_file(in, entry, archive->xml_desc))
                goto load_error;

            if (!open_xml_file(archive->xml_desc, &xdoc, &context))
                goto load_error;

            if (!g_cdb_archive_check_xml_version(archive, context))
            {
                result = DBE_XML_VERSION_ERROR;
                goto load_error;
            }

            archive->snapshot = g_db_snapshot_new_from_xml(archive->tmpdir, get_rle_string(&archive->hash),
                                                           xdoc, context);

            close_xml_file(xdoc, context);

            ret = unlink(archive->xml_desc);
            if (ret != 0) LOG_ERROR_N("unlink");

            if (archive->snapshot == NULL)
                goto load_error;

            break;


        }

    }

    archive_read_close(in);
    archive_read_free(in);

    in = archive_read_new();
    archive_read_support_filter_all(in);
    archive_read_support_format_all(in);

    ret = archive_read_open_filename(in, archive->filename, 10240 /* ?! */);
    if (ret != ARCHIVE_OK) goto bad_archive;

    status = g_db_snapshot_fill(archive->snapshot, in);
    if (!status) goto load_error;

    result = DBE_NONE;

 load_error:

 bad_archive:

    archive_read_close(in);
    archive_read_free(in);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = informations quant à l'archive à créer.            *
*                                                                             *
*  Description : Enregistre une archive avec tous les éléments à conserver.   *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

DBError g_cdb_archive_write(const GCdbArchive *archive)
{
    DBError result;                         /* Conclusion à retourner      */
    struct archive *out;                    /* Archive à constituer        */
    int ret;                                /* Bilan d'un appel            */
    xmlDocPtr xdoc;                         /* Document XML à créer        */
    xmlXPathContextPtr context;             /* Contexte pour les recherches*/
    bool status;                            /* Bilan d'un appel            */
    CPError error;                          /* Bilan d'une compression     */

    out = archive_write_new();
    archive_write_add_filter_xz(out);
    archive_write_set_format_gnutar(out);

    ret = archive_write_open_filename(out, archive->filename);
    if (ret != ARCHIVE_OK)
    {
        result = DBE_ARCHIVE_ERROR;
        goto bad_archive;
    }

    status = g_cdb_archive_create_xml_desc(archive, &xdoc, &context);

    if (!status)
    {
        result = DBE_XML_ERROR;
        goto bad_archive;
    }

    /* Enregistrement des bases */

    result = g_db_snapshot_save(archive->snapshot, xdoc, context, out);

    if (result != DBE_NONE)
        goto bad_archive;

    /* Enregistrement du document XML */

    status = save_xml_file(xdoc, archive->xml_desc);

    close_xml_file(xdoc, context);

    if (!status)
    {
        result = DBE_SYS_ERROR;
        goto bad_xml;
    }

    error = add_file_into_archive(out, archive->xml_desc, "desc.xml");

    switch (error)
    {
        case CPE_NO_ERROR:
            break;

        case CPE_SYSTEM_ERROR:
            result = DBE_SYS_ERROR;
            break;

        case CPE_ARCHIVE_ERROR:
            result = DBE_ARCHIVE_ERROR;
            break;

    }

 bad_xml:

    ret = unlink(archive->xml_desc);
    if (ret != 0) LOG_ERROR_N("unlink");

 bad_archive:

    archive_write_close(out);
    archive_write_free(out);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = informations quant à l'archive à consulter.        *
*                hash    = empreinte extérieure à comparer.                   *
*                                                                             *
*  Description : Détermine si une empreinte correspond à celle d'une archive. *
*                                                                             *
*  Retour      : Résultat de la comparaison : -1, 0 ou 1.                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int g_cdb_archive_compare_hash(const GCdbArchive *archive, const rle_string *hash)
{
    return cmp_rle_string(&archive->hash, hash);

}



/* ---------------------------------------------------------------------------------- */
/*                            MANIPULATION DES PARTIES XML                            */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à constituer.                              *
*                xdoc    = document XML à compléter. [OUT]                    *
*                context = contexte pour les recherches. [OUT]                *
*                                                                             *
*  Description : Crée la description XML correspondant à l'archive.           *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_cdb_archive_create_xml_desc(const GCdbArchive *archive, xmlDocPtr *xdoc, xmlXPathContextPtr *context)
{
    bool result;                            /* Bilan à retourner           */

    result = create_new_xml_file(xdoc, context);

    if (result)
        result = add_content_to_node(*xdoc, *context, "/ChrysalideBinary/Version", PACKAGE_VERSION);

    if (result)
        result = add_content_to_node(*xdoc, *context, "/ChrysalideBinary/Protocol", XSTR(CDB_PROTOCOL_VERSION));

    if (result)
        result = add_content_to_node(*xdoc, *context, "/ChrysalideBinary/Hash", archive->hash.data);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à consulter.                               *
*                context = contexte pour les recherches.                      *
*                                                                             *
*  Description : Vérifie la conformité d'une description XML avec le serveur. *
*                                                                             *
*  Retour      : Bilan de la vérification.                                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_cdb_archive_check_xml_version(const GCdbArchive *archive, xmlXPathContextPtr context)
{
    bool result;                            /* Bilan à retourner           */
    char *version;                          /* Version protocolaire        */
    unsigned long int used;                 /* Version utilisée            */

    result = NULL;

    version = get_node_text_value(context, "/ChrysalideBinary/Protocol");
    if (version == NULL) return false;

    used = strtoul(version, NULL, 16);

    result = (used == CDB_PROTOCOL_VERSION);

    free(version);

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                            ACTUALISATION DE COLLECTIONS                            */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive dont les collections sont à initialiser.   *
*                                                                             *
*  Description : Crée et remplit les collections à partir de leurs bases.     *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_cdb_archive_load_collections(GCdbArchive *archive)
{
    GList *iter;                            /* Boucle de parcours          */
    GDbCollection *collec;                  /* Collection visée manipulée  */

    for (iter = g_list_first(archive->collections);
         iter != NULL;
         iter = g_list_next(iter))
    {
        collec = G_DB_COLLECTION(iter->data);

        if (!g_db_collection_load_all_items(collec, archive->db))
            return false;

    }

    return true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive dont les collections sont à suivre.        *
*                                                                             *
*  Description : Enregistre les signaux associés au suivi des collections.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_register_signals(GCdbArchive *archive)
{
    GList *iter;                            /* Boucle de parcours          */
    GDbCollection *collec;                  /* Collection visée manipulée  */

    for (iter = g_list_first(archive->collections);
         iter != NULL;
         iter = g_list_next(iter))
    {
        collec = G_DB_COLLECTION(iter->data);

        g_signal_connect(collec, "content-extended", G_CALLBACK(on_collection_extended), archive);

    }

}


/******************************************************************************
*                                                                             *
*  Paramètres  : collec  = collection dont le contenu a évolué.               *
*                item    = élément ajouté, modifié ou supprimé.               *
*                archive = centralisation de tous les savoirs.                *
*                                                                             *
*  Description : Réagit à une modification au sein d'une collection donnée.   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void on_collection_extended(GDbCollection *collec, GDbItem *item, GCdbArchive *archive)
{
    packed_buffer_t pbuf;                   /* Tampon d'émission           */
    size_t i;                               /* Boucle de parcours          */
    bool status;                            /* Bilan d'un envoi de retour  */

    init_packed_buffer(&pbuf);

    status = g_db_collection_pack(collec, &pbuf, DBA_ADD_ITEM, item);

    g_mutex_lock(&archive->clients_access);

    for (i = 0; i < archive->count && status; i++)
    {
        status = ssl_send_packed_buffer(&pbuf, archive->clients[i].tls_fd);

        if (!status)
            LOG_ERROR(LMT_ERROR, _("Failed to send some DB update"));

    }

    g_mutex_unlock(&archive->clients_access);

    exit_packed_buffer(&pbuf);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = centralisation de tous les savoirs.                *
*                                                                             *
*  Description : Assure le traitement des requêtes de clients.                *
*                                                                             *
*  Retour      : NULL.                                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void *g_cdb_archive_process(GCdbArchive *archive)
{
    GServerBackend *base;                   /* Base de l'instance          */
    struct pollfd *fds;                     /* Surveillance des flux       */
    nfds_t nfds;                            /* Quantité de ces flux        */
    nfds_t i;                               /* Boucle de parcours          */
    int ret;                                /* Bilan d'un appel            */
    packed_buffer_t in_pbuf;                /* Tampon de réception         */
    uint32_t tmp32;                         /* Valeur sur 32 bits          */
    bool status;                            /* Bilan de lecture initiale   */
    uint32_t command;                       /* Commande de la requête      */
    DBError error;                          /* Bilan d'une opération       */
    packed_buffer_t out_pbuf;               /* Tampon d'émission           */
    GDbCollection *collec;                  /* Collection visée au final   */
    bool reload;                            /* Besoin de rechargement      */
    char *msg;                              /* Erreur à faire remonter     */

    base = G_SERVER_BACKEND(archive);

    fds = NULL;

    while (1)
    {
        /* Reconstitution d'une liste à jour */

        g_mutex_lock(&archive->clients_access);

        nfds = archive->count + 2;
        fds = realloc(fds, nfds * sizeof(struct pollfd));

        for (i = 0; i < (nfds - 2); i++)
        {
            fds[i].fd = SSL_get_fd(archive->clients[i].tls_fd);
            fds[i].events = POLLIN | POLLPRI;
        }

        g_mutex_unlock(&archive->clients_access);

        if (nfds == 2)
            goto gcap_no_more_clients;

        fds[nfds - 2].fd = base->stop_ctrl[0];
        fds[nfds - 2].events = POLLIN | POLLPRI;

        fds[nfds - 1].fd = base->refresh_ctrl[0];
        fds[nfds - 1].events = POLLIN | POLLPRI;

        /* Lancement d'une phase de surveillance */

        ret = poll(fds, nfds, -1);
        if (ret == -1)
        {
            LOG_ERROR_N("poll");
            break;
        }

        /* Demande expresse d'arrêt des procédures */
        if (fds[nfds - 2].revents)
            break;

        /* Demande d'actualisation */
        if (fds[nfds - 1].revents)
            continue;

        /* Traitement des requêtes reçues */

        for (i = 0; i < (nfds - 1); i++)
        {
            /* Le canal est fermé, une sortie doit être demandée... */
            if (fds[i].revents & POLLNVAL)
                goto closed_exchange;

            /**
             * Même chose, cf. "TCP: When is EPOLLHUP generated?"
             * https://stackoverflow.com/questions/52976152/tcp-when-is-epollhup-generated/52976327#52976327
             */

            if (fds[i].revents & (POLLHUP | POLLRDHUP))
                goto closed_exchange;

            /* Données présentes en entrée */
            if (fds[i].revents & (POLLIN | POLLPRI))
            {
                init_packed_buffer(&in_pbuf);

                status = ssl_recv_packed_buffer(&in_pbuf, archive->clients[i].tls_fd);
                if (!status) goto gcap_bad_exchange;

 next_command:

                status = extract_packed_buffer(&in_pbuf, &tmp32, sizeof(uint32_t), true);
                if (!status) goto gcap_bad_exchange;

                command = tmp32;

                switch (command)
                {
                    case DBC_SAVE:

                        error = g_cdb_archive_write(archive);

                        init_packed_buffer(&out_pbuf);

                        status = extend_packed_buffer(&out_pbuf, (uint32_t []) { DBC_SAVE },
                                                      sizeof(uint32_t), true);
                        if (!status) goto gcap_bad_reply;

                        status = extend_packed_buffer(&out_pbuf, (uint32_t []) { error }, sizeof(uint32_t), true);
                        if (!status) goto gcap_bad_reply;

                        status = ssl_send_packed_buffer(&out_pbuf, archive->clients[i].tls_fd);
                        if (!status) goto gcap_bad_reply;

                        exit_packed_buffer(&out_pbuf);

                        break;

                    case DBC_COLLECTION:

                        status = extract_packed_buffer(&in_pbuf, &tmp32, sizeof(uint32_t), true);
                        if (!status) goto gcap_bad_exchange;

                        collec = find_collection_in_list(archive->collections, tmp32);
                        if (collec == NULL) goto gcap_bad_exchange;

                        status = g_db_collection_unpack(collec, &in_pbuf, archive->db);
                        if (!status) goto gcap_bad_exchange;

                        break;

                    case DBC_GET_ALL_ITEMS:

                        init_packed_buffer(&out_pbuf);

                        status = extend_packed_buffer(&out_pbuf, (uint32_t []) { DBC_SET_ALL_ITEMS },
                                                      sizeof(uint32_t), true);
                        if (!status) goto gcap_bad_reply;

                        status = extend_packed_buffer(&out_pbuf, (uint8_t []) { 0x1 }, sizeof(uint8_t), true);
                        if (!status) goto gcap_bad_reply;

                        status = pack_all_collection_updates(archive->collections, &out_pbuf);
                        if (!status) goto gcap_bad_reply;

                        status = extend_packed_buffer(&out_pbuf, (uint32_t []) { DBC_SET_ALL_ITEMS },
                                                      sizeof(uint32_t), true);
                        if (!status) goto gcap_bad_reply;

                        status = extend_packed_buffer(&out_pbuf, (uint8_t []) { 0x0 }, sizeof(uint8_t), true);
                        if (!status) goto gcap_bad_reply;

                        status = ssl_send_packed_buffer(&out_pbuf, archive->clients[i].tls_fd);
                        if (!status) goto gcap_bad_reply;

                        exit_packed_buffer(&out_pbuf);

                        break;

                    case DBC_SET_ALL_ITEMS:
                        asprintf(&msg, _("This command is not available on this side: 0x%08x"), command);
                        LOG_ERROR(LMT_ERROR, msg);
                        free(msg);
                        goto gcap_bad_exchange;
                        break;

                    case DBC_SET_LAST_ACTIVE:

                        init_packed_buffer(&out_pbuf);

                        status = update_activity_in_collections(archive->collections, \
                                                                &in_pbuf, &out_pbuf, archive->db);
                        if (!status) goto gcap_bad_reply;

                        status = ssl_send_packed_buffer(&out_pbuf, archive->clients[i].tls_fd);
                        if (!status) goto gcap_bad_reply;

                        exit_packed_buffer(&out_pbuf);

                        break;

                    case DBC_GET_SNAPSHOTS:

                        if (!g_cdb_archive_send_snapshot_update(archive, &out_pbuf))
                            goto critical_error;

                        status = ssl_send_packed_buffer(&out_pbuf, archive->clients[i].tls_fd);
                        if (!status) goto gcap_bad_reply;

                        exit_packed_buffer(&out_pbuf);

                        break;

                    case DBC_GET_CUR_SNAPSHOT:

                        if (!g_cdb_archive_send_snapshot_change(archive, &out_pbuf))
                            goto critical_error;

                        status = ssl_send_packed_buffer(&out_pbuf, archive->clients[i].tls_fd);
                        if (!status) goto gcap_bad_reply;

                        exit_packed_buffer(&out_pbuf);

                        break;

                    case DBC_CUR_SNAPSHOT_UPDATED:
                        log_variadic_message(LMT_INFO,
                                             _("This command is not available on this side: 0x%08x"), command);
                        goto gcap_bad_exchange;
                        break;

                    case DBC_SET_CUR_SNAPSHOT:

                        error = g_db_snapshot_restore(archive->snapshot, &in_pbuf, &reload);

                        if (error == DBE_NONE)
                        {
#ifndef NDEBUG
                            ret = sqlite3_close(archive->db);
                            assert(ret == SQLITE_OK);
#else
                            sqlite3_close(archive->db);
#endif

                            archive->db = g_db_snapshot_get_database(archive->snapshot);

                            if (archive->db == NULL)
                            {
                                error = DBE_SNAPSHOT_RESTORE_FAILURE;
                            }

                            else
                            {
                                if (!g_cdb_archive_send_snapshot_change(archive, NULL))
                                    goto critical_error;
                            }

                        }

                        else if (error == DBE_BAD_EXCHANGE)
                            goto gcap_bad_exchange;

                        break;

                    case DBC_SET_SNAPSHOT_NAME:

                        error = g_db_snapshot_set_name(archive->snapshot, &in_pbuf);

                        if (error == DBE_NONE)
                        {
                            if (!g_cdb_archive_send_snapshot_update(archive, NULL))
                                goto critical_error;
                        }

                        else if (error == DBE_BAD_EXCHANGE)
                            goto gcap_bad_exchange;

                        break;

                    case DBC_SET_SNAPSHOT_DESC:

                        error = g_db_snapshot_set_desc(archive->snapshot, &in_pbuf);

                        if (error == DBE_NONE)
                        {
                            if (!g_cdb_archive_send_snapshot_update(archive, NULL))
                                goto critical_error;
                        }

                        else if (error == DBE_BAD_EXCHANGE)
                            goto gcap_bad_exchange;

                        break;

                    case DBC_CREATE_SNAPSHOT:

                        error = g_db_snapshot_create(archive->snapshot, archive->db);

                        if (error == DBE_NONE)
                        {
                            if (!g_cdb_archive_send_snapshot_update(archive, NULL))
                                goto critical_error;
                        }

                        else if (error == DBE_BAD_EXCHANGE)
                            goto gcap_bad_exchange;

                        break;

                    case DBC_REMOVE_SNAPSHOT:

                        error = g_db_snapshot_remove(archive->snapshot, &in_pbuf, &reload);

                        if (error == DBE_NONE)
                        {
                            if (!g_cdb_archive_send_snapshot_update(archive, NULL))
                                goto critical_error;

                            if (reload)
                            {
                                if (!g_cdb_archive_send_snapshot_change(archive, NULL))
                                    goto critical_error;
                            }

                        }

                        else if (error == DBE_BAD_EXCHANGE)
                            goto gcap_bad_exchange;

                        break;

                    default:
                        asprintf(&msg, _("Bad protocol command: 0x%08x"), command);
                        LOG_ERROR(LMT_ERROR, msg);
                        free(msg);
                        goto gcap_bad_exchange;
                        break;

                }

                if (has_more_data_in_packed_buffer(&in_pbuf))
                    goto next_command;

                exit_packed_buffer(&in_pbuf);

                continue;

 gcap_bad_reply:

                exit_packed_buffer(&out_pbuf);

 gcap_bad_exchange:

                LOG_ERROR(LMT_ERROR, _("Bad exchange"));

                assert(0);

                exit_packed_buffer(&in_pbuf);

 closed_exchange:

                g_cdb_archive_remove_client(archive, i);

                continue;

 critical_error:

                LOG_ERROR(LMT_ERROR, _("Internal critical error"));

                assert(0);

            }

        }

    }

    /* On disparaît des écrans... */

 gcap_no_more_clients:

    g_server_backend_stop(G_SERVER_BACKEND(archive));

    if (fds != NULL)
        free(fds);

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive   = support pour le suivi d'une connexion.           *
*                fd        = canal de communication réseau ouvert.            *
*                peer_name = désignation de la connexion.                     *
*                user      = désignation de l'utilisateur de la connexion.    *
*                                                                             *
*  Description : Prend en compte une connexion nouvelle d'un utilisateur.     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_add_client(GCdbArchive *archive, SSL *fd, const char *peer_name, const char *user)
{
    cdb_client *client;                     /* Nouvelle fiche d'entité     */

    /**
     * La situation est un peu compliquée lors de l'accueil d'un nouveau client :
     *
     *    - soit on envoie tous les éléments à prendre en compte, mais on doit
     *      bloquer la base de données jusqu'à l'intégration pleine et entière
     *      du client, afin que ce dernier ne loupe pas l'envoi d'un nouvel
     *      élément entre temps.
     *
     *    - soit on intègre le client et celui ci demande des mises à jour
     *      collection par collection ; c'est également à lui que revient le rejet
     *      des éléments envoyés en solitaires avant la réception de la base
     *      complète.
     *
     * On fait le choix du second scenario ici, du fait de la difficulté
     * de maîtriser facilement la reconstitution d'une liste de clients dans
     * g_cdb_archive_process() depuis un autre flot d'exécution.
     */

    g_mutex_lock(&archive->clients_access);

    archive->clients = realloc(archive->clients, ++archive->count * sizeof(cdb_client));

    client = &archive->clients[archive->count - 1];

    client->tls_fd = fd;
    client->peer_name = strdup(peer_name);
    client->user = strdup(user);

    g_mutex_unlock(&archive->clients_access);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à connecter avec un utilisateur.           *
*                index   = indice de l'utilisateur concerné.                  *
*                                                                             *
*  Description : Dissocie un utilisateur de l'archive.                        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void _g_cdb_archive_remove_client(GCdbArchive *archive, size_t index)
{
    cdb_client *client;                     /* Client à traiter            */

    assert(!g_mutex_trylock(&archive->clients_access));

    client = &archive->clients[index];

    SSL_free(client->tls_fd);
    free(client->user);

    if ((index + 1) < archive->count)
        memmove(&archive->clients[index], &archive->clients[index + 1],
                (archive->count - index - 1) * sizeof(cdb_client));

    archive->clients = realloc(archive->clients, --archive->count * sizeof(cdb_client));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à connecter avec un utilisateur.           *
*                index   = indice de l'utilisateur concerné.                  *
*                                                                             *
*  Description : Dissocie un utilisateur de l'archive.                        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_remove_client(GCdbArchive *archive, size_t index)
{
    g_mutex_lock(&archive->clients_access);

    _g_cdb_archive_remove_client(archive, index);

    g_mutex_unlock(&archive->clients_access);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à connecter avec un utilisateur.           *
*                pbuf    = paquet de données à émettre.                       *
*                                                                             *
*  Description : Envoie un paquet de données constitué à tous les clients.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_cdb_archive_send_reply_to_all_clients(GCdbArchive *archive, packed_buffer_t *pbuf)
{
    size_t i;                               /* Boucle de parcours          */
    bool status;                            /* Bilan d'une émission        */

    g_mutex_lock(&archive->clients_access);

    for (i = 0; i < archive->count; i++)
    {
        status = ssl_send_packed_buffer(pbuf, archive->clients[i].tls_fd);
        if (!status)
        {
            log_variadic_message(LMT_ERROR, _("Error while replying to client %zu"), i);

            _g_cdb_archive_remove_client(archive, i);
            i--;

        }

    }

    g_mutex_unlock(&archive->clients_access);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à connecter avec un utilisateur.           *
*                pbuf    = paquet à consituer pour un envoi unique. [OUT]     *
*                                                                             *
*  Description : Envoie à tous les clients la nouvelle liste d'instantanés.   *
*                                                                             *
*  Retour      : Bilan de constitution de la réponse.                         *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_cdb_archive_send_snapshot_update(GCdbArchive *archive, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    bool do_send;                           /* Réalisation de l'émission   */
    packed_buffer_t out_pbuf;               /* Tampon d'émission           */

    do_send = (pbuf == NULL);

    if (pbuf == NULL)
        pbuf = &out_pbuf;

    init_packed_buffer(pbuf);

    result = extend_packed_buffer(pbuf, (uint32_t []) { DBC_SNAPSHOTS_UPDATED },
                                  sizeof(uint32_t), true);
    if (!result) goto bad_reply;

    result = g_db_snapshot_pack_all(archive->snapshot, pbuf);
    if (!result) goto bad_reply;

    result = extend_packed_buffer(pbuf, SNAPSHOT_END_MARK, SNAP_ID_HEX_SZ, false);
    if (!result) goto bad_reply;

    if (do_send)
        g_cdb_archive_send_reply_to_all_clients(archive, pbuf);

 bad_reply:

    if (do_send || !result)
        exit_packed_buffer(pbuf);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : archive = archive à connecter avec un utilisateur.           *
*                pbuf    = paquet à consituer pour un envoi unique. [OUT]     *
*                                                                             *
*  Description : Envoie à tous les clients le nouvel instantané courant.      *
*                                                                             *
*  Retour      : Bilan de constitution de la réponse.                         *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_cdb_archive_send_snapshot_change(GCdbArchive *archive, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    bool do_send;                           /* Réalisation de l'émission   */
    packed_buffer_t out_pbuf;               /* Tampon d'émission           */
    snapshot_id_t id;                       /* Identifiant d'instantané    */

    do_send = (pbuf == NULL);

    if (pbuf == NULL)
        pbuf = &out_pbuf;

    init_packed_buffer(pbuf);

    result = extend_packed_buffer(pbuf, (uint32_t []) { DBC_CUR_SNAPSHOT_UPDATED },
                                  sizeof(uint32_t), true);
    if (!result) goto bad_reply;

    result = g_db_snapshot_get_current_id(archive->snapshot, &id);
    assert(result);
    if (!result) goto bad_reply;

    result = pack_snapshot_id(&id, pbuf);
    if (!result) goto bad_reply;

    if (do_send)
        g_cdb_archive_send_reply_to_all_clients(archive, pbuf);

 bad_reply:

    if (do_send || !result)
        exit_packed_buffer(pbuf);

    return result;

}
