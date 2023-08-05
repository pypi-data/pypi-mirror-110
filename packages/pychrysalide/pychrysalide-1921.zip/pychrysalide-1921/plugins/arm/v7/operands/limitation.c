
/* Chrysalide - Outil d'analyse de fichiers binaires
 * limitation.c - décalages de valeurs
 *
 * Copyright (C) 2017-2018 Cyrille Bagard
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


#include "limitation.h"


#include <arch/operand-int.h>
#include <common/sort.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande déterminant une limitation de domaine et d'accès (instance) */
struct _GArmV7LimitationOperand
{
    GArchOperand parent;                    /* Instance parente            */

    BarrierLimitationType type;             /* Type de limitation          */

};


/* Définition d'un opérande déterminant une limitation de domaine et d'accès (classe) */
struct _GArmV7LimitationOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des co-processeurs ARM. */
static void g_armv7_limitation_operand_class_init(GArmV7LimitationOperandClass *);

/* Initialise une instance de co-processeur ARM. */
static void g_armv7_limitation_operand_init(GArmV7LimitationOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_limitation_operand_dispose(GArmV7LimitationOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_limitation_operand_finalize(GArmV7LimitationOperand *);

/* Compare un opérande avec un autre. */
static int g_armv7_limitation_operand_compare(const GArmV7LimitationOperand *, const GArmV7LimitationOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_limitation_operand_print(const GArmV7LimitationOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_limitation_operand_unserialize(GArmV7LimitationOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_limitation_operand_serialize(const GArmV7LimitationOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour une limitation de domaine et d'accès. */
G_DEFINE_TYPE(GArmV7LimitationOperand, g_armv7_limitation_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des limitations de domaine et d'accès.  *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_limitation_operand_class_init(GArmV7LimitationOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);
    operand = G_ARCH_OPERAND_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_limitation_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_limitation_operand_finalize;

    operand->compare = (operand_compare_fc)g_armv7_limitation_operand_compare;
    operand->print = (operand_print_fc)g_armv7_limitation_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_limitation_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_limitation_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance de limitation de domaine et d'accès. *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_limitation_operand_init(GArmV7LimitationOperand *operand)
{

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

static void g_armv7_limitation_operand_dispose(GArmV7LimitationOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_limitation_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_limitation_operand_finalize(GArmV7LimitationOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_limitation_operand_parent_class)->finalize(G_OBJECT(operand));

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

static int g_armv7_limitation_operand_compare(const GArmV7LimitationOperand *a, const GArmV7LimitationOperand *b)
{
    int result;                             /* Bilan à faire remonter      */

    result = sort_unsigned_long(a->type, b->type);

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

static void g_armv7_limitation_operand_print(const GArmV7LimitationOperand *operand, GBufferLine *line)
{
    switch (operand->type)
    {
        case BLT_SY:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "SY", 2, RTT_KEY_WORD, NULL);
            break;

        case BLT_ST:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "ST", 2, RTT_KEY_WORD, NULL);
            break;

        case BLT_ISH:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "ISH", 3, RTT_KEY_WORD, NULL);
            break;

        case BLT_ISHST:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "ISHST", 5, RTT_KEY_WORD, NULL);
            break;

        case BLT_NSH:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "NSH", 3, RTT_KEY_WORD, NULL);
            break;

        case BLT_NSHST:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "NSHST", 5, RTT_KEY_WORD, NULL);
            break;

        case BLT_OSH:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "OSH", 3, RTT_KEY_WORD, NULL);
            break;

        case BLT_OSHST:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "OSHST", 5, RTT_KEY_WORD, NULL);
            break;

        default:
            g_buffer_line_append_text(line, DLC_ASSEMBLY, "(reserved)", 10, RTT_KEY_WORD, NULL);
            break;

    }

}


/******************************************************************************
*                                                                             *
*  Paramètres  : raw = valeur brute de la limitation à considérer.            *
*                                                                             *
*  Description : Crée une représentation d'une limitation pour barrière.      *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_limitation_operand_new(uint8_t raw)
{
    GArmV7LimitationOperand *result;        /* Structure à retourner       */

    result = g_object_new(G_TYPE_ARMV7_LIMITATION_OPERAND, NULL);

    if (raw < 0b0010 || raw > 0b1111)
        result->type = BLT_RESERVED;

    else
        result->type = raw;

    return G_ARCH_OPERAND(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique le type de limitation représentée.                   *
*                                                                             *
*  Retour      : Type de limitation d'accès et de domaine.                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

BarrierLimitationType g_armv7_limitation_operand_get_value(const GArmV7LimitationOperand *operand)
{
    return operand->type;

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

static bool g_armv7_limitation_operand_unserialize(GArmV7LimitationOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_limitation_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
        result = extract_packed_buffer(pbuf, &operand->type, sizeof(BarrierLimitationType), true);

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

static bool g_armv7_limitation_operand_serialize(const GArmV7LimitationOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_limitation_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
        result = extend_packed_buffer(pbuf, &operand->type, sizeof(BarrierLimitationType), true);

    return result;

}
