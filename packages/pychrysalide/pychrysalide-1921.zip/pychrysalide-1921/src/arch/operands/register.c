
/* Chrysalide - Outil d'analyse de fichiers binaires
 * registers.c - aides auxiliaires relatives aux registres Dalvik
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


#include "register.h"


#include "register-int.h"
#include "../storage.h"



/* ------------------------- REGISTRE SOUS FORME D'OPERANDE ------------------------- */


/* Initialise la classe des opérandes de registre. */
static void g_register_operand_class_init(GRegisterOperandClass *);

/* Initialise une instance d'opérande de registre. */
static void g_register_operand_init(GRegisterOperand *);

/* Supprime toutes les références externes. */
static void g_register_operand_dispose(GRegisterOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_register_operand_finalize(GRegisterOperand *);

/* Compare un opérande avec un autre. */
static int g_register_operand_compare(const GRegisterOperand *, const GRegisterOperand *);

/* Traduit un opérande en version humainement lisible. */
static void g_register_operand_print(const GRegisterOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_register_operand_unserialize(GRegisterOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_register_operand_serialize(const GRegisterOperand *, GAsmStorage *, packed_buffer_t *);



/* ---------------------------------------------------------------------------------- */
/*                           REGISTRE SOUS FORME D'OPERANDE                           */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini par la GLib pour un opérande de registre Dalvik. */
G_DEFINE_TYPE(GRegisterOperand, g_register_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des opérandes de registre Dalvik.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_register_operand_class_init(GRegisterOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);
    operand = G_ARCH_OPERAND_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_register_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_register_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->compare = (operand_compare_fc)g_register_operand_compare;
    operand->print = (operand_print_fc)g_register_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_register_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_register_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'opérande de registre Dalvik.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_register_operand_init(GRegisterOperand *operand)
{
    operand->reg = NULL;

    INIT_REG_OP_EXTRA(operand);

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

static void g_register_operand_dispose(GRegisterOperand *operand)
{
    g_clear_object(&operand->reg);

    G_OBJECT_CLASS(g_register_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_register_operand_finalize(GRegisterOperand *operand)
{
    G_OBJECT_CLASS(g_register_operand_parent_class)->finalize(G_OBJECT(operand));

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

static int g_register_operand_compare(const GRegisterOperand *a, const GRegisterOperand *b)
{
    int result;                             /* Bilan à retourner           */

    result = g_arch_register_compare(a->reg, b->reg);

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

static void g_register_operand_print(const GRegisterOperand *operand, GBufferLine *line)
{
    g_arch_register_print(operand->reg, line);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande représentant un registre.                 *
*                                                                             *
*  Description : Fournit le registre associé à l'opérande.                    *
*                                                                             *
*  Retour      : Représentation interne du registre.                          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchRegister *g_register_operand_get_register(const GRegisterOperand *operand)
{
    GArchRegister *result;                  /* Instance à retourner        */

    result = operand->reg;

    if (result != NULL)
        g_object_ref(G_OBJECT(result));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande représentant un registre à mettre à jour. *
*                                                                             *
*  Description : Marque l'opérande comme étant écrit plutôt que consulté.     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_register_operand_mark_as_written(GRegisterOperand *operand)
{
    regop_obj_extra *extra;                 /* Données insérées à modifier */

    extra = GET_REG_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    extra->is_written = true;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande représentant un registre à consulter.     *
*                                                                             *
*  Description : Indique le type d'accès réalisé sur l'opérande.              *
*                                                                             *
*  Retour      : Type d'accès : true en cas d'écriture, false sinon.          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_register_operand_is_written(const GRegisterOperand *operand)
{
    bool result;                            /* Statut à retourner          */
    regop_obj_extra *extra;                 /* Données insérées à modifier */

    extra = GET_REG_OP_EXTRA(operand);

    g_bit_lock(&extra->lock, HOLE_LOCK_BIT);

    result = extra->is_written;

    g_bit_unlock(&extra->lock, HOLE_LOCK_BIT);

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

static bool g_register_operand_unserialize(GRegisterOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    off64_t pos;                            /* Position dans le flux       */
    packed_buffer_t reg_pbuf;               /* Tampon des données à écrire */
    GArchRegister *reg;                     /* Registre restauré           */

    parent = G_ARCH_OPERAND_CLASS(g_register_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
        result = extract_packed_buffer(pbuf, &pos, sizeof(off64_t), true);

    if (result)
    {
        init_packed_buffer(&reg_pbuf);

        result = g_asm_storage_load_register_data(storage, &reg_pbuf, pos);

        if (result)
        {
            reg = g_arch_register_load(storage, &reg_pbuf);
            result = (reg != NULL);
        }

        if (result)
            operand->reg = reg;

        exit_packed_buffer(&reg_pbuf);

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

static bool g_register_operand_serialize(const GRegisterOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    off64_t pos;                            /* Position dans le flux       */
    packed_buffer_t reg_pbuf;               /* Tampon des données à écrire */

    parent = G_ARCH_OPERAND_CLASS(g_register_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
    {
        init_packed_buffer(&reg_pbuf);

        result = g_arch_register_store(operand->reg, storage, &reg_pbuf);

        if (result)
            result = g_asm_storage_store_register_data(storage, &reg_pbuf, &pos);

        if (result)
            result = extend_packed_buffer(pbuf, &pos, sizeof(off64_t), true);

        exit_packed_buffer(&reg_pbuf);

    }

    return result;

}
