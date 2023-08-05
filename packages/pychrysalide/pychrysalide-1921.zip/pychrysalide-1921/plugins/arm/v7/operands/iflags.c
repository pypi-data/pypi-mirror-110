
/* Chrysalide - Outil d'analyse de fichiers binaires
 * iflags.c - opérandes précisant un masque d'interruption ARMv7
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


#include "iflags.h"


#include <arch/operand-int.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande précisant un masque d'interruption ARMv7 (instance) */
struct _GArmV7IFlagsOperand
{
    GArchOperand parent;                    /* Instance parente            */

    bool abort_bit;                         /* Interruption d'arrêt async. */
    bool irq_bit;                           /* Interruption IRQ            */
    bool fiq_bit;                           /* Interruption FIQ            */

};


/* Définition d'un opérande précisant un masque d'interruption ARMv7 (classe) */
struct _GArmV7IFlagsOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des opérandes de masque d'interruption. */
static void g_armv7_iflags_operand_class_init(GArmV7IFlagsOperandClass *);

/* Initialise une instance d'opérande de masque d'interruption. */
static void g_armv7_iflags_operand_init(GArmV7IFlagsOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_iflags_operand_dispose(GArmV7IFlagsOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_iflags_operand_finalize(GArmV7IFlagsOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_iflags_operand_print(const GArmV7IFlagsOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_iflags_operand_unserialize(GArmV7IFlagsOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_iflags_operand_serialize(const GArmV7IFlagsOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour un opérande de masque d'interruption ARMv7. */
G_DEFINE_TYPE(GArmV7IFlagsOperand, g_armv7_iflags_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des opérandes de masque d'interruption. *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_iflags_operand_class_init(GArmV7IFlagsOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_iflags_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_iflags_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->print = (operand_print_fc)g_armv7_iflags_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_iflags_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_iflags_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'opérande de masque d'interruption. *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_iflags_operand_init(GArmV7IFlagsOperand *operand)
{
    operand->abort_bit = false;
    operand->irq_bit = false;
    operand->fiq_bit = false;

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

static void g_armv7_iflags_operand_dispose(GArmV7IFlagsOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_iflags_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_iflags_operand_finalize(GArmV7IFlagsOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_iflags_operand_parent_class)->finalize(G_OBJECT(operand));

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

static void g_armv7_iflags_operand_print(const GArmV7IFlagsOperand *operand, GBufferLine *line)
{
    if (operand->abort_bit)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "A", 1, RTT_REGISTER, NULL);

    if (operand->irq_bit)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "I", 1, RTT_REGISTER, NULL);

    if (operand->fiq_bit)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "F", 1, RTT_REGISTER, NULL);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : a = bit d'arrêt asynchrone.                                  *
*                i = bit d'interruption IRQ.                                  *
*                f = bit d'interruption FIQ.                                  *
*                                                                             *
*  Description : Crée un opérande de masque d'interruption ARMv7.             *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_iflags_operand_new(bool a, bool i, bool f)
{
    GArmV7IFlagsOperand *result;         /* Structure à retourner       */

    result = g_object_new(G_TYPE_ARMV7_IFLAGS_OPERAND, NULL);

    result->abort_bit = a;
    result->irq_bit = i;
    result->fiq_bit = f;

    return G_ARCH_OPERAND(result);

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

static bool g_armv7_iflags_operand_unserialize(GArmV7IFlagsOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t boolean;                        /* Valeur booléenne            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_iflags_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result)
            operand->abort_bit = (boolean == 1 ? true : false);

    }

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result)
            operand->irq_bit = (boolean == 1 ? true : false);

    }

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result)
            operand->fiq_bit = (boolean == 1 ? true : false);

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

static bool g_armv7_iflags_operand_serialize(const GArmV7IFlagsOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t boolean;                        /* Valeur booléenne            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_iflags_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
    {
        boolean = (operand->abort_bit ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    if (result)
    {
        boolean = (operand->irq_bit ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    if (result)
    {
        boolean = (operand->fiq_bit ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    return result;

}
