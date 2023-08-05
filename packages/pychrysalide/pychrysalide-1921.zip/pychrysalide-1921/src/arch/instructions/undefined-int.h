
/* Chrysalide - Outil d'analyse de fichiers binaires
 * undefined-int.h - prototypes pour la définition générique interne des instructions au comportement non défini
 *
 * Copyright (C) 2019 Cyrille Bagard
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


#ifndef _ARCH_INSTRUCTIONS_UNDEFINED_INT_H
#define _ARCH_INSTRUCTIONS_UNDEFINED_INT_H


#include "undefined.h"
#include "../instruction-int.h"
#include "../../glibext/objhole.h"



/* Informations glissées dans la structure GObject de GArchInstruction */
typedef union _undef_obj_extra
{
    struct
    {
        InstrExpectedBehavior behavior;     /* Conséquences réelles        */

    };

    gint lock;                              /* Gestion d'accès aux fanions */

} undef_obj_extra;

/* Définition générique d'une instruction au comportement non défini (instance) */
struct _GUndefInstruction
{
    GArchInstruction parent;                /* A laisser en premier        */

#if __SIZEOF_INT__ == __SIZEOF_LONG__

    /**
     * L'inclusion des informations suivantes dépend de l'architecture.
     *
     * Si la structure GObject possède un trou, on remplit de préférence
     * ce dernier.
     */

    undef_obj_extra extra;                  /* Externalisation embarquée   */

#endif

};

/**
 * Accès aux informations éventuellement déportées.
 */

#if __SIZEOF_INT__ == __SIZEOF_LONG__

#   define INIT_UNDEF_INSTR_EXTRA(ins) ins->extra.lock = 0

#   define GET_UNDEF_INSTR_EXTRA(ins) &ins->extra

#else

#   define INIT_UNDEF_INSTR_EXTRA(ins) INIT_GOBJECT_EXTRA(G_OBJECT(ins))

#   define GET_UNDEF_INSTR_EXTRA(ins) GET_GOBJECT_EXTRA(G_OBJECT(ins), undef_obj_extra)

#endif

/* Définition générique d'une instruction au comportement non défini (classe) */
struct _GUndefInstructionClass
{
    GArchInstructionClass parent;           /* A laisser en premier        */

};



#endif  /* _ARCH_INSTRUCTIONS_UNDEFINED_INT_H */
