
/* Chrysalide - Outil d'analyse de fichiers binaires
 * file.c - chargement de données binaires à partir d'un fichier
 *
 * Copyright (C) 2015-2019 Cyrille Bagard
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


#include "file.h"


#include <fcntl.h>
#include <malloc.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>


#include "../content-int.h"
#include "../../common/extstr.h"
#include "../../common/pathname.h"
#include "../../core/logs.h"



/* Contenu de données binaires issues d'un fichier (instance) */
struct _GFileContent
{
    GObject parent;                         /* A laisser en premier        */

    GContentAttributes *attribs;            /* Attributs liés au contenu   */

    char *filename;                         /* Fichier chargé en mémoire   */

    bin_t *data;                            /* Contenu binaire représenté  */
    mrange_t range;                         /* Couverture du binaire       */

};

/* Contenu de données binaires issues d'un fichier (classe) */
struct _GFileContentClass
{
    GObjectClass parent;                    /* A laisser en premier        */

};


/* Initialise la classe des contenus de données binaires. */
static void g_file_content_class_init(GFileContentClass *);

/* Initialise une instance de contenu de données binaires. */
static void g_file_content_init(GFileContent *);

/* Procède à l'initialisation de l'interface de lecture. */
static void g_file_content_interface_init(GBinContentInterface *);

/* Supprime toutes les références externes. */
static void g_file_content_dispose(GFileContent *);

/* Procède à la libération totale de la mémoire. */
static void g_file_content_finalize(GFileContent *);

/* Associe un ensemble d'attributs au contenu binaire. */
static void g_file_content_set_attributes(GFileContent *, GContentAttributes *);

/* Fournit l'ensemble des attributs associés à un contenu. */
static GContentAttributes *g_file_content_get_attributes(const GFileContent *);

/* Donne l'origine d'un contenu binaire. */
static GBinContent *g_file_content_get_root(GFileContent *);

/* Fournit le nom associé au contenu binaire. */
static char *g_file_content_describe(const GFileContent *, bool);

/* Ecrit une sauvegarde de contenu binaire dans un fichier XML. */
static bool g_file_content_save(const GFileContent *, xmlDocPtr, xmlXPathContextPtr, const char *, const char *);

/* Fournit une empreinte unique (SHA256) pour les données. */
static void g_file_content_compute_checksum(GFileContent *, GChecksum *);

/* Détermine le nombre d'octets lisibles. */
static phys_t g_file_content_compute_size(const GFileContent *);

/* Détermine la position initiale d'un contenu. */
static void g_file_content_compute_start_pos(const GFileContent *, vmpa2t *);

/* Détermine la position finale d'un contenu. */
static void g_file_content_compute_end_pos(const GFileContent *, vmpa2t *);

/* Avance la tête de lecture d'une certaine quantité de données. */
static bool g_file_content_seek(const GFileContent *, vmpa2t *, phys_t);

/* Donne accès à une portion des données représentées. */
static const bin_t *g_file_content_get_raw_access(const GFileContent *, vmpa2t *, phys_t);

/* Fournit une portion des données représentées. */
static bool g_file_content_read_raw(const GFileContent *, vmpa2t *, phys_t, bin_t *);

/* Lit un nombre non signé sur quatre bits. */
static bool g_file_content_read_u4(const GFileContent *, vmpa2t *, bool *, uint8_t *);

/* Lit un nombre non signé sur un octet. */
static bool g_file_content_read_u8(const GFileContent *, vmpa2t *, uint8_t *);

/* Lit un nombre non signé sur deux octets. */
static bool g_file_content_read_u16(const GFileContent *, vmpa2t *, SourceEndian, uint16_t *);

/* Lit un nombre non signé sur quatre octets. */
static bool g_file_content_read_u32(const GFileContent *, vmpa2t *, SourceEndian, uint32_t *);

/* Lit un nombre non signé sur huit octets. */
static bool g_file_content_read_u64(const GFileContent *, vmpa2t *, SourceEndian, uint64_t *);

/* Lit un nombre non signé encodé au format LEB128. */
static bool g_file_content_read_uleb128(const GFileContent *, vmpa2t *, uleb128_t *);

/* Lit un nombre signé encodé au format LEB128. */
static bool g_file_content_read_leb128(const GFileContent *, vmpa2t *, leb128_t *);



/* Indique le type défini par la GLib pour les contenus de données. */
G_DEFINE_TYPE_WITH_CODE(GFileContent, g_file_content, G_TYPE_OBJECT,
                        G_IMPLEMENT_INTERFACE(G_TYPE_BIN_CONTENT, g_file_content_interface_init));


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des contenus de données binaires.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_file_content_class_init(GFileContentClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_file_content_dispose;
    object->finalize = (GObjectFinalizeFunc)g_file_content_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance de contenu de données binaires.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_file_content_init(GFileContent *content)
{
    GContentAttributes *empty;              /* Jeu d'attributs vide        */
    vmpa2t dummy;                           /* Localisation nulle          */

    content->attribs = NULL;

    empty = g_content_attributes_new("");

    g_binary_content_set_attributes(G_BIN_CONTENT(content), empty);

    content->filename = NULL;
    content->data = NULL;

    init_vmpa(&dummy, VMPA_NO_PHYSICAL, VMPA_NO_VIRTUAL);
    init_mrange(&content->range, &dummy, 0);

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

static void g_file_content_interface_init(GBinContentInterface *iface)
{
    iface->set_attribs = (set_content_attributes)g_file_content_set_attributes;
    iface->get_attribs = (get_content_attributes)g_file_content_get_attributes;

    iface->get_root = (get_content_root_fc)g_file_content_get_root;

    iface->describe = (describe_content_fc)g_file_content_describe;

    iface->save = (save_content_fc)g_file_content_save;

    iface->compute_checksum = (compute_checksum_fc)g_file_content_compute_checksum;

    iface->compute_size = (compute_size_fc)g_file_content_compute_size;
    iface->compute_start_pos = (compute_start_pos_fc)g_file_content_compute_start_pos;
    iface->compute_end_pos = (compute_end_pos_fc)g_file_content_compute_end_pos;

    iface->seek = (seek_fc)g_file_content_seek;

    iface->get_raw_access = (get_raw_access_fc)g_file_content_get_raw_access;

    iface->read_raw = (read_raw_fc)g_file_content_read_raw;
    iface->read_u4 = (read_u4_fc)g_file_content_read_u4;
    iface->read_u8 = (read_u8_fc)g_file_content_read_u8;
    iface->read_u16 = (read_u16_fc)g_file_content_read_u16;
    iface->read_u32 = (read_u32_fc)g_file_content_read_u32;
    iface->read_u64 = (read_u64_fc)g_file_content_read_u64;

    iface->read_uleb128 = (read_uleb128_fc)g_file_content_read_uleb128;
    iface->read_leb128 = (read_leb128_fc)g_file_content_read_leb128;

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

static void g_file_content_dispose(GFileContent *content)
{
    g_clear_object(&content->attribs);

    G_OBJECT_CLASS(g_file_content_parent_class)->dispose(G_OBJECT(content));

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

static void g_file_content_finalize(GFileContent *content)
{
    free(content->filename);

    if (content->data != NULL)
        free(content->data);

    G_OBJECT_CLASS(g_file_content_parent_class)->finalize(G_OBJECT(content));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : filename = chemin d'accès au fichier à charger.              *
*                                                                             *
*  Description : Charge en mémoire le contenu d'un fichier donné.             *
*                                                                             *
*  Retour      : Représentation de contenu à manipuler ou NULL en cas d'échec.*
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GBinContent *g_file_content_new(const char *filename)
{
    GFileContent *result;                   /* Structure à retourner       */
    int fd;                                 /* Descripteur du fichier      */
    struct stat info;                       /* Informations sur le fichier */
    int ret;                                /* Bilan d'un appel            */
    void *content;                          /* Contenu brut du fichier     */
    vmpa2t base;                            /* Localisation des données    */

    /* Récupération des données */

    fd = open(filename, O_RDONLY);
    if (fd == -1)
    {
        LOG_ERROR_N("open");
        goto gbcnff_error;
    }

    ret = fstat(fd, &info);
    if (ret == -1)
    {
        close(fd);
        LOG_ERROR_N("fstat");
        goto gbcnff_error;
    }

    content = mmap(NULL, info.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (content == MAP_FAILED)
    {
        close(fd);
        LOG_ERROR_N("mmap");
        goto gbcnff_error;
    }

    /* Constitution du contenu officiel */

    result = g_object_new(G_TYPE_FILE_CONTENT, NULL);

    result->filename = strdup(filename);

    result->data = (bin_t *)malloc(info.st_size);
    memcpy(result->data, content, info.st_size);

    munmap(content, info.st_size);
    close(fd);

    init_vmpa(&base, 0, VMPA_NO_VIRTUAL);
    init_mrange(&result->range, &base, info.st_size);

    return G_BIN_CONTENT(result);

 gbcnff_error:

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : context = contexte pour les recherches XPath.                *
*                path    = chemin d'accès au noeud XML à lire.                *
*                base    = référence au lieu d'enregistrement du projet.      *
*                                                                             *
*  Description : Charge en mémoire le contenu d'un fichier à partir d'XML.    *
*                                                                             *
*  Retour      : Adresse de la représentation ou NULL en cas d'échec.         *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GBinContent *g_file_content_new_from_xml(xmlXPathContextPtr context, const char *path, const char *base)
{
    GBinContent *result;                    /* Adresse à retourner         */
    char *access;                           /* Chemin pour une sous-config.*/
    char *filename;                         /* Chemin du binaire à charger */
    char *absolute;                         /* Chemin absolu final         */

    result = NULL;

    /* Chemin du fichier à retrouver */

    access = strdup(path);
    access = stradd(access, "/Filename");

    filename = get_node_text_value(context, access);

    free(access);

    /* Chargement */

    if (filename != NULL)
    {
        absolute = build_absolute_filename(base, filename);

        free(filename);

        if (absolute != NULL)
        {
            result = g_file_content_new(absolute);
            free(absolute);
        }

    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à actualiser.                      *
*                attribs = jeu d'attributs à lier au contenu courant.         *
*                                                                             *
*  Description : Associe un ensemble d'attributs au contenu binaire.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_file_content_set_attributes(GFileContent *content, GContentAttributes *attribs)
{
    content->attribs = attribs;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à consulter.                       *
*                                                                             *
*  Description : Fournit l'ensemble des attributs associés à un contenu.      *
*                                                                             *
*  Retour      : Jeu d'attributs liés au contenu courant.                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static GContentAttributes *g_file_content_get_attributes(const GFileContent *content)
{
    GContentAttributes *result;             /* Instance à retourner        */

    result = content->attribs;

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

static GBinContent *g_file_content_get_root(GFileContent *content)
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

static char *g_file_content_describe(const GFileContent *content, bool full)
{
    char *result;                           /* Description à retourner     */
    const char *sep;                        /* Caractère de séparation     */

    if (full)
        result = strdup(content->filename);

    else
    {
        sep = strrchr(content->filename, G_DIR_SEPARATOR);

        if (sep == NULL)
            result = strdup(content->filename);

        else
            result = strdup(++sep);

    }

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

static bool g_file_content_save(const GFileContent *content, xmlDocPtr xdoc, xmlXPathContextPtr context, const char *path, const char *base)
{
    bool result;                            /* Bilan à faire remonter      */
    char *access;                           /* Chemin d'accès à un élément */
    char *relative;                         /* Chemin d'accès relatif      */

    /* Type */

    result = add_string_attribute_to_node(xdoc, context, path, "type", "file");
    if (!result) goto gfcs_exit;

    /* Nom du fichier associé */

    access = strdup(path);
    access = stradd(access, "/Filename");

    relative = build_relative_filename(base, content->filename);

    result = add_content_to_node(xdoc, context, access, relative);

    free(relative);
    free(access);

 gfcs_exit:

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

static void g_file_content_compute_checksum(GFileContent *content, GChecksum *checksum)
{
    g_checksum_update(checksum, content->data, get_mrange_length(&content->range));

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

static phys_t g_file_content_compute_size(const GFileContent *content)
{
    phys_t result;                          /* Quantité trouvée à retourner*/

    result = get_mrange_length(&content->range);

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

static void g_file_content_compute_start_pos(const GFileContent *content, vmpa2t *pos)
{
    copy_vmpa(pos, get_mrange_addr(&content->range));

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

static void g_file_content_compute_end_pos(const GFileContent *content, vmpa2t *pos)
{
    compute_mrange_end_addr(&content->range, pos);

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

static bool g_file_content_seek(const GFileContent *content, vmpa2t *addr, phys_t length)
{
    bool result;                            /* Bilan à retourner           */
    phys_t offset;                          /* Emplacement de départ       */

    result = false;

    offset = get_phy_addr(addr);

    if (length > get_mrange_length(&content->range))
        goto gfcs_done;

    if (offset > (get_mrange_length(&content->range) - length))
        goto gfcs_done;

    advance_vmpa(addr, length);

    result = true;

 gfcs_done:

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

static const bin_t *g_file_content_get_raw_access(const GFileContent *content, vmpa2t *addr, phys_t length)
{
    const bin_t *result;                    /* Données utiles à renvoyer   */
    phys_t offset;                          /* Emplacement de départ       */
    bool allowed;                           /* Capacité d'avancer ?        */

    offset = get_phy_addr(addr);

    allowed = g_file_content_seek(content, addr, length);

    result = (allowed ? &content->data[offset] : NULL);

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

static bool g_file_content_read_raw(const GFileContent *content, vmpa2t *addr, phys_t length, bin_t *out)
{
    bool result;                            /* Bilan à remonter            */
    const bin_t *data;                      /* Pointeur vers données utiles*/

    data = g_file_content_get_raw_access(content, addr, length);

    if (data != NULL)
    {
        result = true;
        memcpy(out, data, length);
    }
    else
        result = false;

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

static bool g_file_content_read_u4(const GFileContent *content, vmpa2t *addr, bool *low, uint8_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_u4(val, content->data, &pos, length, low);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

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

static bool g_file_content_read_u8(const GFileContent *content, vmpa2t *addr, uint8_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_u8(val, content->data, &pos, length);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

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

static bool g_file_content_read_u16(const GFileContent *content, vmpa2t *addr, SourceEndian endian, uint16_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_u16(val, content->data, &pos, length, endian);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

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

static bool g_file_content_read_u32(const GFileContent *content, vmpa2t *addr, SourceEndian endian, uint32_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_u32(val, content->data, &pos, length, endian);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

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

static bool g_file_content_read_u64(const GFileContent *content, vmpa2t *addr, SourceEndian endian, uint64_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_u64(val, content->data, &pos, length, endian);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

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

static bool g_file_content_read_uleb128(const GFileContent *content, vmpa2t *addr, uleb128_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_uleb128(val, content->data, &pos, length);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

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

static bool g_file_content_read_leb128(const GFileContent *content, vmpa2t *addr, leb128_t *val)
{
    bool result;                            /* Bilan de lecture à renvoyer */
    phys_t pos;                             /* Tête de lecture courante    */
    phys_t length;                          /* Taille de la surface dispo. */

    pos = get_phy_addr(addr);

    if (pos == VMPA_NO_PHYSICAL)
        return false;

    length = get_mrange_length(&content->range);

    result = read_leb128(val, content->data, &pos, length);

    if (result)
        advance_vmpa(addr, pos - get_phy_addr(addr));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu binaire à venir consulter.                 *
*                                                                             *
*  Description : Fournit le nom de fichier associé au contenu binaire.        *
*                                                                             *
*  Retour      : Chemin d'accès au contenu binaire.                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

const char *g_file_content_get_filename(const GFileContent *content)
{
    char *result;                           /* Chemin d'accès à retourner  */

    result = content->filename;

    return result;

}
