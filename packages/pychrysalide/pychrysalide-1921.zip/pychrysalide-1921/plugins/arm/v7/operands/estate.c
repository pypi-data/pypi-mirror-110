
/* Chrysalide - Outil d'analyse de fichiers binaires
 * estate.c - décalages de valeurs
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


#include "estate.h"


#include <arch/operand-int.h>
#include <common/sort.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande affichant le choix d'un boutisme (instance) */
struct _GArmV7EndianOperand
{
    GArchOperand parent;                    /* Instance parente            */

    bool big;                               /* Grand boutisme à afficher ? */

};


/* Définition d'un opérande affichant le choix d'un boutisme (classe) */
struct _GArmV7EndianOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des affichages de boutisme. */
static void g_armv7_endian_operand_class_init(GArmV7EndianOperandClass *);

/* Initialise une instance d'affichage de boutisme. */
static void g_armv7_endian_operand_init(GArmV7EndianOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_endian_operand_dispose(GArmV7EndianOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_endian_operand_finalize(GArmV7EndianOperand *);

/* Compare un opérande avec un autre. */
static int g_armv7_endian_operand_compare(const GArmV7EndianOperand *, const GArmV7EndianOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_endian_operand_print(const GArmV7EndianOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_endian_operand_unserialize(GArmV7EndianOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_endian_operand_serialize(const GArmV7EndianOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour une endian de domaine et d'accès. */
G_DEFINE_TYPE(GArmV7EndianOperand, g_armv7_endian_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des affichages de boutisme.             *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_endian_operand_class_init(GArmV7EndianOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);
    operand = G_ARCH_OPERAND_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_endian_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_endian_operand_finalize;

    operand->compare = (operand_compare_fc)g_armv7_endian_operand_compare;
    operand->print = (operand_print_fc)g_armv7_endian_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_endian_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_endian_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'affichage de boutisme.             *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_endian_operand_init(GArmV7EndianOperand *operand)
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

static void g_armv7_endian_operand_dispose(GArmV7EndianOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_endian_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_endian_operand_finalize(GArmV7EndianOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_endian_operand_parent_class)->finalize(G_OBJECT(operand));

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

static int g_armv7_endian_operand_compare(const GArmV7EndianOperand *a, const GArmV7EndianOperand *b)
{
    int result;                             /* Bilan à faire remonter      */

    result = sort_boolean(a->big, b->big);

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

static void g_armv7_endian_operand_print(const GArmV7EndianOperand *operand, GBufferLine *line)
{
    if (operand->big)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "BE", 2, RTT_KEY_WORD, NULL);
    else
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "LE", 2, RTT_KEY_WORD, NULL);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : big = indication sur le boutisme à représenter.              *
*                                                                             *
*  Description : Crée une représentation de boutisme ARMv7.                   *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_endian_operand_new(bool big)
{
    GArmV7EndianOperand *result;            /* Structure à retourner       */

    result = g_object_new(G_TYPE_ARMV7_ENDIAN_OPERAND, NULL);

    result->big = big;

    return G_ARCH_OPERAND(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique le type de boutisme représenté.                      *
*                                                                             *
*  Retour      : Type de boutisme.                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_armv7_endian_operand_is_big_endian(const GArmV7EndianOperand *operand)
{
    return operand->big;

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

static bool g_armv7_endian_operand_unserialize(GArmV7EndianOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t big;                            /* Grand boutisme à afficher ? */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_endian_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
    {
        result = extract_packed_buffer(pbuf, &big, sizeof(uint8_t), false);

        if (result)
            operand->big = (big == 1 ? true : false);

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

static bool g_armv7_endian_operand_serialize(const GArmV7EndianOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t big;                            /* Grand boutisme à afficher ? */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_endian_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
    {
        big = (operand->big ? 1 : 0);
        result = extend_packed_buffer(pbuf, &big, sizeof(uint8_t), false);
    }

    return result;

}
