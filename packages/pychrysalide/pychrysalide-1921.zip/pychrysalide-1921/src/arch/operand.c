
/* Chrysalide - Outil d'analyse de fichiers binaires
 * operand.c - gestion générique des opérandes
 *
 * Copyright (C) 2008-2020 Cyrille Bagard
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


#include "operand.h"


#include <assert.h>
#include <malloc.h>
#include <string.h>


#include "operand-int.h"
#include "storage.h"
#include "../common/sort.h"
#include "../core/logs.h"



/* ---------------------------------------------------------------------------------- */
/*                          DEFINITION D'OPERANDE QUELCONQUE                          */
/* ---------------------------------------------------------------------------------- */


/* Initialise la classe générique des opérandes. */
static void g_arch_operand_class_init(GArchOperandClass *);

/* Initialise une instance d'opérande d'architecture. */
static void g_arch_operand_init(GArchOperand *);

/* Supprime toutes les références externes. */
static void g_arch_operand_dispose(GArchOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_arch_operand_finalize(GArchOperand *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_arch_operand_unserialize(GArchOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_arch_operand_serialize(const GArchOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini pour un opérande d'architecture. */
G_DEFINE_TYPE(GArchOperand, g_arch_operand, G_TYPE_OBJECT);



/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe générique des opérandes.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_arch_operand_class_init(GArchOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Encore une autre vision...  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_arch_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_arch_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->unserialize = (unserialize_operand_fc)g_arch_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_arch_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'opérande d'architecture.           *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_arch_operand_init(GArchOperand *operand)
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

static void g_arch_operand_dispose(GArchOperand *operand)
{
    G_OBJECT_CLASS(g_arch_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_arch_operand_finalize(GArchOperand *operand)
{
    G_OBJECT_CLASS(g_arch_operand_parent_class)->finalize(G_OBJECT(operand));

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

int g_arch_operand_compare(const GArchOperand *a, const GArchOperand *b)
{
    int result;                             /* Bilan à faire remonter      */
    GType type_a;                           /* Type de l'object A          */
    GType type_b;                           /* Type de l'object B          */

    type_a = G_OBJECT_TYPE(G_OBJECT(a));
    type_b = G_OBJECT_TYPE(G_OBJECT(b));

    assert(sizeof(GType) <= sizeof(unsigned long));

    result = sort_unsigned_long(type_a, type_b);

    if (result == 0)
        result = G_ARCH_OPERAND_GET_CLASS(a)->compare(a, b);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                target  = instruction à venir retrouver.                     *
*                                                                             *
*  Description : Détermine le chemin conduisant à un opérande interne.        *
*                                                                             *
*  Retour      : Chemin d'accès à l'opérande ou NULL en cas d'absence.        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

char *g_arch_operand_find_inner_operand_path(const GArchOperand *operand, const GArchOperand *target)
{
    char *result;                           /* Chemin à retourner          */
    GArchOperandClass *class;               /* Classe associée à l'objet   */

    class = G_ARCH_OPERAND_GET_CLASS(operand);

    if (class->find_inner != NULL)
        result = class->find_inner(operand, target);

    else
        result = NULL;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                path  = chemin d'accès à un opérande à retrouver.            *
*                                                                             *
*  Description : Obtient l'opérande correspondant à un chemin donné.          *
*                                                                             *
*  Retour      : Opérande trouvé ou NULL en cas d'échec.                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_arch_operand_get_inner_operand_from_path(const GArchOperand *operand, const char *path)
{
    GArchOperand *result;                   /* Opérande trouvée à renvoyer */
    GArchOperandClass *class;               /* Classe associée à l'objet   */

    class = G_ARCH_OPERAND_GET_CLASS(operand);

    if (class->get_inner != NULL)
        result = class->get_inner(operand, path);

    else
        result = NULL;

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

void g_arch_operand_print(const GArchOperand *operand, GBufferLine *line)
{
    G_ARCH_OPERAND_GET_CLASS(operand)->print(operand, line);

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

char *g_arch_operand_build_tooltip(const GArchOperand *operand, const GLoadedBinary *binary)
{
    char *result;                           /* Description à retourner     */
    GArchOperandClass *class;               /* Classe associée à l'objet   */

    class = G_ARCH_OPERAND_GET_CLASS(operand);

    if (class->build_tooltip != NULL)
        result = class->build_tooltip(operand, binary);
    else
        result = NULL;

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

static bool g_arch_operand_unserialize(GArchOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */

    result = true;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = mécanisme de sauvegarde à manipuler.               *
*                format  = format binaire chargé associé à l'architecture.    *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Charge un opérande depuis une mémoire tampon.                *
*                                                                             *
*  Retour      : Opérande d'assemblage constitué ou NULL en cas d'échec.      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_arch_operand_load(GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    GArchOperand *result;                   /* Instance à retourner        */
    bool status;                            /* Bilan du chargement         */

    result = G_ARCH_OPERAND(g_asm_storage_create_object(storage, pbuf));

    if (result != NULL)
    {
        status = G_ARCH_OPERAND_GET_CLASS(result)->unserialize(result, storage, format, pbuf);

        if (!status)
        {
            g_object_unref(G_OBJECT(result));
            result = NULL;
        }

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

static bool g_arch_operand_serialize(const GArchOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */

    result = true;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instruction d'assemblage à consulter.              *
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

bool g_arch_operand_store(const GArchOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */

    result = g_asm_storage_store_object_gtype(storage, G_OBJECT(operand), pbuf);

    if (result)
        result = G_ARCH_OPERAND_GET_CLASS(operand)->serialize(operand, storage, pbuf);

    return result;

}
