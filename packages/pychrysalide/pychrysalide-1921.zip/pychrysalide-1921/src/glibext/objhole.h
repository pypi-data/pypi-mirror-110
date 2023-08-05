
/* Chrysalide - Outil d'analyse de fichiers binaires
 * objhole.h - prototypes pour l'utilisation d'un espace inutilisé dans la structure GObject
 *
 * Copyright (C) 2020 Cyrille Bagard
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


#ifndef _GLIBEXT_OBJHOLE_H
#define _GLIBEXT_OBJHOLE_H


#include <glib-object.h>


#include "../common/cpp.h"



/**
 * Une structure GObject a la définition suivante :
 *
 *    struct  _GObject
 *    {
 *        GTypeInstance  g_type_instance;
 *        volatile guint ref_count;
 *        GData          *qdata;
 *    };
 *
 * L'espace entre les deux derniers champs est exploité ici.
 */


#define INIT_GOBJECT_EXTRA(obj)                                 \
    do                                                          \
    {                                                           \
        guint *___space;                                        \
        ___space = (((guint *)&obj->ref_count) + 1);            \
        BUILD_BUG_ON((___space + 1) == (guint *)&obj->qdata);   \
        *___space = 0;                                          \
    }                                                           \
    while (0)


#define GET_GOBJECT_EXTRA(obj, tp)                              \
    ({                                                          \
        BUILD_BUG_ON(sizeof(tp) > sizeof(guint));               \
        tp *___result;                                          \
        ___result = (tp *)(((guint *)&obj->ref_count) + 1);     \
        BUILD_BUG_ON((___result + 1) == (tp *)&obj->qdata);     \
        ___result;                                              \
    })



/**
 * Choix du bit de verrou pour le champ "lock".
 *
 * Dans la structure exploitant le mot utilisé ici, ce verrou est généralement
 * placé dans le bit de poids fort pour les objets qui l'utilisent.
 */

#if __BYTE_ORDER == __LITTLE_ENDIAN

#   define HOLE_LOCK_BIT 31

#elif __BYTE_ORDER == __BIG_ENDIAN

#   define HOLE_LOCK_BIT 0

#else

#   error "Unknown byte order"

#endif



#endif  /* _GLIBEXT_OBJHOLE_H */
