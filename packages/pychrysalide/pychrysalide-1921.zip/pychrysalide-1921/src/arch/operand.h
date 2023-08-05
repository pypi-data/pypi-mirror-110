
/* Chrysalide - Outil d'analyse de fichiers binaires
 * operand.h - prototypes pour la gestion générique des opérandes
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


#ifndef _ARCH_OPERAND_H
#define _ARCH_OPERAND_H


#include <glib-object.h>


#include "../common/packed.h"
#include "../format/format.h"
#include "../glibext/bufferline.h"



/* ------------------------ DEFINITION D'OPERANDE QUELCONQUE ------------------------ */


/* Depuis "../analysis/binary.h" : description de fichier binaire */
typedef struct _GLoadedBinary GLoadedBinary;


#define G_TYPE_ARCH_OPERAND            g_arch_operand_get_type()
#define G_ARCH_OPERAND(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_ARCH_OPERAND, GArchOperand))
#define G_IS_ARCH_OPERAND(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_ARCH_OPERAND))
#define G_ARCH_OPERAND_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_ARCH_OPERAND, GArchOperandClass))
#define G_IS_ARCH_OPERAND_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_ARCH_OPERAND))
#define G_ARCH_OPERAND_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_ARCH_OPERAND, GArchOperandClass))


/* Définition générique d'un opérande d'architecture (instance) */
typedef struct _GArchOperand GArchOperand;

/* Définition générique d'un opérande d'architecture (classe) */
typedef struct _GArchOperandClass GArchOperandClass;


/* Indique le type défini pour un opérande d'architecture. */
GType g_arch_operand_get_type(void);

/* Compare un opérande avec un autre. */
int g_arch_operand_compare(const GArchOperand *, const GArchOperand *);

/* Détermine le chemin conduisant à un opérande interne. */
char *g_arch_operand_find_inner_operand_path(const GArchOperand *, const GArchOperand *);

/* Obtient l'opérande correspondant à un chemin donné. */
GArchOperand *g_arch_operand_get_inner_operand_from_path(const GArchOperand *, const char *);

/* Traduit un opérande en version humainement lisible. */
void g_arch_operand_print(const GArchOperand *, GBufferLine *);

/* Construit un petit résumé concis de l'opérande. */
char *g_arch_operand_build_tooltip(const GArchOperand *, const GLoadedBinary *);



/* --------------------- TRANSPOSITIONS VIA CACHE DES OPERANDES --------------------- */


/* Depuis "storage.h" : définition d'une conservation d'instructions d'assemblage (instance) */
typedef struct _GAsmStorage GAsmStorage;


/* Charge un opérande depuis une mémoire tampon. */
GArchOperand *g_arch_operand_load(GAsmStorage *, GBinFormat *, packed_buffer_t *);

/* Sauvegarde un opérande dans une mémoire tampon. */
bool g_arch_operand_store(const GArchOperand *, GAsmStorage *, packed_buffer_t *);



#endif  /* _ARCH_OPERAND_H */
