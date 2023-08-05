
/* Chrysalide - Outil d'analyse de fichiers binaires
 * registers.c - aides auxiliaires relatives aux registres Dalvik
 *
 * Copyright (C) 2012-2018 Cyrille Bagard
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
#include "storage.h"



/* ---------------------------- PUR REGISTRE DU MATERIEL ---------------------------- */


/* Initialise la classe des registres. */
static void g_arch_register_class_init(GArchRegisterClass *);

/* Initialise une instance de registre. */
static void g_arch_register_init(GArchRegister *);

/* Supprime toutes les références externes. */
static void g_arch_register_dispose(GArchRegister *);

/* Procède à la libération totale de la mémoire. */
static void g_arch_register_finalize(GArchRegister *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES REGISTRES --------------------- */


/* Charge un registre depuis une mémoire tampon. */
static GArchRegister *g_arch_register_unserialize(GArchRegister *, GAsmStorage *, packed_buffer_t *);

/* Sauvegarde un registre dans une mémoire tampon. */
static bool g_arch_register_serialize(const GArchRegister *, GAsmStorage *, packed_buffer_t *);



/* ---------------------------------------------------------------------------------- */
/*                              PUR REGISTRE DU MATERIEL                              */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour une représentation d'un registre. */
G_DEFINE_TYPE(GArchRegister, g_arch_register, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des registres.                          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_arch_register_class_init(GArchRegisterClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_arch_register_dispose;
    object->finalize = (GObjectFinalizeFunc)g_arch_register_finalize;

    klass->unserialize = (reg_unserialize_fc)g_arch_register_unserialize;
    klass->serialize = (reg_serialize_fc)g_arch_register_serialize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = instance à initialiser.                                *
*                                                                             *
*  Description : Initialise une instance de registre.                         *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_arch_register_init(GArchRegister *reg)
{

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = instance d'objet GLib à traiter.                       *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_arch_register_dispose(GArchRegister *reg)
{
    G_OBJECT_CLASS(g_arch_register_parent_class)->dispose(G_OBJECT(reg));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = instance d'objet GLib à traiter.                       *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_arch_register_finalize(GArchRegister *reg)
{
    G_OBJECT_CLASS(g_arch_register_parent_class)->finalize(G_OBJECT(reg));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = opérande à consulter pour le calcul.                   *
*                                                                             *
*  Description : Produit une empreinte à partir d'un registre.                *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

guint g_arch_register_hash(const GArchRegister *reg)
{
    return G_ARCH_REGISTER_GET_CLASS(reg)->hash(reg);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : a = premier registre à consulter.                            *
*                b = second registre à consulter.                             *
*                                                                             *
*  Description : Compare un registre avec un autre.                           *
*                                                                             *
*  Retour      : Bilan de la comparaison.                                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int g_arch_register_compare(const GArchRegister *a, const GArchRegister *b)
{
    return G_ARCH_REGISTER_GET_CLASS(a)->compare(a, b);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg  = registre à transcrire.                                *
*                line = ligne tampon où imprimer l'opérande donné.            *
*                                                                             *
*  Description : Traduit un registre en version humainement lisible.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_arch_register_print(const GArchRegister *reg, GBufferLine *line)
{
    G_ARCH_REGISTER_GET_CLASS(reg)->print(reg, line);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = registre à consulter.                                  *
*                                                                             *
*  Description : Indique si le registre correspond à ebp ou similaire.        *
*                                                                             *
*  Retour      : true si la correspondance est avérée, false sinon.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_arch_register_is_base_pointer(const GArchRegister *reg)
{
    bool result;                            /* Bilan à renvoyer            */

    if (G_ARCH_REGISTER_GET_CLASS(reg)->is_bp != NULL)
        result = G_ARCH_REGISTER_GET_CLASS(reg)->is_bp(reg);
    else
        result = false;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg = registre à consulter.                                  *
*                                                                             *
*  Description : Indique si le registre correspond à esp ou similaire.        *
*                                                                             *
*  Retour      : true si la correspondance est avérée, false sinon.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_arch_register_is_stack_pointer(const GArchRegister *reg)
{
    bool result;                            /* Bilan à renvoyer            */

    if (G_ARCH_REGISTER_GET_CLASS(reg)->is_sp != NULL)
        result = G_ARCH_REGISTER_GET_CLASS(reg)->is_sp(reg);
    else
        result = false;

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                       TRANSPOSITIONS VIA CACHE DES REGISTRES                       */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : reg     = registre d'architecture à constituer.              *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Charge un registre depuis une mémoire tampon.                *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static GArchRegister *g_arch_register_unserialize(GArchRegister *reg, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    GArchRegister *result;                  /* Instance à retourner        */

    result = reg;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : storage = mécanisme de sauvegarde à manipuler.               *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Charge un registre depuis une mémoire tampon.                *
*                                                                             *
*  Retour      : Registre d'architecture constitué ou NULL en cas d'échec.    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GArchRegister *g_arch_register_load(GAsmStorage *storage, packed_buffer_t *pbuf)
{
    GArchRegister *result;                  /* Instance à retourner        */
    GArchRegister *dummy;                   /* Patron du type de registre  */

    dummy = G_ARCH_REGISTER(g_asm_storage_create_object(storage, pbuf));

    if (dummy != NULL)
    {
        result = G_ARCH_REGISTER_GET_CLASS(dummy)->unserialize(dummy, storage, pbuf);

        /* Si personne ne l'a fait avant... */
        if (result != NULL)
            g_object_unref(G_OBJECT(dummy));

    }

    else
        result = NULL;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg     = registre d'architecture à consulter.               *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Sauvegarde un registre dans une mémoire tampon.              *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_arch_register_serialize(const GArchRegister *reg, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */

    result = true;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reg     = registre d'architecture à consulter.               *
*                storage = mécanisme de sauvegarde à manipuler.               *
*                pbuf    = zone tampon à remplir.                             *
*                                                                             *
*  Description : Sauvegarde un registre dans une mémoire tampon.              *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_arch_register_store(const GArchRegister *reg, GAsmStorage *storage, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */

    result = g_asm_storage_store_object_gtype(storage, G_OBJECT(reg), pbuf);

    if (result)
        result = G_ARCH_REGISTER_GET_CLASS(reg)->serialize(reg, storage, pbuf);

    return result;

}
