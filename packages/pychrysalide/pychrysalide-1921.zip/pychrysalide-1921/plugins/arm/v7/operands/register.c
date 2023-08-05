
/* Chrysalide - Outil d'analyse de fichiers binaires
 * register.c - opérandes visant un registre ARMv7
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


#include "register.h"


#include <arch/operands/register-int.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande visant un registre ARMv7 (instance) */
struct _GArmV7RegisterOperand
{
    GRegisterOperand parent;                /* Instance parente            */

    unsigned int alignment;                 /* Eventuel alignement         */
    bool has_alignment;                     /* Validité du champ           */

    bool write_back;                        /* Mise à jour du registre ?   */

};


/* Définition d'un opérande visant un registre ARMv7 (classe) */
struct _GArmV7RegisterOperandClass
{
    GRegisterOperandClass parent;           /* Classe parente              */

};


/* Initialise la classe des opérandes de registre ARMv7. */
static void g_armv7_register_operand_class_init(GArmV7RegisterOperandClass *);

/* Initialise une instance d'opérande de registre ARMv7. */
static void g_armv7_register_operand_init(GArmV7RegisterOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_register_operand_dispose(GArmV7RegisterOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_register_operand_finalize(GArmV7RegisterOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_register_operand_print(const GArmV7RegisterOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_register_operand_unserialize(GArmV7RegisterOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_register_operand_serialize(const GArmV7RegisterOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour un opérande de registre ARMv7. */
G_DEFINE_TYPE(GArmV7RegisterOperand, g_armv7_register_operand, G_TYPE_REGISTER_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des opérandes de registre ARMv7.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_register_operand_class_init(GArmV7RegisterOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_register_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_register_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->print = (operand_print_fc)g_armv7_register_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_register_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_register_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'opérande de registre ARMv7.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_register_operand_init(GArmV7RegisterOperand *operand)
{
    operand->write_back = false;

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

static void g_armv7_register_operand_dispose(GArmV7RegisterOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_register_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_register_operand_finalize(GArmV7RegisterOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_register_operand_parent_class)->finalize(G_OBJECT(operand));

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

static void g_armv7_register_operand_print(const GArmV7RegisterOperand *operand, GBufferLine *line)
{
    GArchOperandClass *parent;              /* Classe parente              */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_register_operand_parent_class);

    parent->print(G_ARCH_OPERAND(operand), line);

    if (operand->write_back)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "!", 1, RTT_PUNCT, NULL);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = registre déjà en place.                                *
*                                                                             *
*  Description : Crée un opérande visant un registre ARMv7.                   *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_register_operand_new(GArmV7Register *reg)
{
    GArmV7RegisterOperand *result;         /* Structure à retourner       */

    result = g_object_new(G_TYPE_ARMV7_REGISTER_OPERAND, NULL);

    G_REGISTER_OPERAND(result)->reg = G_ARCH_REGISTER(reg);

    return G_ARCH_OPERAND(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande représentant un registre.                 *
*                align   = alignement imposé au registre.                     *
*                                                                             *
*  Description : Définit un alignement à appliquer à l'opérande de registre.  *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_armv7_register_operand_define_alignement(GArmV7RegisterOperand *operand, unsigned int align)
{
    operand->alignment = align;

    operand->has_alignment = true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande représentant un registre.                 *
*                wback   = indique si le registre est mis à jour après coup.  *
*                                                                             *
*  Description : Détermine si le registre est mis à jour après l'opération.   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_armv7_register_operand_write_back(GArmV7RegisterOperand *operand, bool wback)
{
    operand->write_back = wback;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande représentant un registre.                 *
*                                                                             *
*  Description : Indique si le registre est mis à jour après coup.            *
*                                                                             *
*  Retour      : Evolution du registre.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_armv7_register_operand_is_written_back(const GArmV7RegisterOperand *operand)
{
    bool result;                            /* Statut à retourner          */

    result = operand->write_back;

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

static bool g_armv7_register_operand_unserialize(GArmV7RegisterOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t boolean;                        /* Valeur booléenne            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_register_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result)
            operand->has_alignment = (boolean == 1 ? true : false);

    }

    if (result && operand->has_alignment)
        result = extract_packed_buffer(pbuf, &operand->alignment, sizeof(unsigned int), true);

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result)
            operand->write_back = (boolean == 1 ? true : false);

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

static bool g_armv7_register_operand_serialize(const GArmV7RegisterOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t boolean;                        /* Valeur booléenne            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_register_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
    {
        boolean = (operand->has_alignment ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    if (result && operand->has_alignment)
        result = extend_packed_buffer(pbuf, &operand->alignment, sizeof(unsigned int), true);

    if (result)
    {
        boolean = (operand->write_back ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    return result;

}
