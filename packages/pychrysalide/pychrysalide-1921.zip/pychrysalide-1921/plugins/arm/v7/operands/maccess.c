
/* Chrysalide - Outil d'analyse de fichiers binaires
 * maccess.c - accès à la mémorie à partir d'un registre et d'un décalage
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


#include "maccess.h"


#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


#include <arch/operand-int.h>
#include <common/cpp.h>
#include <common/sort.h>
#include <core/logs.h>
#include <gtkext/gtkblockdisplay.h>



/* Définition d'un opérande offrant un accès à la mémoire depuis une base (instance) */
struct _GArmV7MAccessOperand
{
    GArchOperand parent;                    /* Instance parente            */

    GArchOperand *base;                     /* Base de l'accès en mémoire  */
    GArchOperand *offset;                   /* Décalage pour l'adresse     */
    GArchOperand *shift;                    /* Décalage supplémentaire ?   */
    bool post_indexed;                      /* Position du décalage        */
    bool write_back;                        /* Mise à jour de la base      */

};


/* Définition d'un opérande offrant un accès à la mémoire depuis une base (classe) */
struct _GArmV7MAccessOperandClass
{
    GArchOperandClass parent;               /* Classe parente              */

};


/* Initialise la classe des accès à la mémoire chez ARM. */
static void g_armv7_maccess_operand_class_init(GArmV7MAccessOperandClass *);

/* Initialise une instance d'accès à la mémoire chez ARM. */
static void g_armv7_maccess_operand_init(GArmV7MAccessOperand *);

/* Supprime toutes les références externes. */
static void g_armv7_maccess_operand_dispose(GArmV7MAccessOperand *);

/* Procède à la libération totale de la mémoire. */
static void g_armv7_maccess_operand_finalize(GArmV7MAccessOperand *);

/* Compare un opérande avec un autre. */
static int g_armv7_maccess_operand_compare(const GArmV7MAccessOperand *, const GArmV7MAccessOperand *);

/* Détermine le chemin conduisant à un opérande interne. */
static char *g_armv7_maccess_operand_find_inner_operand_path(const GArmV7MAccessOperand *, const GArchOperand *);

/* Obtient l'opérande correspondant à un chemin donné. */
static GArchOperand *g_armv7_maccess_operand_get_inner_operand_from_path(const GArmV7MAccessOperand *, const char *);

/* Traduit un opérande en version humainement lisible. */
static void g_armv7_maccess_operand_print(const GArmV7MAccessOperand *, GBufferLine *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Charge un opérande depuis une mémoire tampon. */
static bool g_armv7_maccess_operand_unserialize(GArmV7MAccessOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
static bool g_armv7_maccess_operand_serialize(const GArmV7MAccessOperand *, GAsmStorage *, packed_buffer_t *);



/* Indique le type défini par la GLib pour un accès à la mémoire depuis une base. */
G_DEFINE_TYPE(GArmV7MAccessOperand, g_armv7_maccess_operand, G_TYPE_ARCH_OPERAND);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des accès à la mémoire chez ARM.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_maccess_operand_class_init(GArmV7MAccessOperandClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchOperandClass *operand;             /* Version de classe parente   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_armv7_maccess_operand_dispose;
    object->finalize = (GObjectFinalizeFunc)g_armv7_maccess_operand_finalize;

    operand = G_ARCH_OPERAND_CLASS(klass);

    operand->compare = (operand_compare_fc)g_armv7_maccess_operand_compare;
    operand->find_inner = (find_inner_operand_fc)g_armv7_maccess_operand_find_inner_operand_path;
    operand->get_inner = (get_inner_operand_fc)g_armv7_maccess_operand_get_inner_operand_from_path;

    operand->print = (operand_print_fc)g_armv7_maccess_operand_print;

    operand->unserialize = (unserialize_operand_fc)g_armv7_maccess_operand_unserialize;
    operand->serialize = (serialize_operand_fc)g_armv7_maccess_operand_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = instance à initialiser.                            *
*                                                                             *
*  Description : Initialise une instance d'accès à la mémoire chez ARM.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_armv7_maccess_operand_init(GArmV7MAccessOperand *operand)
{
    operand->base = NULL;
    operand->offset = NULL;
    operand->shift = NULL;

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

static void g_armv7_maccess_operand_dispose(GArmV7MAccessOperand *operand)
{
    if (operand->base != NULL)
        g_object_unref(G_OBJECT(operand->base));

    if (operand->offset != NULL)
        g_object_unref(G_OBJECT(operand->offset));

    if (operand->shift != NULL)
        g_object_unref(G_OBJECT(operand->shift));

    G_OBJECT_CLASS(g_armv7_maccess_operand_parent_class)->dispose(G_OBJECT(operand));

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

static void g_armv7_maccess_operand_finalize(GArmV7MAccessOperand *operand)
{
    G_OBJECT_CLASS(g_armv7_maccess_operand_parent_class)->finalize(G_OBJECT(operand));

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

static int g_armv7_maccess_operand_compare(const GArmV7MAccessOperand *a, const GArmV7MAccessOperand *b)
{
    int result;                             /* Bilan à faire remonter      */

    result = g_arch_operand_compare(a->base, b->base);
    if (result != 0) goto gamoc_done;

    result = sort_pointer(a->offset, b->offset, (__compar_fn_t)g_arch_operand_compare);
    if (result != 0) goto gamoc_done;

    result = sort_pointer(a->shift, b->shift, (__compar_fn_t)g_arch_operand_compare);
    if (result != 0) goto gamoc_done;

    result = sort_boolean(a->post_indexed, b->post_indexed);
    if (result != 0) goto gamoc_done;

    result = sort_boolean(a->write_back, b->write_back);

 gamoc_done:

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

static char *g_armv7_maccess_operand_find_inner_operand_path(const GArmV7MAccessOperand *operand, const GArchOperand *target)
{
    char *result;                           /* Chemin à retourner          */
    size_t count;                           /* Nombre d'opérandes en place */
    size_t i;                               /* Boucle de parcours          */
    int ret;                                /* Bilan d'une construction    */
    char *sub_path;                         /* Sous-chemin emprunté        */

    GArchOperand *candidates[] = { operand->base, operand->offset, operand->shift };

    result = NULL;

    count = ARRAY_SIZE(candidates);

    /* Première passe : accès direct */

    for (i = 0; i < count && result == NULL; i++)
    {
        if (candidates[i] == NULL)
            continue;

        if (candidates[i] == target)
        {
            ret = asprintf(&result, "%zu", i);
            if (ret == -1)
            {
                LOG_ERROR_N("asprintf");
                result = NULL;
            }
        }

    }

    /* Seconde passe : accès profond */

    for (i = 0; i < count && result == NULL; i++)
    {
        if (candidates[i] == NULL)
            continue;

        sub_path = g_arch_operand_find_inner_operand_path(candidates[i], target);

        if (sub_path != NULL)
        {
            ret = asprintf(&result, "%zu:%s", i, sub_path);
            if (ret == -1)
            {
                LOG_ERROR_N("asprintf");
                result = NULL;
            }

            free(sub_path);

        }

    }

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

static GArchOperand *g_armv7_maccess_operand_get_inner_operand_from_path(const GArmV7MAccessOperand *operand, const char *path)
{
    GArchOperand *result;                   /* Opérande trouvée à renvoyer */
    size_t index;                           /* Indice de l'opérande visé   */
    char *end;                              /* Poursuite du parcours ?     */
    GArchOperand *found;                    /* Opérande trouvé             */

    GArchOperand *candidates[] = { operand->base, operand->offset, operand->shift };

    result = NULL;

    /* Recherche au premier niveau */

    index = strtoul(path, &end, 10);

    if ((index == ULONG_MAX && errno == ERANGE) || (index == 0 && errno == EINVAL))
    {
        LOG_ERROR_N("strtoul");
        goto done;
    }

    if (index >= ARRAY_SIZE(candidates))
        goto done;

    found = candidates[index];
    if (found == NULL) goto done;

    if (*end == '\0')
    {
        result = found;
        g_object_ref(G_OBJECT(result));
        goto done;
    }

    /* Recherche en profondeur */

    assert(*end == ':');

    result = g_arch_operand_get_inner_operand_from_path(found, end + 1);

 done:

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

static void g_armv7_maccess_operand_print(const GArmV7MAccessOperand *operand, GBufferLine *line)
{
    g_buffer_line_append_text(line, DLC_ASSEMBLY, "[", 1, RTT_HOOK, NULL);

    g_arch_operand_print(operand->base, line);

    if (operand->post_indexed)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "]", 1, RTT_HOOK, NULL);

    if (operand->offset != NULL)
    {
        g_buffer_line_append_text(line, DLC_ASSEMBLY, ",", 1, RTT_PUNCT, NULL);
        g_buffer_line_append_text(line, DLC_ASSEMBLY, " ", 1, RTT_RAW, NULL);

        g_arch_operand_print(operand->offset, line);

    }

    if (operand->shift != NULL)
    {
        g_buffer_line_append_text(line, DLC_ASSEMBLY, ",", 1, RTT_PUNCT, NULL);
        g_buffer_line_append_text(line, DLC_ASSEMBLY, " ", 1, RTT_RAW, NULL);

        g_arch_operand_print(operand->shift, line);

    }

    if (!operand->post_indexed)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "]", 1, RTT_HOOK, NULL);

    if (operand->post_indexed && operand->write_back)
        g_buffer_line_append_text(line, DLC_ASSEMBLY, "!", 1, RTT_PUNCT, NULL);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : base   = représente le registre de la base d'accès.          *
*                offset = détermine le décalage entre l'adresse et la base.   *
*                shift  = opération de décalage pour jouer sur le décalage.   *
*                post   = précise la forme donnée au décalage à appliquer.    *
*                wback  = indique une mise à jour de la base après usage.     *
*                                                                             *
*  Description : Crée un accès à la mémoire depuis une base et un décalage.   *
*                                                                             *
*  Retour      : Opérande mis en place.                                       *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_maccess_operand_new(GArchOperand *base, GArchOperand *offset, GArchOperand *shift, bool post, bool wback)
{
    GArmV7MAccessOperand *result;           /* Structure à retourner       */

    result = g_object_new(G_TYPE_ARMV7_MACCESS_OPERAND, NULL);

    result->base = base;
    result->offset = offset;
    result->shift = shift;

    result->post_indexed = post;
    result->write_back = wback;

    return G_ARCH_OPERAND(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Founit la base d'un accès à la mémoire.                      *
*                                                                             *
*  Retour      : Opérande en place.                                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_maccess_operand_get_base(const GArmV7MAccessOperand *operand)
{
    return operand->base;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Founit le décalage d'un accès à la mémoire depuis la base.   *
*                                                                             *
*  Retour      : Opérande en place.                                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_maccess_operand_get_offset(const GArmV7MAccessOperand *operand)
{
    return operand->offset;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Founit le décalage d'un décalage pour un accès mémoire.      *
*                                                                             *
*  Retour      : Opérande en place.                                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchOperand *g_armv7_maccess_operand_get_shift(const GArmV7MAccessOperand *operand)
{
    return operand->shift;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique si le décalage est post-indexé.                      *
*                                                                             *
*  Retour      : Statut des opérations menées.                                *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_armv7_maccess_operand_is_post_indexed(const GArmV7MAccessOperand *operand)
{
    return operand->post_indexed;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : operand = opérande à consulter.                              *
*                                                                             *
*  Description : Indique si la base est mise à jour après usage.              *
*                                                                             *
*  Retour      : Statut des opérations menées.                                *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_armv7_maccess_operand_has_to_write_back(const GArmV7MAccessOperand *operand)
{
    return operand->write_back;

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

static bool g_armv7_maccess_operand_unserialize(GArmV7MAccessOperand *operand, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    GArchOperand *subop;                    /* Sous-opérande à intégrer    */
    uint8_t boolean;                        /* Valeur booléenne            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_maccess_operand_parent_class);

    result = parent->unserialize(G_ARCH_OPERAND(operand), storage, format, pbuf);

    if (result)
    {
        subop = g_arch_operand_load(storage, format, pbuf);

        if (subop == NULL)
            result = false;

        else
            operand->base = subop;

    }

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result && boolean == 1)
        {
            subop = g_arch_operand_load(storage, format, pbuf);

            if (subop == NULL)
                result = false;

            else
                operand->offset = subop;

        }

    }

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result && boolean == 1)
        {
            subop = g_arch_operand_load(storage, format, pbuf);

            if (subop == NULL)
                result = false;

            else
                operand->shift = subop;

        }

    }

    if (result)
    {
        result = extract_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);

        if (result)
            operand->post_indexed = (boolean == 1 ? true : false);

    }

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

static bool g_armv7_maccess_operand_serialize(const GArmV7MAccessOperand *operand, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchOperandClass *parent;              /* Classe parente à consulter  */
    uint8_t boolean;                        /* Valeur booléenne            */

    parent = G_ARCH_OPERAND_CLASS(g_armv7_maccess_operand_parent_class);

    result = parent->serialize(G_ARCH_OPERAND(operand), storage, pbuf);

    if (result)
        result = g_arch_operand_store(operand->base, storage, pbuf);

    if (result)
    {
        if (operand->offset == NULL)
            result = extend_packed_buffer(pbuf, (uint8_t []) { 0 }, sizeof(uint8_t), false);

        else
        {
            result = extend_packed_buffer(pbuf, (uint8_t []) { 1 }, sizeof(uint8_t), false);

            if (result)
                result = g_arch_operand_store(operand->offset, storage, pbuf);

        }

    }

    if (result)
    {
        if (operand->shift == NULL)
            result = extend_packed_buffer(pbuf, (uint8_t []) { 0 }, sizeof(uint8_t), false);

        else
        {
            result = extend_packed_buffer(pbuf, (uint8_t []) { 1 }, sizeof(uint8_t), false);

            if (result)
                result = g_arch_operand_store(operand->shift, storage, pbuf);

        }

    }

    if (result)
    {
        boolean = (operand->post_indexed ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    if (result)
    {
        boolean = (operand->write_back ? 1 : 0);
        result = extend_packed_buffer(pbuf, &boolean, sizeof(uint8_t), false);
    }

    return result;

}
