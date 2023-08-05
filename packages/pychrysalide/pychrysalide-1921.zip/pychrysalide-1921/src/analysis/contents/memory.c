
/* Chrysalide - Outil d'analyse de fichiers binaires
 * memory.c - chargement de données binaires à partir de la mémoire
 *
 * Copyright (C) 2018-2019 Cyrille Bagard
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


#include "memory.h"


#include <assert.h>
#include <malloc.h>
#include <string.h>
#include <unistd.h>


#include <i18n.h>


#include "file.h"
#include "../content-int.h"
#include "../../common/extstr.h"
#include "../../common/io.h"



/* Contenu de données binaires résidant en mémoire (instance) */
struct _GMemoryContent
{
    GObject parent;                         /* A laisser en premier        */

    char *storage;                          /* Conservation des données    */
    GBinContent *backend;                   /* Exploitation des données    */

};

/* Contenu de données binaires résidant en mémoire (classe) */
struct _GMemoryContentClass
{
    GObjectClass parent;                    /* A laisser en premier        */

};


/* Initialise la classe des contenus de données en mémoire. */
static void g_memory_content_class_init(GMemoryContentClass *);

/* Initialise une instance de contenu de données en mémoire. */
static void g_memory_content_init(GMemoryContent *);

/* Procède à l'initialisation de l'interface de lecture. */
static void g_memory_content_interface_init(GBinContentInterface *);

/* Supprime toutes les références externes. */
static void g_memory_content_dispose(GMemoryContent *);

/* Procède à la libération totale de la mémoire. */
static void g_memory_content_finalize(GMemoryContent *);

/* Donne l'origine d'un contenu binaire. */
static GBinContent *g_memory_content_get_root(GMemoryContent *);

/* Fournit le nom associé au contenu binaire. */
static char *g_memory_content_describe(const GMemoryContent *, bool);

/* Ecrit une sauvegarde de contenu binaire dans un fichier XML. */
static bool g_memory_content_save(const GMemoryContent *, xmlDocPtr, xmlXPathContextPtr, const char *, const char *);

/* Fournit une empreinte unique (SHA256) pour les données. */
static void g_memory_content_compute_checksum(GMemoryContent *, GChecksum *);

/* Détermine le nombre d'octets lisibles. */
static phys_t g_memory_content_compute_size(const GMemoryContent *);

/* Détermine la position initiale d'un contenu. */
static void g_memory_content_compute_start_pos(const GMemoryContent *, vmpa2t *);

/* Détermine la position finale d'un contenu. */
static void g_memory_content_compute_end_pos(const GMemoryContent *, vmpa2t *);

/* Avance la tête de lecture d'une certaine quantité de données. */
static bool g_memory_content_seek(const GMemoryContent *, vmpa2t *, phys_t);

/* Donne accès à une portion des données représentées. */
static const bin_t *g_memory_content_get_raw_access(const GMemoryContent *, vmpa2t *, phys_t);

/* Fournit une portion des données représentées. */
static bool g_memory_content_read_raw(const GMemoryContent *, vmpa2t *, phys_t, bin_t *);

/* Lit un nombre non signé sur quatre bits. */
static bool g_memory_content_read_u4(const GMemoryContent *, vmpa2t *, bool *, uint8_t *);

/* Lit un nombre non signé sur un octet. */
static bool g_memory_content_read_u8(const GMemoryContent *, vmpa2t *, uint8_t *);

/* Lit un nombre non signé sur deux octets. */
static bool g_memory_content_read_u16(const GMemoryContent *, vmpa2t *, SourceEndian, uint16_t *);

/* Lit un nombre non signé sur quatre octets. */
static bool g_memory_content_read_u32(const GMemoryContent *, vmpa2t *, SourceEndian, uint32_t *);

/* Lit un nombre non signé sur huit octets. */
static bool g_memory_content_read_u64(const GMemoryContent *, vmpa2t *, SourceEndian, uint64_t *);

/* Lit un nombre non signé encodé au format LEB128. */
static bool g_memory_content_read_uleb128(const GMemoryContent *, vmpa2t *, uleb128_t *);

/* Lit un nombre signé encodé au format LEB128. */
static bool g_memory_content_read_leb128(const GMemoryContent *, vmpa2t *, leb128_t *);



/* Indique le type défini par la GLib pour les contenus de données en mémoire. */
G_DEFINE_TYPE_WITH_CODE(GMemoryContent, g_memory_content, G_TYPE_OBJECT,
                        G_IMPLEMENT_INTERFACE(G_TYPE_BIN_CONTENT, g_memory_content_interface_init));


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des contenus de données en mémoire.     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_class_init(GMemoryContentClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_memory_content_dispose;
    object->finalize = (GObjectFinalizeFunc)g_memory_content_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance de contenu de données en mémoire.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_init(GMemoryContent *content)
{
    content->storage = NULL;
    content->backend = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de lecture.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_interface_init(GBinContentInterface *iface)
{
    iface->get_root = (get_content_root_fc)g_memory_content_get_root;

    iface->describe = (describe_content_fc)g_memory_content_describe;

    iface->save = (save_content_fc)g_memory_content_save;

    iface->compute_checksum = (compute_checksum_fc)g_memory_content_compute_checksum;

    iface->compute_size = (compute_size_fc)g_memory_content_compute_size;
    iface->compute_start_pos = (compute_start_pos_fc)g_memory_content_compute_start_pos;
    iface->compute_end_pos = (compute_end_pos_fc)g_memory_content_compute_end_pos;

    iface->seek = (seek_fc)g_memory_content_seek;

    iface->get_raw_access = (get_raw_access_fc)g_memory_content_get_raw_access;

    iface->read_raw = (read_raw_fc)g_memory_content_read_raw;
    iface->read_u4 = (read_u4_fc)g_memory_content_read_u4;
    iface->read_u8 = (read_u8_fc)g_memory_content_read_u8;
    iface->read_u16 = (read_u16_fc)g_memory_content_read_u16;
    iface->read_u32 = (read_u32_fc)g_memory_content_read_u32;
    iface->read_u64 = (read_u64_fc)g_memory_content_read_u64;

    iface->read_uleb128 = (read_uleb128_fc)g_memory_content_read_uleb128;
    iface->read_leb128 = (read_leb128_fc)g_memory_content_read_leb128;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_dispose(GMemoryContent *content)
{
    if (content->backend)
        g_object_unref(G_OBJECT(content->backend));

    G_OBJECT_CLASS(g_memory_content_parent_class)->dispose(G_OBJECT(content));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_finalize(GMemoryContent *content)
{
    if (content->storage != NULL)
    {
        unlink(content->storage);
        free(content->storage);
    }

    G_OBJECT_CLASS(g_memory_content_parent_class)->finalize(G_OBJECT(content));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : data = données du contenu volatile.                          *
*                size = quantité de ces données.                              *
*                                                                             *
*  Description : Charge en mémoire le contenu de données brutes.              *
*                                                                             *
*  Retour      : Représentation de contenu à manipuler ou NULL en cas d'échec.*
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GBinContent *g_memory_content_new(const bin_t *data, phys_t size)
{
    GMemoryContent *result;                 /* Structure à retourner      */
    int fd;                                 /* Descripteur du fichier      */
    bool status;                            /* Bilan des écritures         */

    result = g_object_new(G_TYPE_MEMORY_CONTENT, NULL);

    fd = make_tmp_file("memcnt", "bin", &result->storage);
    if (fd == -1) goto gmcn_error;

    status = safe_write(fd, data, size);

    close(fd);

    if (!status) goto gmcn_error;

    result->backend = g_file_content_new(result->storage);
    if (result->backend == NULL) goto gmcn_error;

    return G_BIN_CONTENT(result);

 gmcn_error:

    g_object_unref(G_OBJECT(result));

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : context = contexte pour les recherches XPath.                *
*                path    = chemin d'accès au noeud XML à lire.                *
*                base    = référence au lieu d'enregistrement du projet.      *
*                                                                             *
*  Description : Charge des données à laisser en mémoire à partir d'XML.      *
*                                                                             *
*  Retour      : Adresse de la représentation ou NULL en cas d'échec.         *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GBinContent *g_memory_content_new_from_xml(xmlXPathContextPtr context, const char *path, const char *base)
{
    GBinContent *result;                    /* Adresse à retourner         */
    char *access;                           /* Chemin pour une sous-config.*/
    char *encoded;                          /* Données encodées à charger  */
    guchar *data;                           /* Données brutes à charger    */
    gsize size;                             /* Quantité de ces données     */

    result = NULL;

    /* Chemin du fichier à retrouver */

    access = strdup(path);
    access = stradd(access, "/Data");

    encoded = get_node_text_value(context, access);

    free(access);

    /* Chargement */

    if (encoded != NULL)
    {
        data = g_base64_decode(encoded, &size);

        free(encoded);

        if (data != NULL)
        {
            result = g_memory_content_new(data, size);
            g_free(data);
        }

    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à consulter.                       *
*                                                                             *
*  Description : Donne l'origine d'un contenu binaire.                        *
*                                                                             *
*  Retour      : Contenu à l'origine du contenu courant.                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static GBinContent *g_memory_content_get_root(GMemoryContent *content)
{
    GBinContent *result;                    /* Contenu en place à renvoyer */

    result = G_BIN_CONTENT(content);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à consulter.                       *
*                full    = précise s'il s'agit d'une version longue ou non.   *
*                                                                             *
*  Description : Fournit le nom associé au contenu binaire.                   *
*                                                                             *
*  Retour      : Nom de fichier avec chemin absolu au besoin.                 *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static char *g_memory_content_describe(const GMemoryContent *content, bool full)
{
    char *result;                           /* Description à retourner     */

    result = strdup("In-memory content");

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à traiter.                         *
*                xdoc    = structure XML en cours d'édition.                  *
*                context = contexte à utiliser pour les recherches.           *
*                path    = chemin d'accès réservé au binaire.                 *
*                base    = référence au lieu d'enregistrement du projet.      *
*                                                                             *
*  Description : Ecrit une sauvegarde de contenu binaire dans un fichier XML. *
*                                                                             *
*  Retour      : true si l'opération a bien tourné, false sinon.              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_save(const GMemoryContent *content, xmlDocPtr xdoc, xmlXPathContextPtr context, const char *path, const char *base)
{
    bool result;                            /* Bilan à faire remonter      */
    char *access;                           /* Chemin d'accès à un élément */
    vmpa2t start;                           /* Tête de lecture initiale    */
    phys_t length;                          /* Nombre d'octets disponibles */
    const bin_t *data;                      /* Données brutes à sauvegarder*/
    gchar *encoded;                         /* Données encodées à écrire   */

    /* Type */

    result = add_string_attribute_to_node(xdoc, context, path, "type", "memory");
    if (!result) goto gmcs_exit;

    /* Données en mémoire associées */

    access = strdup(path);
    access = stradd(access, "/Data");

    init_vmpa(&start, 0, VMPA_NO_VIRTUAL);

    length = g_binary_content_compute_size(content->backend);

    data = g_binary_content_get_raw_access(content->backend, &start, length);
    assert(data != NULL);

    encoded = g_base64_encode((const guchar *)data, length);
    assert(encoded != NULL);

    result = add_content_to_node(xdoc, context, access, encoded);

    g_free(encoded);
    free(access);

 gmcs_exit:

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content  = contenu binaire à venir lire.                     *
*                checksum = empreinte de zone mémoire à compléter.            *
*                                                                             *
*  Description : Calcule une empreinte unique (SHA256) pour les données.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_compute_checksum(GMemoryContent *content, GChecksum *checksum)
{
    GBinContentIface *iface;                /* Interface utilisée          */

    iface = G_BIN_CONTENT_GET_IFACE(content->backend);

    iface->compute_checksum(content->backend, checksum);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                                                                             *
*  Description : Détermine le nombre d'octets lisibles.                       *
*                                                                             *
*  Retour      : Quantité représentée.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static phys_t g_memory_content_compute_size(const GMemoryContent *content)
{
    phys_t result;                          /* Quantité trouvée à retourner*/

    result = g_binary_content_compute_size(content->backend);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                pos     = position initiale. [OUT]                           *
*                                                                             *
*  Description : Détermine la position initiale d'un contenu.                 *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_compute_start_pos(const GMemoryContent *content, vmpa2t *pos)
{
    g_binary_content_compute_start_pos(content->backend, pos);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                pos     = position finale (exclusive). [OUT]                 *
*                                                                             *
*  Description : Détermine la position finale d'un contenu.                   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_memory_content_compute_end_pos(const GMemoryContent *content, vmpa2t *pos)
{
    g_binary_content_compute_end_pos(content->backend, pos);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                length  = quantité d'octets à provisionner.                  *
*                                                                             *
*  Description : Avance la tête de lecture d'une certaine quantité de données.*
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_seek(const GMemoryContent *content, vmpa2t *addr, phys_t length)
{
    bool result;                            /* Bilan à retourner           */

    result = g_binary_content_seek(content->backend, addr, length);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                length  = quantité d'octets à lire.                          *
*                                                                             *
*  Description : Donne accès à une portion des données représentées.          *
*                                                                             *
*  Retour      : Pointeur vers les données à lire ou NULL en cas d'échec.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static const bin_t *g_memory_content_get_raw_access(const GMemoryContent *content, vmpa2t *addr, phys_t length)
{
    const bin_t *result;                    /* Données utiles à renvoyer   */

    result = g_binary_content_get_raw_access(content->backend, addr, length);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                length  = quantité d'octets à lire.                          *
*                out     = réceptacle disponible pour ces données. [OUT]      *
*                                                                             *
*  Description : Fournit une portion des données représentées.                *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_raw(const GMemoryContent *content, vmpa2t *addr, phys_t length, bin_t *out)
{
    bool result;                            /* Bilan à remonter            */

    result = g_binary_content_read_raw(content->backend, addr, length, out);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                low     = position éventuelle des 4 bits visés. [OUT]        *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre non signé sur quatre bits.                     *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_u4(const GMemoryContent *content, vmpa2t *addr, bool *low, uint8_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_u4(content->backend, addr, low, val);

    return result;

}



/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre non signé sur un octet.                        *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_u8(const GMemoryContent *content, vmpa2t *addr, uint8_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_u8(content->backend, addr, val);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                endian  = ordre des bits dans la source.                     *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre non signé sur deux octets.                     *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_u16(const GMemoryContent *content, vmpa2t *addr, SourceEndian endian, uint16_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_u16(content->backend, addr, endian, val);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                endian  = ordre des bits dans la source.                     *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre non signé sur quatre octets.                   *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_u32(const GMemoryContent *content, vmpa2t *addr, SourceEndian endian, uint32_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_u32(content->backend, addr, endian, val);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                endian  = ordre des bits dans la source.                     *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre non signé sur huit octets.                     *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_u64(const GMemoryContent *content, vmpa2t *addr, SourceEndian endian, uint64_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_u64(content->backend, addr, endian, val);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre non signé encodé au format LEB128.             *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_uleb128(const GMemoryContent *content, vmpa2t *addr, uleb128_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_uleb128(content->backend, addr, val);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir lire.                      *
*                addr    = position de la tête de lecture.                    *
*                val     = lieu d'enregistrement de la lecture. [OUT]         *
*                                                                             *
*  Description : Lit un nombre signé encodé au format LEB128.                 *
*                                                                             *
*  Retour      : Bilan de l'opération : true en cas de succès, false sinon.   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_memory_content_read_leb128(const GMemoryContent *content, vmpa2t *addr, leb128_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */

    result = g_binary_content_read_leb128(content->backend, addr, val);

    return result;

}
