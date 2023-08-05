
/* Chrysalide - Outil d'analyse de fichiers binaires
 * it.c - manipulation des informations de l'instruction TI
 *
 * Copyright (C) 2018 Cyrille Bagard
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


#include "it.h"


#include <assert.h>


#include <arch/operand-int.h>
#include <common/sort.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande organisant l'application d'une instruction IT (instance) */
struct _GArmV7ITCondOperand
{
    GArchOperand parent;                    /* Instance parente            */

    ArmCondCode firstcond;                  /* Condition première          */
    uint8_t mask;                           /* Masque de l'interprétation  */

};


/* Définition d'un opérande organisant l'application d'une instruction IT (classe) */
struct _GArmV7ITCondOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des conditions d'application d'IT. */
static void g_armv7_itcond_operand_class_init(GArmV7ITCondOperandClass *);

/* Initialise une instance de conditions d'application d'IT. */
static void g_armv7_itcond_operand_init(GArmV7ITCondOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_itcond_operand_dispose(GArmV7ITCondOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_itcond_operand_finalize(GArmV7ITCondOperand *);

/* Compare un opérande avec un autre. */
static int g_armv7_itcond_operand_compare(const GArmV7ITCondOperand *, const GArmV7ITCondOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_itcond_operand_print(const GArmV7ITCondOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_itcond_operand_unserialize(GArmV7ITCondOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_itcond_operand_serialize(const GArmV7ITCondOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour l'application d'une instruction IT. */
G_DEFINE_TYPE(GArmV7ITCondOperand, g_armv7_itcond_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des conditions d'application d'IT.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_itcond_operand_class_init(GArmV7ITCondOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);
    operand = G_ARCH_OPERAND_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_itcond_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_itcond_operand_finalize;

    operand->compare = (operand_compare_fc)g_armv7_itcond_operand_compare;
    operand->print = (operand_print_fc)g_armv7_itcond_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_itcond_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_itcond_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance de conditions d'application d'IT.    *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_itcond_operand_init(GArmV7ITCondOperand *operand)
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

static void g_armv7_itcond_operand_dispose(GArmV7ITCondOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_itcond_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_itcond_operand_finalize(GArmV7ITCondOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_itcond_operand_parent_class)->finalize(G_OBJECT(operand));

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

static int g_armv7_itcond_operand_compare(const GArmV7ITCondOperand *a, const GArmV7ITCondOperand *b)
{
    int result;                             /* Bilan à faire remonter      */

    result = sort_boolean(a->firstcond, b->firstcond);

    if (result == 0)
        result = sort_unsigned_long(a->mask, b->mask);

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

static void g_armv7_itcond_operand_print(const GArmV7ITCondOperand *operand, GBufferLine *line)
{
    const char *kw;                         /* Mot clef à imprimer         */

    switch (operand->firstcond)
    {
        case ACC_EQ: kw = "EQ"; break;
        case ACC_NE: kw = "NE"; break;
        case ACC_HS: kw = "HS"; break;
        case ACC_LO: kw = "LO"; break;
        case ACC_MI: kw = "MI"; break;
        case ACC_PL: kw = "PL"; break;
        case ACC_VS: kw = "VS"; break;
        case ACC_VC: kw = "VC"; break;
        case ACC_HI: kw = "HI"; break;
        case ACC_LS: kw = "LS"; break;
        case ACC_GE: kw = "GE"; break;
        case ACC_LT: kw = "LT"; break;
        case ACC_GT: kw = "GT"; break;
        case ACC_LE: kw = "LE"; break;
        case ACC_AL: kw = NULL; break;
        case ACC_NV: kw = "NV"; break;

        default:    /* Pour GCC... */
            assert(false);
            kw = NULL;
            break;

    }

    if (kw != NULL)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, kw, 2, RTT_KEY_WORD, NULL);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : firstcond = valeur brute de la condition d'exécution.        *
*                mask      = masque d'interprétation pour l'instruction.      *
*                                                                             *
*  Description : Crée un opérande lié à une instruction IT.                   *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_itcond_operand_new(uint8_t firstcond, uint8_t mask)
{
    GArmV7ITCondOperand *result;            /* Structure à retourner       */

    if (firstcond > ACC_NV)
        return NULL;

    result = g_object_new(G_TYPE_ARMV7_ITCOND_OPERAND, NULL);

    result->firstcond = firstcond;
    result->mask = mask;

    return G_ARCH_OPERAND(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Fournit la condition associée à l'opérande.                  *
*                                                                             *
*  Retour      : Condition classique pour ARMv7.                              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

ArmCondCode g_armv7_itcond_operand_get_firstcond(const GArmV7ITCondOperand *operand)
{
    ArmCondCode result;                     /* Condition à renvoyer        */

    result = operand->firstcond;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Fournit le masque d'interprétation de la condition.          *
*                                                                             *
*  Retour      : Masque de bits.                                              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

uint8_t g_armv7_itcond_operand_get_mask(const GArmV7ITCondOperand *operand)
{
    uint8_t result;                         /* Valeur à retourner          */

    result = operand->mask;

    return result;

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

static bool g_armv7_itcond_operand_unserialize(GArmV7ITCondOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_itcond_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
        result = extract_packed_buffer(pbuf, &operand->firstcond, sizeof(ArmCondCode), true);

    if (result)
        result = extract_packed_buffer(pbuf, &operand->mask, sizeof(uint8_t), false);

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

static bool g_armv7_itcond_operand_serialize(const GArmV7ITCondOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_itcond_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
        result = extend_packed_buffer(pbuf, &operand->firstcond, sizeof(ArmCondCode), true);

    if (result)
        result = extend_packed_buffer(pbuf, &operand->mask, sizeof(uint8_t), false);

    return result;

}
