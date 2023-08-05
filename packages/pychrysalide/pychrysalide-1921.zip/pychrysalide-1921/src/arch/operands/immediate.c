
/* Chrysalide - Outil d'analyse de fichiers binaires
 * immediate.c - opérandes représentant des valeurs numériques
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
 *  along with Chrysalide.  If not, see <http://www.gnu.org/licenses/>.
 */


#include "immediate.h"


#include <assert.h>
#include <ctype.h>
#include <inttypes.h>
#include <limits.h>
#include <malloc.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>


#include <i18n.h>


#include "rename-int.h"
#include "targetable-int.h"
#include "../operand-int.h"
#include "../../common/asm.h"
#include "../../common/extstr.h"
#include "../../core/logs.h"
#include "../../format/format.h"
#include "../../glibext/objhole.h"
#include "../../gtkext/gtkblockdisplay.h"



/* ------------------------- OPERANDE POUR VALEUR IMMEDIATE ------------------------- */


/* Etats particuliers d'un opérande de valeur immédiate */
typedef enum _ImmOpFlag
{
    IOF_ZERO_PADDING_BY_DEFAULT,            /* Bourrage avec 0 par défaut ?*/
    IOF_ZERO_PADDING,                       /* Bourrage avec 0 ?           */

} ImmOpFlag;

/* Informations glissées dans la structure GObject de GArchInstruction */
typedef union _immop_obj_extra
{
    struct
    {
        MemoryDataSize size;                /* Taille de l'opérande        */

        ImmOperandDisplay def_display;      /* Type par défaut d'affichage */
        ImmOperandDisplay display;          /* Format général d'affichage  */
        ImmOpFlag flags;                    /* Informations diverses       */

    };

    gint lock;                              /* Gestion d'accès aux fanions */

} immop_obj_extra;

/* Définition d'un opérande de valeur numérique (instance) */
struct _GImmOperand
{
    GArchOperand parent;                    /* Instance parente            */

    uint64_t raw;                           /* Valeur transtypée           */

#if __SIZEOF_INT__ == __SIZEOF_LONG__

    /**
     * L'inclusion des informations suivantes dépend de l'architecture.
     *
     * Si la structure GObject possède un trou, on remplit de préférence
     * ce dernier.
     */

    immop_obj_extra extra;                  /* Externalisation embarquée   */

#endif

};

/**
 * Accès aux informations éventuellement déportées.
 */

#if __SIZEOF_INT__ == __SIZEOF_LONG__

#   define INIT_IMM_OP_EXTRA(op) op->extra.lock = 0

#   define GET_IMM_OP_EXTRA(op) &op->extra

#else

#   define INIT_IMM_OP_EXTRA(op) INIT_GOBJECT_EXTRA(G_OBJECT(op))

#   define GET_IMM_OP_EXTRA(op) GET_GOBJECT_EXTRA(G_OBJECT(op), immop_obj_extra)

#endif

/* Définition d'un opérande de valeur numérique (classe) */
struct _GImmOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des opérandes de valeur immédiate. */
static void g_imm_operand_class_init(GImmOperandClass *);

/* Initialise un opérande de valeur immédiate. */
static void g_imm_operand_init(GImmOperand *);

/* Procède à l'initialisation de l'interface de ciblage. */
static void g_imm_operand_targetable_interface_init(GTargetableOperandInterface *);

/* Procède à l'initialisation de l'interface de renommage. */
static void g_imm_operand_renameable_interface_init(GRenameableOperandInterface *);

/* Supprime toutes les références externes. */
static void g_imm_operand_dispose(GImmOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_imm_operand_finalize(GImmOperand *);

/* Compare un opérande avec un autre. */
static int g_imm_operand_compare(const GImmOperand *, const GImmOperand *);

/* Construit la chaîne de caractères correspondant à l'opérande. */
static size_t _g_imm_operand_to_string(const GImmOperand *, ImmOperandDisplay, char [IMM_MAX_SIZE]);

/* Traduit un opérande en version humainement lisible. */
static void g_imm_operand_print(const GImmOperand *, GBufferLine *);

/* Construit un petit résumé concis de l'opérande. */
static char *g_imm_operand_build_tooltip(const GImmOperand *, const GLoadedBinary *);

/* Charge un opérande depuis une mémoire tampon. */
static bool g_imm_operand_unserialize(GImmOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_imm_operand_serialize(const GImmOperand *, GAsmStorage *, packed_buffer_t *);

/* Obtient l'adresse de la cible visée par un opérande. */
static bool g_imm_operand_get_addr(const GImmOperand *, const vmpa2t *, GBinFormat *, GArchProcessor *, vmpa2t *);

/* Construit un opérande de représentation alternative. */
static GRenamedOperand *g_imm_operand_build(const GImmOperand *, const char *);



/* ----------------------- REMPLACEMENT DE VALEURS IMMEDIATES ----------------------- */


/* Définition d'un remplacement d'opérande de valeur numérique (instance) */
struct _GKnownImmOperand
{
    GImmOperand parent;                     /* Instance parente            */

    char *alt_text;                         /* Alternative humaine         */

};

/* Définition d'un remplacement d'opérande de valeur numérique (classe) */
struct _GKnownImmOperandClass
{
    GImmOperandClass parent;                /* Classe parente              */

};


/* Initialise la classe des remplacements d'opérandes. */
static void g_known_imm_operand_class_init(GKnownImmOperandClass *);

/* Initialise un remplacement d'opérande de valeur immédiate. */
static void g_known_imm_operand_init(GKnownImmOperand *);

/* Procède à l'initialisation de l'interface de renommage. */
static void g_known_imm_operand_renamed_interface_init(GRenamedOperandInterface *);

/* Supprime toutes les références externes. */
static void g_known_imm_operand_dispose(GKnownImmOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_known_imm_operand_finalize(GKnownImmOperand *);

/* Compare un opérande avec un autre. */
static int g_known_imm_operand_compare(const GKnownImmOperand *, const GKnownImmOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_known_imm_operand_print(const GKnownImmOperand *, GBufferLine *);

/* Charge un opérande depuis une mémoire tampon. */
static bool g_known_imm_operand_unserialize(GKnownImmOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_known_imm_operand_serialize(const GKnownImmOperand *, GAsmStorage *, packed_buffer_t *);

/* Fournit un texte comme représentation alternative d'opérande. */
static const char *g_known_imm_operand_get_text(const GKnownImmOperand *);



/* ---------------------------------------------------------------------------------- */
/*                           OPERANDE POUR VALEUR IMMEDIATE                           */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour un opérande de valeur numérique. */
G_DEFINE_TYPE_WITH_CODE(GImmOperand, g_imm_operand, G_TYPE_ARCH_OPERAND,
                        G_IMPLEMENT_INTERFACE(G_TYPE_TARGETABLE_OPERAND, g_imm_operand_targetable_interface_init)
                        G_IMPLEMENT_INTERFACE(G_TYPE_RENAMEABLE_OPERAND, g_imm_operand_renameable_interface_init));


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des opérandes de valeur immédiate.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_imm_operand_class_init(GImmOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);
    operand = G_ARCH_OPERAND_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_imm_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_imm_operand_finalize;

    operand->compare = (operand_compare_fc)g_imm_operand_compare;
    operand->print = (operand_print_fc)g_imm_operand_print;
    operand->build_tooltip = (operand_build_tooltip_fc)g_imm_operand_build_tooltip;

    operand->unserialize = (unserialize_operand_fc)g_imm_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_imm_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise un opérande de valeur immédiate.                  *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_imm_operand_init(GImmOperand *operand)
{
    operand->raw = 0;

    INIT_IMM_OP_EXTRA(operand);

    GET_IMM_OP_EXTRA(operand)->def_display = IOD_HEX;
    GET_IMM_OP_EXTRA(operand)->display = IOD_COUNT;

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

static void g_imm_operand_targetable_interface_init(GTargetableOperandInterface *iface)
{
    iface->get_addr = (get_targetable_addr_fc)g_imm_operand_get_addr;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de renommage.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_imm_operand_renameable_interface_init(GRenameableOperandInterface *iface)
{
    iface->build = (build_renameable_fc)g_imm_operand_build;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_imm_operand_dispose(GImmOperand *operand)
{
    G_OBJECT_CLASS(g_imm_operand_parent_class)->dispose(G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_imm_operand_finalize(GImmOperand *operand)
{
    G_OBJECT_CLASS(g_imm_operand_parent_class)->finalize(G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : size    = taille de l'opérande souhaitée.                    *
*                content = flux de données à analyser.                        *
*                addr    = position courante dans ce flux. [OUT]              *
*                low     = position éventuelle des 4 bits visés. [OUT]        *
*                endian  = ordre des bits dans la source.                     *
*                                                                             *
*  Description : Crée un opérande réprésentant une valeur numérique.          *
*                                                                             *
*  Retour      : Instruction mise en place.                                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *_g_imm_operand_new_from_data(MemoryDataSize size, const GBinContent *content, vmpa2t *addr, bool *low, SourceEndian endian)
{
    GImmOperand *result;                    /* Opérande à retourner        */
    immop_obj_extra *extra;                 /* Données insérées à modifier */
    uint8_t uval8;                          /* Valeur sur 8 bits           */
    uint16_t uval16;                        /* Valeur sur 16 bits          */
    uint32_t uval32;                        /* Valeur sur 32 bits          */
    uint64_t uval64;                        /* Valeur sur 64 bits          */
    int8_t sval8;                           /* Valeur sur 8 bits           */
    int16_t sval16;                         /* Valeur sur 16 bits          */
    int32_t sval32;                         /* Valeur sur 32 bits          */
    int64_t sval64;                         /* Valeur sur 64 bits          */

    result = g_object_new(G_TYPE_IMM_OPERAND, NULL);

    extra = GET_IMM_OP_EXTRA(result);

    extra->size = size;

    switch (size)
    {
        case MDS_4_BITS_UNSIGNED:
            if (!g_binary_content_read_u4(content, addr, low, &uval8))
                goto gionfd_error;
            result->raw = uval8;
            break;

        case MDS_8_BITS_UNSIGNED:
            if (!g_binary_content_read_u8(content, addr, &uval8))
                goto gionfd_error;
            result->raw = uval8;
            break;

        case MDS_16_BITS_UNSIGNED:
            if (!g_binary_content_read_u16(content, addr, endian, &uval16))
                goto gionfd_error;
            result->raw = uval16;
            break;

        case MDS_32_BITS_UNSIGNED:
            if (!g_binary_content_read_u32(content, addr, endian, &uval32))
                goto gionfd_error;
            result->raw = uval32;
            break;

        case MDS_64_BITS_UNSIGNED:
            if (!g_binary_content_read_u64(content, addr, endian, &uval64))
                goto gionfd_error;
            result->raw = uval64;
            break;

        case MDS_4_BITS_SIGNED:
            if (!g_binary_content_read_s4(content, addr, low, &sval8))
                goto gionfd_error;
            result->raw = sval8;
            break;

        case MDS_8_BITS_SIGNED:
            if (!g_binary_content_read_s8(content, addr, &sval8))
                goto gionfd_error;
            result->raw = sval8;
            break;

        case MDS_16_BITS_SIGNED:
            if (!g_binary_content_read_s16(content, addr, endian, &sval16))
                goto gionfd_error;
            result->raw = sval16;
            break;

        case MDS_32_BITS_SIGNED:
            if (!g_binary_content_read_s32(content, addr, endian, &sval32))
                goto gionfd_error;
            result->raw = sval32;
            break;

        case MDS_64_BITS_SIGNED:
            if (!g_binary_content_read_s64(content, addr, endian, &sval64))
                goto gionfd_error;
            result->raw = sval64;
            break;

        case MDS_UNDEFINED:
            goto gionfd_error;
            break;

    }

    return G_ARCH_OPERAND(result);

 gionfd_error:

    g_object_unref(G_OBJECT(result));

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : size  = taille de l'opérande souhaitée.                      *
*                value = valeur sur x bits à venir récupérer.                 *
*                                                                             *
*  Description : Crée un opérande réprésentant une valeur numérique.          *
*                                                                             *
*  Retour      : Instruction mise en place.                                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_imm_operand_new_from_value(MemoryDataSize size, uint64_t value)
{
    GImmOperand *result;                    /* Opérande à retourner        */
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    if (size == MDS_UNDEFINED)
        result = NULL;

    else
    {
        result = g_object_new(G_TYPE_IMM_OPERAND, NULL);

        extra = GET_IMM_OP_EXTRA(result);

        extra->size = size;

        result->raw = value;

    }

    return (result != NULL ? G_ARCH_OPERAND(result) : NULL);

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

static int g_imm_operand_compare(const GImmOperand *a, const GImmOperand *b)
{
    int result;                             /* Bilan à retourner           */
    immop_obj_extra *ea;                    /* Données insérées à modifier */
    immop_obj_extra *eb;                    /* Données insérées à modifier */

    ea = GET_IMM_OP_EXTRA(a);
    eb = GET_IMM_OP_EXTRA(b);

    g_bit_lock(&ea->lock, HOLE_LOCK_BIT);
    g_bit_lock(&eb->lock, HOLE_LOCK_BIT);

    if (ea->size < eb->size)
    {
        result = -1;
        goto done;
    }
    else if (ea->size > eb->size)
    {
        result = 1;
        goto done;
    }

    if (a->raw < b->raw)
    {
        result = -1;
        goto done;
    }
    else if (a->raw > b->raw)
    {
        result = 1;
        goto done;
    }

    if (ea->def_display < eb->def_display)
    {
        result = -1;
        goto done; 
   }
    else if (ea->def_display > eb->def_display)
    {
        result = 1;
        goto done;
    }

    if (ea->display < eb->display)
    {
        result = -1;
        goto done;
    }
    else if (ea->display > eb->display)
    {
        result = 1;
        goto done;
    }

    if (ea->flags < eb->flags)
    {
        result = -1;
        goto done;
    }
    else if (ea->flags > eb->flags)
    {
        result = 1;
        goto done;
    }

    result = 0;

 done:

    g_bit_unlock(&eb->lock, HOLE_LOCK_BIT);
    g_bit_unlock(&ea->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Renseigne la taille de la valeur indiquée à la construction. *
*                                                                             *
*  Retour      : Taille de la valeur représentée en mémoire.                  *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

MemoryDataSize g_imm_operand_get_size(const GImmOperand *operand)
{
    MemoryDataSize result;                  /* Taille à retourner          */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = extra->size;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                size  = taille de l'opérande souhaitée.                      *
*                ...  = valeur sur x bits à venir récupérer.                  *
*                                                                             *
*  Description : Fournit la valeur portée par une opérande numérique.         *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_get_value(const GImmOperand *operand, MemoryDataSize size, ...)
{
    bool result;                            /* Bilan à retourner           */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/
    va_list ap;                             /* Liste des compléments       */
    uint8_t *uval8;                         /* Valeur sur 8 bits           */
    uint16_t *uval16;                       /* Valeur sur 16 bits          */
    uint32_t *uval32;                       /* Valeur sur 32 bits          */
    uint64_t *uval64;                       /* Valeur sur 64 bits          */
    int8_t *sval8;                          /* Valeur sur 8 bits           */
    int16_t *sval16;                        /* Valeur sur 16 bits          */
    int32_t *sval32;                        /* Valeur sur 32 bits          */
    int64_t *sval64;                        /* Valeur sur 64 bits          */

    result = false;

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    if (extra->size != size)
        goto exit;

    va_start(ap, size);

    switch (size)
    {
        /* Pour GCC... */
        case MDS_UNDEFINED:
            goto exit;
            break;
        case MDS_4_BITS_UNSIGNED:
        case MDS_8_BITS_UNSIGNED:
            uval8 = va_arg(ap, uint8_t *);
            *uval8 = operand->raw;
            break;
        case MDS_16_BITS_UNSIGNED:
            uval16 = va_arg(ap, uint16_t *);
            *uval16 = operand->raw;
            break;
        case MDS_32_BITS_UNSIGNED:
            uval32 = va_arg(ap, uint32_t *);
            *uval32 = operand->raw;
            break;
        case MDS_64_BITS_UNSIGNED:
            uval64 = va_arg(ap, uint64_t *);
            *uval64 = operand->raw;
            break;
        case MDS_4_BITS_SIGNED:
        case MDS_8_BITS_SIGNED:
            sval8 = va_arg(ap, int8_t *);
            *sval8 = operand->raw;
            break;
        case MDS_16_BITS_SIGNED:
            sval16 = va_arg(ap, int16_t *);
            *sval16 = operand->raw;
            break;
        case MDS_32_BITS_SIGNED:
            sval32 = va_arg(ap, int32_t *);
            *sval32 = operand->raw;
            break;
        case MDS_64_BITS_SIGNED:
            sval64 = va_arg(ap, int64_t *);
            *sval64 = operand->raw;
            break;
    }

    va_end(ap);

    result = true;

 exit:

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Fournit la valeur brute représentée par l'opérande.          *
*                                                                             *
*  Retour      : Valeur destinée à un usage interne.                          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

uint64_t g_imm_operand_get_raw_value(const GImmOperand *operand)
{
    return operand->raw;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à actualiser. [OUT]  *
*                size    = taille de l'opérande souhaitée.                    *
*                value   = valeur sur x bits à venir récupérer.               *
*                                                                             *
*  Description : Définit la nouvelle valeur de l'opérande à une valeur.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_set_value(GImmOperand *operand, MemoryDataSize size, uint64_t value)
{
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    assert(size != MDS_UNDEFINED);

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    extra->size = size;

    operand->raw = value;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Indique si une valeur est complétée par des zéros par défaut.*
*                                                                             *
*  Retour      : true si des zéro sont ajoutés à l'affichage, false sinon.    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_get_default_padding(const GImmOperand *operand)
{
    bool result;                            /* Statut à retourner          */
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = (extra->flags & IOF_ZERO_PADDING_BY_DEFAULT);

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à actualiser. [OUT]  *
*                state   = true si des zéro sont à ajouter, false sinon.      *
*                                                                             *
*  Description : Précise si des zéro doivent compléter l'affichage ou non.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_set_default_padding(GImmOperand *operand, bool state)
{
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    if (state)
        extra->flags |= IOF_ZERO_PADDING_BY_DEFAULT;
    else
        extra->flags &= ~IOF_ZERO_PADDING_BY_DEFAULT;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à actualiser. [OUT]  *
*                state   = true si des zéro sont à ajouter, false sinon.      *
*                                                                             *
*  Description : Précise si des zéro doivent compléter l'affichage ou non.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_pad(GImmOperand *operand, bool state)
{
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    if (state)
        extra->flags |= (IOF_ZERO_PADDING_BY_DEFAULT | IOF_ZERO_PADDING);
    else
        extra->flags &= ~(IOF_ZERO_PADDING_BY_DEFAULT | IOF_ZERO_PADDING);

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Indique si une valeur est complétée par des zéros.           *
*                                                                             *
*  Retour      : true si des zéro sont ajoutés à l'affichage, false sinon.    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_does_padding(const GImmOperand *operand)
{
    bool result;                            /* Statut à retourner          */
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = (extra->flags & (IOF_ZERO_PADDING_BY_DEFAULT | IOF_ZERO_PADDING));

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à actualiser. [OUT]  *
*                display = format global d'un affichage de valeur.            *
*                                                                             *
*  Description : Définit le format textuel par défaut de la valeur.           *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_set_default_display(GImmOperand *operand, ImmOperandDisplay display)
{
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    extra->def_display = display;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Indique le format textuel par défaut de la valeur.           *
*                                                                             *
*  Retour      : Format global d'un affichage de valeur.                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

ImmOperandDisplay g_imm_operand_get_default_display(const GImmOperand *operand)
{
    ImmOperandDisplay result;               /* Affichage à retourner       */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = extra->def_display;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à actualiser. [OUT]  *
*                display = format global d'un affichage de valeur.            *
*                                                                             *
*  Description : Définit la grande ligne du format textuel de la valeur.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_set_display(GImmOperand *operand, ImmOperandDisplay display)
{
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    extra->display = display;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Indique la grande ligne du format textuel de la valeur.      *
*                                                                             *
*  Retour      : Format global d'un affichage de valeur.                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

ImmOperandDisplay g_imm_operand_get_display(const GImmOperand *operand)
{
    ImmOperandDisplay result;               /* Affichage à retourner       */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    if (extra->display != IOD_COUNT)
        result = extra->display;
    else
        result = extra->def_display;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Indique le signe d'une valeur immédiate.                     *
*                                                                             *
*  Retour      : true si la valeur est strictement négative, false sinon.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_is_negative(const GImmOperand *operand)
{
    bool result;                            /* Bilan à renvoyer            */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    switch (extra->size)
    {
        case MDS_4_BITS_SIGNED:
        case MDS_8_BITS_SIGNED:
        case MDS_16_BITS_SIGNED:
        case MDS_32_BITS_SIGNED:
        case MDS_64_BITS_SIGNED:
            /**
             * Pour les valeurs plus petites que 64 bits, le compilateur
             * réalise une extension de signe lors du transtypage.
             */
            result = (operand->raw & 0x8000000000000000ll);
            break;
        default:
            result = false;
            break;
    }

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = structure dont le contenu est à consulter.         *
*                                                                             *
*  Description : Indique si une valeur immédiate est nulle ou non.            *
*                                                                             *
*  Retour      : true si la valeur est nulle, false sinon.                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_is_null(const GImmOperand *operand)
{
    return (operand->raw == 0ll);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à transcrire.                             *
*                display = type d'affichage demandé.                          *
*                value   = valeur portée par l'opérande transcrite. [OUT]     *
*                                                                             *
*  Description : Construit la chaîne de caractères correspondant à l'opérande.*
*                                                                             *
*  Retour      : Nombre de caractères utilisés.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static size_t _g_imm_operand_to_string(const GImmOperand *operand, ImmOperandDisplay display, char value[IMM_MAX_SIZE])
{
    size_t result;                          /* Longueur à retourner        */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/
    unsigned int range;                     /* Catégorie de la taille      */
    const char *prefix;                     /* Entrée en matière           */
    const char *suffix;                     /* Sortie de matière           */
    const char *alternate;                  /* Préfixe de forme alternative*/
    const char *intro;                      /* Introduction du formatage   */
    bool do_padding;                        /* Indication de bourrage      */
    const char *zpad;                       /* Remplissage par des zéros   */
    const char *lmod;                       /* Modification de longueur    */
    const char *conv;                       /* Opérateur de conversion     */
    char binval[65];                        /* Conversion intégrée         */
    unsigned int max;                       /* Indice du plus fort bit     */
    unsigned int i;                         /* Boucle de parcours          */
    char format[16 + 65];                   /* Format d'impression final   */

    static const char *zpad_defs[] = { "", "02", "04", "08", "016" };
    static const char *lmod_defs[] = { "hh", "hh", "h", "", __PRI64_PREFIX };
    static const char *conv_si_defs[] = { "", "o", "d", "x", "c" };
    static const char *conv_us_defs[] = { "", "o", "u", "x", "c" };

    assert(display <= IOD_LAST_VALID);

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    range = MDS_RANGE(extra->size);

    /* Encadrement pour les caractères */
    if (display == IOD_CHAR)
    {
        prefix = "'";
        suffix = "'";
    }
    else
    {
        prefix = "";
        suffix = "";
    }

    /* Préfix de forme '0x', 'b' ou '0' */
    switch (display)
    {
        case IOD_BIN:
            alternate = "b";
            break;
        case IOD_OCT:
            alternate = "0";
            break;
        case IOD_HEX:
            alternate = "0x";
            break;
        default:
            alternate = "";
            break;
    }

    /* Va-t-on réellement avoir besoin d'un formatage ? */
    if (display != IOD_BIN)
        intro = "%";
    else
        intro = "";

    /* Drapeau de remplissage ? */

    do_padding = (extra->flags & (IOF_ZERO_PADDING_BY_DEFAULT | IOF_ZERO_PADDING));

    if (do_padding)
    {
        if (extra->display != IOD_COUNT)
            do_padding = (extra->display != IOD_BIN && extra->display != IOD_HEX);
        else
            do_padding = (extra->def_display != IOD_BIN && extra->def_display != IOD_HEX);
    }

    switch (display)
    {
        case IOD_BIN:
        case IOD_CHAR:
        case IOD_OCT:
        case IOD_DEC:
            zpad = "";
            break;
        default:
            zpad = (do_padding ? zpad_defs[range] : "");
            break;
    }

    /* Modification de la longueur fournie */

    if (display != IOD_BIN)
        lmod = lmod_defs[range];
    else
        lmod = "";

    /* Spécification de la conversion */

    if (display != IOD_BIN)
    {
        if (MDS_IS_SIGNED(extra->size))
            conv = conv_si_defs[display];
        else
            conv = conv_us_defs[display];

    }
    else
    {
        if (do_padding)
            max = range * 8;

        else
        {
            if (!msb_64(operand->raw, &max))
            {
                conv = "0";
                max = 0;
            }
        }

        if (max > 0)
        {
            conv = binval;

            for (i = max; i > 0; i--)
                binval[max - i] = (operand->raw & (1llu << (i - 1)) ? '1' : '0');

            binval[max] = '\0';

        }

    }

    /* Impression finale */

    snprintf(format, sizeof(format), "%s%s%s%s%s%s%s", prefix, alternate, intro, zpad, lmod, conv, suffix);

    switch (extra->size)
    {
        case MDS_UNDEFINED:
            result = snprintf(value, IMM_MAX_SIZE, "<? undef value ?>");
            break;

        case MDS_4_BITS_UNSIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (uint8_t)operand->raw);
            break;

        case MDS_8_BITS_UNSIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (uint8_t)operand->raw);
            break;

        case MDS_16_BITS_UNSIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (uint16_t)operand->raw);
            break;

        case MDS_32_BITS_UNSIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (uint32_t)operand->raw);
            break;

        case MDS_64_BITS_UNSIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (uint64_t)operand->raw);
            break;

        case MDS_4_BITS_SIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (int8_t)operand->raw);
            break;

        case MDS_8_BITS_SIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (int8_t)operand->raw);
            break;

        case MDS_16_BITS_SIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (int16_t)operand->raw);
            break;

        case MDS_32_BITS_SIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (int32_t)operand->raw);
            break;

        case MDS_64_BITS_SIGNED:
            result = snprintf(value, IMM_MAX_SIZE, format, (int64_t)operand->raw);
            break;

        default:
            assert(false);
            result = 0;
            break;

    }

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    assert(result > 0);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à transcrire.                             *
*                syntax  = type de représentation demandée.                   *
*                value   = valeur portée par l'opérande transcrite. [OUT]     *
*                                                                             *
*  Description : Construit la chaîne de caractères correspondant à l'opérande.*
*                                                                             *
*  Retour      : Nombre de caractères utilisés.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

size_t g_imm_operand_to_string(const GImmOperand *operand, char value[IMM_MAX_SIZE])
{
    size_t result;                          /* Longueur à retourner        */
    ImmOperandDisplay display;              /* Type d'affichage courant    */

    display = g_imm_operand_get_display(operand);

    result = _g_imm_operand_to_string(operand, display, value);

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

static void g_imm_operand_print(const GImmOperand *operand, GBufferLine *line)
{
    char value[IMM_MAX_SIZE];               /* Chaîne à imprimer           */
    size_t len;                             /* Taille de l'élément inséré  */

    len = g_imm_operand_to_string(operand, value);

    g_buffer_line_append_text(line, DLC_ASSEMBLY, value, len, RTT_IMMEDIATE, G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                binary  = informations relatives au binaire chargé.          *
*                                                                             *
*  Description : Construit un petit résumé concis de l'opérande.              *
*                                                                             *
*  Retour      : Chaîne de caractères à libérer après usage ou NULL.          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static char *g_imm_operand_build_tooltip(const GImmOperand *operand, const GLoadedBinary *binary)
{
    char *result;                           /* Description à retourner     */
    char value[IMM_MAX_SIZE];               /* Conversion artificielle     */
    char *conv;                             /* Affichage de la Conversion  */

    if (operand->raw <= UCHAR_MAX && isprint(operand->raw))
        switch (operand->raw)
        {
            case '&':
                asprintf(&result, _("Character: '&amp;'"));
                break;
            case '<':
                asprintf(&result, _("Character: '&lt;'"));
                break;
            case '>':
                asprintf(&result, _("Character: '&gt;'"));
                break;
            default:
                asprintf(&result, _("Character: '%c'"), (char)operand->raw);
                break;
        }

    else
        asprintf(&result, _("Character: &lt;not printable&gt;"));

    /* Binaire */

    _g_imm_operand_to_string(operand, IOD_BIN, value);

    asprintf(&conv, _("Binary: %s"), value);

    result = stradd(result, "\n");
    result = stradd(result, conv);

    free(conv);

    /* Octal */

    _g_imm_operand_to_string(operand, IOD_OCT, value);

    asprintf(&conv, _("Octal: %s"), value);

    result = stradd(result, "\n");
    result = stradd(result, conv);

    free(conv);

    /* Décimal */

    _g_imm_operand_to_string(operand, IOD_DEC, value);

    asprintf(&conv, _("Decimal: %s"), value);

    result = stradd(result, "\n");
    result = stradd(result, conv);

    free(conv);

    /* Hexadécimal */

    _g_imm_operand_to_string(operand, IOD_HEX, value);

    asprintf(&conv, _("Hexadecimal: %s"), value);

    result = stradd(result, "\n");
    result = stradd(result, conv);

    free(conv);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à traiter.                                *
*                pos     = valeur résultante. [OUT]                           *
*                                                                             *
*  Description : Convertit une valeur immédiate en position de type phys_t.   *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_to_phys_t(const GImmOperand *operand, phys_t *pos)
{
    bool result;                            /* Bilan à renvoyer            */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = !MDS_IS_SIGNED(extra->size);

    if (result)
        *pos = operand->raw;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à traiter.                                *
*                addr    = valeur résultante. [OUT]                           *
*                                                                             *
*  Description : Convertit une valeur immédiate en adresse de type virt_t.    *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_imm_operand_to_virt_t(const GImmOperand *operand, virt_t *addr)
{
    bool result;                            /* Bilan à renvoyer            */
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = !MDS_IS_SIGNED(extra->size);

    if (result)
        *addr = operand->raw;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à traiter.                                *
*                val     = valeur résultante. [OUT]                           *
*                                                                             *
*  Description : Convertit une valeur immédiate en valeur de type leb128_t.   *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_as_leb128(const GImmOperand *operand, leb128_t *val)
{
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    *val = operand->raw;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à traiter.                                *
*                val     = valeur résultante. [OUT]                           *
*                                                                             *
*  Description : Convertit une valeur immédiate en valeur de type uleb128_t.  *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_imm_operand_as_uleb128(const GImmOperand *operand, uleb128_t *val)
{
    immop_obj_extra *extra;                 /* Données insérées à consulter*/

    extra = GET_IMM_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    *val = operand->raw;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


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

static bool g_imm_operand_unserialize(GImmOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    parent = G_ARCH_OPERAND_CLASS(g_imm_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
        result = extract_packed_buffer(pbuf, &operand->raw, sizeof(uint64_t), true);

    if (result)
    {
        extra = GET_IMM_OP_EXTRA(operand);

        g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

        result = extract_packed_buffer(pbuf, &extra->size, sizeof(MemoryDataSize), true);

        if (result)
            result = extract_packed_buffer(pbuf, &extra->def_display, sizeof(ImmOperandDisplay), true);

        if (result)
            result = extract_packed_buffer(pbuf, &extra->display, sizeof(ImmOperandDisplay), true);

        if (result)
            result = extract_packed_buffer(pbuf, &extra->flags, sizeof(uint8_t), false);

        g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    }

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

static bool g_imm_operand_serialize(const GImmOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    immop_obj_extra *extra;                 /* Données insérées à modifier */

    parent = G_ARCH_OPERAND_CLASS(g_imm_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
        result = extend_packed_buffer(pbuf, &operand->raw, sizeof(uint64_t), true);

    if (result)
    {
        extra = GET_IMM_OP_EXTRA(operand);

        g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

        result = extend_packed_buffer(pbuf, &extra->size, sizeof(MemoryDataSize), true);

        if (result)
            result = extend_packed_buffer(pbuf, &extra->def_display, sizeof(ImmOperandDisplay), true);

        if (result)
            result = extend_packed_buffer(pbuf, &extra->display, sizeof(ImmOperandDisplay), true);

        if (result)
            result = extend_packed_buffer(pbuf, &extra->flags, sizeof(ImmOpFlag), true);

        g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

    }

    return result;

}


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

static bool g_imm_operand_get_addr(const GImmOperand *operand, const vmpa2t *src, GBinFormat *format, GArchProcessor *proc, vmpa2t *addr)
{
    bool result;                            /* Bilan à retourner           */
    virt_t virt;                            /* Adresse virtuelle           */

    result = g_imm_operand_to_virt_t(operand, &virt);

    if (result)
        result = g_exe_format_translate_address_into_vmpa(G_EXE_FORMAT(format), virt, addr);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = operande à consulter.                              *
*                text    = texte alternatif de représentation.                *
*                                                                             *
*  Description : Construit un opérande de représentation alternative.         *
*                                                                             *
*  Retour      : Nouvel opérande, en version renommée.                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static GRenamedOperand *g_imm_operand_build(const GImmOperand *operand, const char *text)
{
    GRenamedOperand *result;                /* Instance à retourner        */

    result = G_RENAMED_OPERAND(g_known_imm_operand_new(operand, text));

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                         REMPLACEMENT DE VALEURS IMMEDIATES                         */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour un remplacemet d'opérande de valeur numérique. */
G_DEFINE_TYPE_WITH_CODE(GKnownImmOperand, g_known_imm_operand, G_TYPE_IMM_OPERAND,
                        G_IMPLEMENT_INTERFACE(G_TYPE_RENAMED_OPERAND, g_known_imm_operand_renamed_interface_init));


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des remplacements d'opérandes.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_known_imm_operand_class_init(GKnownImmOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);
    operand = G_ARCH_OPERAND_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_known_imm_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_known_imm_operand_finalize;

    operand->compare = (operand_compare_fc)g_known_imm_operand_compare;
    operand->print = (operand_print_fc)g_known_imm_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_known_imm_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_known_imm_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise un remplacement d'opérande de valeur immédiate.   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_known_imm_operand_init(GKnownImmOperand *operand)
{
    operand->alt_text = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de renommage.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_known_imm_operand_renamed_interface_init(GRenamedOperandInterface *iface)
{
    iface->get_text = (get_renamed_text_fc)g_known_imm_operand_get_text;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_known_imm_operand_dispose(GKnownImmOperand *operand)
{
    if (operand->alt_text != NULL)
        free(operand->alt_text);

    G_OBJECT_CLASS(g_known_imm_operand_parent_class)->dispose(G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance d'objet GLib à traiter.                   *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_known_imm_operand_finalize(GKnownImmOperand *operand)
{
    G_OBJECT_CLASS(g_known_imm_operand_parent_class)->finalize(G_OBJECT(operand));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : old = opérande à venir copier avant son remplacement.        *
*                alt = texte alternatif à présenter pour l'impression.        *
*                                                                             *
*  Description : Crée un opérande remplaçant visuellement une valeur.         *
*                                                                             *
*  Retour      : Instruction mise en place.                                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_known_imm_operand_new(const GImmOperand *old, const char *alt)
{
    GKnownImmOperand *result;               /* Remplacement à retourner    */
    immop_obj_extra *src;                   /* Données insérées à consulter*/
    immop_obj_extra *dest;                  /* Données insérées à modifier */

    result = g_object_new(G_TYPE_KNOWN_IMM_OPERAND, NULL);

    result->parent.raw = old->raw;

    src = GET_IMM_OP_EXTRA(old);
    dest = GET_IMM_OP_EXTRA(&result->parent);

    g_bit_lock(&src->lock, HOLE_LOCK_BIT);

    *dest = *src;

    g_bit_unlock(&src->lock, HOLE_LOCK_BIT);

    result->alt_text = strdup(alt);

    return G_ARCH_OPERAND(result);

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

static int g_known_imm_operand_compare(const GKnownImmOperand *a, const GKnownImmOperand *b)
{
    int result;                             /* Bilan à retourner           */
    GArchOperandClass *class;               /* Classe parente à consulter  */

    class = G_ARCH_OPERAND_CLASS(g_known_imm_operand_parent_class);

    result = class->compare(G_ARCH_OPERAND(a), G_ARCH_OPERAND(b));

    if (result == 0)
        result = strcmp(a->alt_text, b->alt_text);

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

static void g_known_imm_operand_print(const GKnownImmOperand *operand, GBufferLine *line)
{
    size_t len;                             /* Taille de l'élément inséré  */

    len = strlen(operand->alt_text);

    g_buffer_line_append_text(line, DLC_ASSEMBLY, operand->alt_text, len, RTT_IMMEDIATE, G_OBJECT(operand));

}


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

static bool g_known_imm_operand_unserialize(GKnownImmOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    unsigned short len;                     /* Taille du contenu alternatif*/

    parent = G_ARCH_OPERAND_CLASS(g_known_imm_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
        result = extract_packed_buffer(pbuf, &len, sizeof(unsigned short), true);

    if (result)
        result = (len > 0);

    if (result)
    {
        operand->alt_text = malloc(len);

        result = extract_packed_buffer(pbuf, operand->alt_text, len, false);

    }

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

static bool g_known_imm_operand_serialize(const GKnownImmOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    size_t len;                             /* Taille du contenu alternatif*/

    parent = G_ARCH_OPERAND_CLASS(g_known_imm_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
    {
        len = strlen(operand->alt_text) + 1;
        assert(len > 1);

        if (len > (2 << (sizeof(unsigned short) * 8 - 1)))
        {
            log_variadic_message(LMT_ERROR, "Alternative text too long: '%s' (%zu bytes)",
                                 operand->alt_text, len);
            result = false;
        }

        else
            result = extend_packed_buffer(pbuf, (unsigned short []) { len }, sizeof(unsigned short), true);

        if (result)
            result = extend_packed_buffer(pbuf, operand->alt_text, len, false);

    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = operande à consulter.                              *
*                                                                             *
*  Description : Fournit un texte comme représentation alternative d'opérande.*
*                                                                             *
*  Retour      : Chaîne de caractère de représentation alternative.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static const char *g_known_imm_operand_get_text(const GKnownImmOperand *operand)
{
    const char *result;                     /* Texte à retourner           */

    result = operand->alt_text;

    return result;

}
