
/* Chrysalide - Outil d'analyse de fichiers binaires
 * operand-int.h - prototypes pour la définition générique interne des opérandes
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


#ifndef _ARCH_OPERAND_INT_H
#define _ARCH_OPERAND_INT_H


#include "operand.h"



/* Compare un opérande avec un autre. */
typedef int (* operand_compare_fc) (const GArchOperand *, const GArchOperand *);

/* Détermine le chemin conduisant à un opérande interne. */
typedef char * (* find_inner_operand_fc) (const GArchOperand *, const GArchOperand *);

/* Obtient l'opérande correspondant à un chemin donné. */
typedef GArchOperand * (* get_inner_operand_fc) (const GArchOperand *, const char *);

/* Traduit un opérande en version humainement lisible. */
typedef void (* operand_print_fc) (const GArchOperand *, GBufferLine *);

/* Construit un petit résumé concis de l'opérande. */
typedef char * (* operand_build_tooltip_fc) (const GArchOperand *, const GLoadedBinary *);

/* Charge un opérande depuis une mémoire tampon. */
typedef bool (* unserialize_operand_fc) (GArchOperand *, GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
typedef bool (* serialize_operand_fc) (const GArchOperand *, GAsmStorage *, packed_buffer_t *);


/* Définition générique d'un opérande d'architecture (instance) */
struct _GArchOperand
{
    GObject parent;                         /* A laisser en premier        */

};


/* Définition générique d'un opérande d'architecture (classe) */
struct _GArchOperandClass
{
    GObjectClass parent;                    /* A laisser en premier        */

    operand_compare_fc compare;             /* Comparaison d'opérandes     */
    find_inner_operand_fc find_inner;       /* Définition d'un chemin      */
    get_inner_operand_fc get_inner;         /* Récupération d'un opérande  */

    operand_print_fc print;                 /* Texte humain équivalent     */
    operand_build_tooltip_fc build_tooltip; /* Construction de description */

    unserialize_operand_fc unserialize;     /* Chargement depuis un tampon */
    serialize_operand_fc serialize;         /* Conservation dans un tampon */

};



#endif  /* _ARCH_OPERAND_INT_H */
