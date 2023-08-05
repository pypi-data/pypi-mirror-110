
/* Chrysalide - Outil d'analyse de fichiers binaires
 * pool.c - opérandes pointant vers la table des constantes
 *
 * Copyright (C) 2017-2020 Cyrille Bagard
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


#include "pool.h"


#include <stdio.h>
#include <string.h>


#include <i18n.h>


#include <arch/operand-int.h>
#include <arch/operands/targetable-int.h>
#include <common/sort.h>
#include <gtkext/gtkblockdisplay.h>
#include <plugins/dex/pool.h>



/* Définition d'un opérande visant un élément de table de constantes Dalvik (instance) */
struct _GDalvikPoolOperand
{
    GArchOperand parent;                    /* Instance parente            */

    GDexFormat *format;                     /* Lien vers le contenu réel   */
    DalvikPoolType type;                    /* Type de table visée         */
    uint32_t index;                         /* Indice de l'élément visé    */

};


/* Définition d'un opérande visant un élément de table de constantes Dalvik (classe) */
struct _GDalvikPoolOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des opérandes de constante Dalvik. */
static void g_dalvik_pool_operand_class_init(GDalvikPoolOperandClass *);

/* Initialise une instance d'opérande de constante Dalvik. */
static void g_dalvik_pool_operand_init(GDalvikPoolOperand *);

/* Procède à l'initialisation de l'interface de ciblage. */
static void g_dalvik_pool_operand_targetable_interface_init(GTargetableOperandInterface *);

/* Supprime toutes les références externes. */
static void g_dalvik_pool_operand_dispose(GDalvikPoolOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_dalvik_pool_operand_finalize(GDalvikPoolOperand *);

/* Compare un opérande avec un autre. */
static int g_dalvik_pool_operand_compare(const GDalvikPoolOperand *, const GDalvikPoolOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_dalvik_pool_operand_print(const GDalvikPoolOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_dalvik_pool_operand_unserialize(GDalvikPoolOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_dalvik_pool_operand_serialize(const GDalvikPoolOperand *, GAsmStorage *, packed_buffer_t *);



/* ----------------------- INTERFACE DE CIBLAGE POUR OPERANDE ----------------------- */


/* Obtient l'adresse de la cible visée par un opérande. */
static bool g_dalvik_pool_operand_get_addr(const GDalvikPoolOperand *, const vmpa2t *, GBinFormat *, GArchProcessor *, vmpa2t *);



/* Indique le type défini par la GLib pour un un élément de table de constantes Dalvik. */
G_DEFINE_TYPE_WITH_CODE(GDalvikPoolOperand, g_dalvik_pool_operand, G_TYPE_ARCH_OPERAND,
                        G_IMPLEMENT_INTERFACE(G_TYPE_TARGETABLE_OPERAND, g_dalvik_pool_operand_targetable_interface_init));


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des opérandes de constante Dalvik.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_dalvik_pool_operand_class_init(GDalvikPoolOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_dalvik_pool_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_dalvik_pool_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->compare = (operand_compare_fc)g_dalvik_pool_operand_compare;
    operand->print = (operand_print_fc)g_dalvik_pool_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_dalvik_pool_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_dalvik_pool_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'opérande de constante Dalvik.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_dalvik_pool_operand_init(GDalvikPoolOperand *operand)
{
    operand->format = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de ciblage.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_dalvik_pool_operand_targetable_interface_init(GTargetableOperandInterface *iface)
{
    iface->get_addr = (get_targetable_addr_fc)g_dalvik_pool_operand_get_addr;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : binary = instance d'objet GLib à traiter.                    *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_dalvik_pool_operand_dispose(GDalvikPoolOperand *operand)
{
    if (operand->format != NULL)
        g_object_unref(G_OBJECT(operand->format));

    G_OBJECT_CLASS(g_dalvik_pool_operand_parent_class)->dispose(G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : binary = instance d'objet GLib à traiter.                    *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_dalvik_pool_operand_finalize(GDalvikPoolOperand *operand)
{
    G_OBJECT_CLASS(g_dalvik_pool_operand_parent_class)->finalize(G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : a = premier opérande à consulter.                            *
*                b = second opérande à consulter.                             *
*                                                                             *
*  Description : Compare un opérande avec un autre.                           *
*                                                                             *
*  Retour      : Bilan de la comparaison.                                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static int g_dalvik_pool_operand_compare(const GDalvikPoolOperand *a, const GDalvikPoolOperand *b)
{
    int result;                             /* Bilan à renvoyer            */

    result = sort_unsigned_long((unsigned long)a->format, (unsigned long)b->format);

    if (result == 0)
        result = sort_unsigned_long(a->type, b->type);

    if (result == 0)
        result = sort_unsigned_long(a->index, b->index);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à traiter.                                *
*                line    = ligne tampon où imprimer l'opérande donné.         *
*                                                                             *
*  Description : Traduit un opérande en version humainement lisible.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_dalvik_pool_operand_print(const GDalvikPoolOperand *operand, GBufferLine *line)
{
    GDexPool *pool;                         /* Table de ressources         */
    const char *string;                     /* Chaîne de caractères #1     */
    GDataType *type;                        /* Type à représenter          */
    size_t len;                             /* Taille du texte à créer     */
    char *tmp;                              /* Chaîne de caractères #2     */
    GBinRoutine *routine;                   /* Routine à représenter       */
    GBinVariable *field;                    /* Champ à représenter         */
    GDexMethod *method;                     /* Méthode à retrouver         */

    pool = g_dex_format_get_pool(operand->format);

    switch (operand->type)
    {
        case DPT_NONE:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "????", 4, RTT_ERROR, NULL);
            break;

        case DPT_STRING:

            string = g_dex_pool_get_string(pool, operand->index, NULL, NULL);

            if (string != NULL)
            {
                g_buffer_line_append_text(line, DLC_ASSEMBLY, "\"", 1, RTT_STRING, NULL);

                len = strlen(string);

                if (len > 0)
                    g_buffer_line_append_text(line, DLC_ASSEMBLY, string, len, RTT_STRING, NULL);

                g_buffer_line_append_text(line, DLC_ASSEMBLY, "\"", 1, RTT_STRING, NULL);

            }
            else
            {
                len = strlen(_("<bad string index (%d)>")) + 10 /* 4294967295U */ + 1;
                tmp = calloc(len, sizeof(char));
                snprintf(tmp, len, _("<bad string index (%d)>"), operand->index);

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, len - 1, RTT_ERROR, NULL);

                free(tmp);

            }

            break;

        case DPT_TYPE:

            type = g_dex_pool_get_type_(pool, operand->index);

            if (type != NULL)
            {
                tmp = g_data_type_to_string(type, true);
                g_object_unref(G_OBJECT(type));

                g_buffer_line_append_text(line, DLC_ASSEMBLY, "<", 1, RTT_HOOK, NULL);
                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, strlen(tmp), RTT_VAR_NAME, NULL);
                g_buffer_line_append_text(line, DLC_ASSEMBLY, ">", 1, RTT_HOOK, NULL);

            }
            else
            {
                len = strlen(_("<bad type index (%d)>")) + 10 /* 4294967295U */ + 1;
                tmp = calloc(len, sizeof(char));
                snprintf(tmp, len, _("<bad type index (%d)>"), operand->index);

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, len - 1, RTT_ERROR, NULL);

            }

            free(tmp);

            break;

        case DPT_PROTO:

            routine = g_dex_pool_get_prototype(pool, operand->index);

            if (routine != NULL)
            {
                tmp = g_binary_symbol_get_label(G_BIN_SYMBOL(routine));
                g_object_unref(G_OBJECT(routine));

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, strlen(tmp), RTT_LABEL, G_OBJECT(operand));

            }
            else
            {
                len = strlen(_("<bad prototype index (%d)>")) + 10 /* 4294967295U */ + 1;
                tmp = calloc(len, sizeof(char));
                snprintf(tmp, len, _("<bad prototype index (%d)>"), operand->index);

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, len - 1, RTT_ERROR, NULL);

            }

            free(tmp);

            break;

        case DPT_FIELD:

            field = g_dex_pool_get_field(pool, operand->index);

            if (field != NULL)
            {
                tmp = g_binary_variable_to_string(field, true);
                g_object_unref(G_OBJECT(field));

                g_buffer_line_append_text(line, DLC_ASSEMBLY, "<", 1, RTT_HOOK, NULL);
                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, strlen(tmp), RTT_VAR_NAME, NULL);
                g_buffer_line_append_text(line, DLC_ASSEMBLY, ">", 1, RTT_HOOK, NULL);

            }
            else
            {
                len = strlen(_("<bad field index (%d)>")) + 10 /* 4294967295U */ + 1;
                tmp = calloc(len, sizeof(char));
                snprintf(tmp, len, _("<bad field index (%d)>"), operand->index);

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, len - 1, RTT_ERROR, NULL);

            }

            free(tmp);

            break;

        case DPT_METHOD:

            method = g_dex_pool_get_method(pool, operand->index);

            if (method != NULL)
                routine = g_dex_method_get_routine(method);
            else
                routine = NULL;

            if (routine != NULL)
            {
                tmp = g_binary_symbol_get_label(G_BIN_SYMBOL(routine));
                g_object_unref(G_OBJECT(routine));

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, strlen(tmp), RTT_LABEL, G_OBJECT(operand));

            }
            else
            {
                len = strlen(_("<bad method index (%d)>")) + 10 /* 4294967295U */ + 1;
                tmp = calloc(len, sizeof(char));
                snprintf(tmp, len, _("<bad method index (%d)>"), operand->index);

                g_buffer_line_append_text(line, DLC_ASSEMBLY, tmp, len - 1, RTT_ERROR, NULL);

            }

            free(tmp);

            if (method != NULL)
                g_object_unref(G_OBJECT(method));

            break;

    }

    g_object_unref(G_OBJECT(pool));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : format  = format du fichier contenant le code.               *
*                type    = type de table visée avec la référence.             *
*                content = flux de données à analyser.                        *
*                pos     = position courante dans ce flux. [OUT]              *
*                size    = taille de l'opérande, et donc du registre.         *
*                endian  = ordre des bits dans la source.                     *
*                                                                             *
*  Description : Crée un opérande visant un élément constant Dalvik.          *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_dalvik_pool_operand_new(GDexFormat *format, DalvikPoolType type, const GBinContent *content, vmpa2t *pos, MemoryDataSize size, SourceEndian endian)
{
    GDalvikPoolOperand *result;             /* Structure à retourner       */
    uint16_t index16;                       /* Indice sur 16 bits          */
    uint32_t index32;                       /* Indice sur 32 bits          */
    bool test;                              /* Bilan de lecture            */

    switch (size)
    {
        case MDS_16_BITS:
            test = g_binary_content_read_u16(content, pos, endian, &index16);
            break;
        case MDS_32_BITS:
            test = g_binary_content_read_u32(content, pos, endian, &index32);
            break;
        default:
            test = false;
            break;
    }

    if (!test)
        goto gdpon_exit;

    result = g_object_new(G_TYPE_DALVIK_POOL_OPERAND, NULL);

    g_object_ref(G_OBJECT(format));

    result->format = format;
    result->type = type;
    result->index = (size == MDS_16_BITS ? index16 : index32);

    return G_ARCH_OPERAND(result);

 gdpon_exit:

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique la nature de la table de constantes visée ici.       *
*                                                                             *
*  Retour      : Type de table constantes visée.                              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

DalvikPoolType g_dalvik_pool_operand_get_pool_type(const GDalvikPoolOperand *operand)
{
    return operand->type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique l'indice de l'élément dans la table de constantes.   *
*                                                                             *
*  Retour      : Indice de l'élément visé dans la table de constantes.        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

uint32_t g_dalvik_pool_operand_get_index(const GDalvikPoolOperand *operand)
{
    return operand->index;

}



/* ---------------------------------------------------------------------------------- */
/*                       TRANSPOSITIONS VIA CACHE DES OPERANDES                       */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande d'assemblage à constituer.                *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                format  = format binaire chargé associé à l'architecture.    *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Charge un opérande depuis une mémoire tampon.                *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_dalvik_pool_operand_unserialize(GDalvikPoolOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */

    parent = G_ARCH_OPERAND_CLASS(g_dalvik_pool_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
    {
        operand->format = G_DEX_FORMAT(format);
        g_object_ref(G_OBJECT(format));
    }

    if (result)
        result = extract_packed_buffer(pbuf, &operand->type, sizeof(DalvikPoolType), true);

    if (result)
        result = extract_packed_buffer(pbuf, &operand->index, sizeof(uint32_t), true);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande d'assemblage à consulter.                 *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Sauvegarde un opérande dans une mémoire tampon.              *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_dalvik_pool_operand_serialize(const GDalvikPoolOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */

    parent = G_ARCH_OPERAND_CLASS(g_dalvik_pool_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
        result = extend_packed_buffer(pbuf, &operand->type, sizeof(DalvikPoolType), true);

    if (result)
        result = extend_packed_buffer(pbuf, &operand->index, sizeof(uint32_t), true);

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                         INTERFACE DE CIBLAGE POUR OPERANDE                         */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = operande à consulter.                              *
*                src     = localisation de l'instruction mère.                *
*                format  = format reconnu pour le binaire chargé.             *
*                proc    = architecture associée à ce même binaire.           *
*                addr    = localisation de la cible. [OUT]                    *
*                                                                             *
*  Description : Obtient l'adresse de la cible visée par un opérande.         *
*                                                                             *
*  Retour      : true si la cible est valide, false sinon.                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_dalvik_pool_operand_get_addr(const GDalvikPoolOperand *operand, const vmpa2t *src, GBinFormat *format, GArchProcessor *proc, vmpa2t *addr)
{
    bool result;                            /* Bilan à retourner           */
    GDexPool *pool;                         /* Table de ressources         */
    GDexMethod *method;                     /* Méthode ciblée ici          */
    GBinRoutine *routine;                   /* Routine liée à la méthode   */
    const mrange_t *range;                  /* Zone d'occupation           */

    result = false;

    if (operand->type == DPT_METHOD)
    {
        pool = g_dex_format_get_pool(G_DEX_FORMAT(format));

        method = g_dex_pool_get_method(pool, operand->index);

        g_object_unref(G_OBJECT(pool));

        if (method != NULL)
        {
            routine = g_dex_method_get_routine(method);
            range = g_binary_symbol_get_range(G_BIN_SYMBOL(routine));

            if (range->addr.physical > 0)
            {
                copy_vmpa(addr, get_mrange_addr(range));
                result = true;
            }

            g_object_unref(G_OBJECT(routine));
            g_object_unref(G_OBJECT(method));

        }

    }

    return result;

}
