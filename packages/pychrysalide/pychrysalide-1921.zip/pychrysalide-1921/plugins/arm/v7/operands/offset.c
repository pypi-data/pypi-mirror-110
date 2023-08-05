
/* Chrysalide - Outil d'analyse de fichiers binaires
 * offset.c - constitution d'un décalage positif ou négatif
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


#include "offset.h"


#include <stdio.h>
#include <string.h>


#include <arch/operand-int.h>
#include <common/sort.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande visant à constituer un décalage relatif ARMv7 (instance) */
struct _GArmV7OffsetOperand
{
    GArchOperand parent;                    /* Instance parente            */

    bool positive;                          /* Sens du décalage            */
    GArchOperand *value;                    /* Valeur du décalage          */

};


/* Définition d'un opérande visant à constituer un décalage relatif ARMv7 (classe) */
struct _GArmV7OffsetOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des décalages relatifs ARMv7. */
static void g_armv7_offset_operand_class_init(GArmV7OffsetOperandClass *);

/* Initialise une instance de décalage relatif ARMv7. */
static void g_armv7_offset_operand_init(GArmV7OffsetOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_offset_operand_dispose(GArmV7OffsetOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_offset_operand_finalize(GArmV7OffsetOperand *);

/* Compare un opérande avec un autre. */
static int g_armv7_offset_operand_compare(const GArmV7OffsetOperand *, const GArmV7OffsetOperand *);

/* Détermine le chemin conduisant à un opérande interne. */
static char *g_armv7_offset_operand_find_inner_operand_path(const GArmV7OffsetOperand *, const GArchOperand *);

/* Obtient l'opérande correspondant à un chemin donné. */
static GArchOperand *g_armv7_offset_operand_get_inner_operand_from_path(const GArmV7OffsetOperand *, const char *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_offset_operand_print(const GArmV7OffsetOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_offset_operand_unserialize(GArmV7OffsetOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_offset_operand_serialize(const GArmV7OffsetOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour un décalage relatif ARMv7. */
G_DEFINE_TYPE(GArmV7OffsetOperand, g_armv7_offset_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des décalages relatifs ARMv7.           *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_offset_operand_class_init(GArmV7OffsetOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_offset_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_offset_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->compare = (operand_compare_fc)g_armv7_offset_operand_compare;
    operand->find_inner = (find_inner_operand_fc)g_armv7_offset_operand_find_inner_operand_path;
    operand->get_inner = (get_inner_operand_fc)g_armv7_offset_operand_get_inner_operand_from_path;

    operand->print = (operand_print_fc)g_armv7_offset_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_offset_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_offset_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance de décalage relatif ARMv7.           *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_offset_operand_init(GArmV7OffsetOperand *operand)
{
    operand->value = NULL;

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

static void g_armv7_offset_operand_dispose(GArmV7OffsetOperand *operand)
{
    if (operand->value != NULL)
        g_object_unref(G_OBJECT(operand->value));

    G_OBJECT_CLASS(g_armv7_offset_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_offset_operand_finalize(GArmV7OffsetOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_offset_operand_parent_class)->finalize(G_OBJECT(operand));

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

static int g_armv7_offset_operand_compare(const GArmV7OffsetOperand *a, const GArmV7OffsetOperand *b)
{
    int result;                             /* Bilan à faire remonter      */

    result = sort_boolean(a->positive, b->positive);
    if (result != 0) goto gaooc_done;

    result = g_arch_operand_compare(a->value, b->value);

 gaooc_done:

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

static char *g_armv7_offset_operand_find_inner_operand_path(const GArmV7OffsetOperand *operand, const GArchOperand *target)
{
    char *result;                           /* Chemin à retourner          */

    if (target == operand->value)
        result = strdup("0");
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

static GArchOperand *g_armv7_offset_operand_get_inner_operand_from_path(const GArmV7OffsetOperand *operand, const char *path)
{
    GArchOperand *result;                   /* Opérande trouvée à renvoyer */

    result = NULL;

    if (strncmp(path, "0", 1) == 0)
        switch (path[1])
        {
            case '\0':
                result = operand->value;
                g_object_ref(G_OBJECT(result));
                break;

            case ':':
                result = g_arch_operand_get_inner_operand_from_path(operand->value, path + 1);
                break;

        }

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

static void g_armv7_offset_operand_print(const GArmV7OffsetOperand *operand, GBufferLine *line)
{
    if (!operand->positive)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "-", 1, RTT_KEY_WORD, NULL);

    g_arch_operand_print(operand->value, line);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : positive = indique si la quantité doit être ajoutée ou non.  *
*                value    = valeur du décalage à appliquer.                   *
*                                                                             *
*  Description : Crée un décalage selon un sens et une valeur donnés.         *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_offset_operand_new(bool positive, GArchOperand *value)
{
    GArmV7OffsetOperand *result;            /* Structure à retourner       */

    result = g_object_new(G_TYPE_ARMV7_OFFSET_OPERAND, NULL);

    result->positive = positive;
    result->value = value;

    return G_ARCH_OPERAND(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique le sens du décalage représenté.                      *
*                                                                             *
*  Retour      : Indication d'ajout ou de retrait.                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_armv7_offset_operand_is_positive(const GArmV7OffsetOperand *operand)
{
    return operand->positive;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Founit la valeur utilisée pour un décalage.                  *
*                                                                             *
*  Retour      : Opérande en place.                                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_offset_operand_get_value(const GArmV7OffsetOperand *operand)
{
    GArchOperand *result;                   /* Instance à retourner        */

    result = operand->value;

    g_object_ref(G_OBJECT(result));

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

static bool g_armv7_offset_operand_unserialize(GArmV7OffsetOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    GArchOperand *value;                    /* Valeur à intégrer           */
    uint8_t positive;                       /* Sens du décalage            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_offset_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
    {
        value = g_arch_operand_load(storage, format, pbuf);

        if (value == NULL)
            result = false;

        else
            operand->value = value;

    }

    if (result)
    {
        result = extract_packed_buffer(pbuf, &positive, sizeof(uint8_t), false);

        if (result)
            operand->positive = (positive == 1 ? true : false);

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

static bool g_armv7_offset_operand_serialize(const GArmV7OffsetOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t positive;                       /* Sens du décalage            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_offset_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
    {
        positive = (operand->positive ? 1 : 0);
        result = extend_packed_buffer(pbuf, &positive, sizeof(uint8_t), false);
    }

    if (result)
        result = g_arch_operand_store(operand->value, storage, pbuf);

    return result;

}
