
/* Chrysalide - Outil d'analyse de fichiers binaires
 * symbol-int.h - prototypes pour la définition interne des symboles dans un binaire
 *
 * Copyright (C) 2017-2019 Cyrille Bagard
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


#ifndef _FORMAT_SYMBOL_INT_H
#define _FORMAT_SYMBOL_INT_H


#include "symbol.h"
#include "../glibext/objhole.h"



/* Fournit une étiquette pour viser un symbole. */
typedef char * (* get_symbol_label_fc) (const GBinSymbol *);


/* Informations glissées dans la structure GObject de GBinSymbol */
typedef union _sym_obj_extra
{
    struct
    {
        SymbolType stype;                   /* Type du symbole             */
        SymbolStatus status;                /* Visibilité du symbole       */

        char nm_prefix;                     /* Eventuel préfixe "nm"       */

        SymbolFlag flags;                   /* Informations complémentaires*/

    };

    gint lock;                              /* Gestion d'accès aux fanions */

} sym_obj_extra;

/* Symbole d'exécutable (instance) */
struct _GBinSymbol
{
    GObject parent;                         /* A laisser en premier        */

    mrange_t range;                         /* Couverture mémoire          */

    char *alt;                              /* Nom alternatif              */

#if __SIZEOF_INT__ == __SIZEOF_LONG__

    /**
     * L'inclusion des informations suivantes dépend de l'architecture.
     *
     * Si la structure GObject possède un trou, on remplit de préférence
     * ce dernier.
     */

    sym_obj_extra extra;                    /* Externalisation embarquée   */

#endif

};

/**
 * Accès aux informations éventuellement déportées.
 */

#if __SIZEOF_INT__ == __SIZEOF_LONG__

#   define INIT_BIN_SYMBOL_EXTRA(sym) sym->extra.lock = 0

#   define GET_BIN_SYMBOL_EXTRA(sym) &sym->extra

#else

#   define INIT_BIN_SYMBOL_EXTRA(sym) INIT_GOBJECT_EXTRA(G_OBJECT(sym))

#   define GET_BIN_SYMBOL_EXTRA(sym) GET_GOBJECT_EXTRA(G_OBJECT(sym), sym_obj_extra)

#endif

/* Symbole d'exécutable (classe) */
struct _GBinSymbolClass
{
    GObjectClass parent;                    /* A laisser en premier        */

    get_symbol_label_fc get_label;          /* Obtention d'une étiquette   */

};



#endif  /* _FORMAT_SYMBOL_INT_H */
