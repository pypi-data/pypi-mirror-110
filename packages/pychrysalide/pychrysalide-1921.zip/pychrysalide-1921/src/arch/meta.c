
/* Chrysalide - Outil d'analyse de fichiers binaires
 * artificial.c - instructions pures vues de l'esprit
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


#include "meta.h"


#include <malloc.h>


#include "instruction-int.h"



/* ------------------------- INSTRUCTION INCONNUE / DONNEES ------------------------- */


/* Définition d'une instruction de rassemblement (instance) */
struct _GMetaInstruction
{
    GArchInstruction parent;                /* A laisser en premier        */

    GArchInstruction *fake;                 /* Instruction simulée         */

    GArchInstruction **children;            /* Instructions représentées   */
    size_t count;                           /* Taille de cette liste       */

};

/* Définition d'une instruction de rassemblement (classe) */
struct _GMetaInstructionClass
{
    GArchInstructionClass parent;           /* A laisser en premier        */

};


/* Initialise la classe des instructions de rassemblement. */
static void g_meta_instruction_class_init(GMetaInstructionClass *);

/* Initialise une instance d'instruction de rassemblement. */
static void g_meta_instruction_init(GMetaInstruction *);

/* Supprime toutes les références externes. */
static void g_meta_instruction_dispose(GMetaInstruction *);

/* Procède à la libération totale de la mémoire. */
static void g_meta_instruction_finalize(GMetaInstruction *);

/* Indique l'encodage d'une instruction de façon détaillée. */
static const char *g_meta_instruction_get_encoding(const GMetaInstruction *);

/* Fournit le nom humain de l'instruction manipulée. */
static const char *g_meta_instruction_get_keyword(const GMetaInstruction *);



/* -------------------- CONSERVATION SUR DISQUE DES INSTRUCTIONS -------------------- */


/* Charge une instruction depuis une mémoire tampon. */
static bool g_meta_instruction_unserialize(GMetaInstruction *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde une instruction dans une mémoire tampon. */
static bool g_meta_instruction_serialize(GMetaInstruction *, GAsmStorage *, packed_buffer_t *);



/* ---------------------------------------------------------------------------------- */
/*                           INSTRUCTION INCONNUE / DONNEES                           */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour une instruction inconnue d'architecture. */
G_DEFINE_TYPE(GMetaInstruction, g_meta_instruction, G_TYPE_ARCH_INSTRUCTION);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des instructions de rassemblement.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_meta_instruction_class_init(GMetaInstructionClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchInstructionClass *instr;           /* Encore une autre vision...  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_meta_instruction_dispose;
    object->finalize = (GObjectFinalizeFunc)g_meta_instruction_finalize;

    instr = G_ARCH_INSTRUCTION_CLASS(klass);

    instr->get_encoding = (get_instruction_encoding_fc)g_meta_instruction_get_encoding;
    instr->get_keyword = (get_instruction_keyword_fc)g_meta_instruction_get_keyword;

    instr->unserialize = (unserialize_instruction_fc)g_meta_instruction_unserialize;
    instr->serialize = (serialize_instruction_fc)g_meta_instruction_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instance à initialiser.                              *
*                                                                             *
*  Description : Initialise une instance d'instruction de rassemblement.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_meta_instruction_init(GMetaInstruction *instr)
{
    GArchInstruction *parent;               /* Version parente             */
    vmpa2t invalid;                         /* Absence de position         */

    parent = G_ARCH_INSTRUCTION(instr);

    init_vmpa(&invalid, VMPA_NO_PHYSICAL, VMPA_NO_VIRTUAL);
    init_mrange(&parent->range, &invalid, 0);

    instr->fake = NULL;

    instr->children = NULL;
    instr->count = 0;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instance d'objet GLib à traiter.                     *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_meta_instruction_dispose(GMetaInstruction *instr)
{
    size_t i;                               /* Boucle de parcours          */

    if (instr->fake != NULL)
        g_object_unref(G_OBJECT(instr->fake));

    for (i = 0; i < instr->count; i++)
        g_object_unref(G_OBJECT(instr->children[i]));

    G_OBJECT_CLASS(g_meta_instruction_parent_class)->dispose(G_OBJECT(instr));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instance d'objet GLib à traiter.                     *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_meta_instruction_finalize(GMetaInstruction *instr)
{
    if (instr->children != NULL)
        free(instr->children);

    G_OBJECT_CLASS(g_meta_instruction_parent_class)->finalize(G_OBJECT(instr));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : fake = instruction à simuler.                                *
*                                                                             *
*  Description : Crée une instruction rassemblant d'autres instructions.      *
*                                                                             *
*  Retour      : Instruction mise en place.                                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchInstruction *g_meta_instruction_new(GArchInstruction *fake)
{
    GMetaInstruction *result;               /* Instruction à retourner     */

    result = g_object_new(G_TYPE_META_INSTRUCTION, NULL);

    result->fake = fake;

    return G_ARCH_INSTRUCTION(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instruction quelconque à consulter.                  *
*                                                                             *
*  Description : Indique l'encodage d'une instruction de façon détaillée.     *
*                                                                             *
*  Retour      : Description humaine de l'encodage utilisé.                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static const char *g_meta_instruction_get_encoding(const GMetaInstruction *instr)
{
    const char *result;                     /* Description à retourner     */

    result = g_arch_instruction_get_encoding(instr->fake);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instruction d'assemblage à consulter.                *
*                                                                             *
*  Description : Fournit le nom humain de l'instruction manipulée.            *
*                                                                             *
*  Retour      : Mot clef de bas niveau.                                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static const char *g_meta_instruction_get_keyword(const GMetaInstruction *instr)
{
    const char *result;                     /* Désignation à renvoyer      */

    result = g_arch_instruction_get_keyword(instr->fake);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instruction d'assemblage à compléter.                *
*                child = instruction à intégrer au rassemblement.             *
*                last  = marque l'instruction comme étant la dernière du lot. *
*                                                                             *
*  Description : Intègre une nouvelle instruction dans un rassemblement.      *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_meta_instruction_add_child(GMetaInstruction *instr, GArchInstruction *child, bool last)
{
    GArchInstruction *parent;               /* Autre version de l'instruct°*/
    const mrange_t *base;                   /* Base d'une couverture       */
    vmpa2t start;                           /* Position de départ          */
    vmpa2t end;                             /* Position d'arrivée          */
    mrange_t range;                         /* Couverture nouvelle         */
    instr_link_t *links;                    /* Liens présents à copier     */
    size_t count;                           /* Quantité de ces liens       */
    size_t i;                               /* Boucle de parcours          */

    instr->children = (GArchInstruction **)realloc(instr->children,
                                                   ++instr->count * sizeof(GArchInstruction *));

    instr->children[instr->count - 1] = child;

    parent = G_ARCH_INSTRUCTION(instr);

    /* Mise à jour de la couverture totale */

    if (last)
    {
        if (instr->count == 1)
            g_arch_instruction_set_range(parent, g_arch_instruction_get_range(child));

        else
        {
            base = g_arch_instruction_get_range(instr->children[0]);
            copy_vmpa(&start, get_mrange_addr(base));

            base = g_arch_instruction_get_range(child);
            compute_mrange_end_addr(base, &end);

            init_mrange(&range, &start, compute_vmpa_diff(&start, &end));

            g_arch_instruction_set_range(parent, &range);

        }

    }

    /* Appropriation des liens contenus */

    links = g_arch_instruction_get_sources(child, &count);

    for (i = 0; i < count; i++)
    {
        if (instr->count == 1 || links[i].type == ILT_REF)
            g_arch_instruction_link_with(links[i].linked, parent, links[i].type);

        unref_instr_link((&links[i]));

    }

    if (links != NULL)
        free(links);

    links = g_arch_instruction_get_destinations(child, &count);

    for (i = 0; i < count; i++)
    {
        if (last || links[i].type == ILT_REF)
            g_arch_instruction_link_with(parent, links[i].linked, links[i].type);

        unref_instr_link((&links[i]));

    }

    if (links != NULL)
        free(links);

}



/* ---------------------------------------------------------------------------------- */
/*                      CONSERVATION SUR DISQUE DES INSTRUCTIONS                      */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : instr   = instruction d'assemblage à consulter.              *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                format  = format binaire chargé associé à l'architecture.    *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Charge une instruction depuis une mémoire tampon.            *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_meta_instruction_unserialize(GMetaInstruction *instr, GAsmStorage *storage, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchInstructionClass *parent;          /* Classe parente à consulter  */

    parent = G_ARCH_INSTRUCTION_CLASS(g_meta_instruction_parent_class);

    result = parent->unserialize(G_ARCH_INSTRUCTION(instr), storage, format, pbuf);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr   = instruction d'assemblage à consulter.              *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Sauvegarde une instruction dans une mémoire tampon.          *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_meta_instruction_serialize(GMetaInstruction *instr, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GArchInstructionClass *parent;          /* Classe parente à consulter  */

    parent = G_ARCH_INSTRUCTION_CLASS(g_meta_instruction_parent_class);

    result = parent->serialize(G_ARCH_INSTRUCTION(instr), storage, pbuf);

    return result;

}
