
/* Chrysalide - Outil d'analyse de fichiers binaires
 * meta.h - prototypes pour les instructions qui en rassemblent d'autres
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


#ifndef _ARCH_META_H
#define _ARCH_META_H


#include <glib-object.h>
#include <stdbool.h>


#include "instruction.h"



/* ------------------------- INSTRUCTION INCONNUE / DONNEES ------------------------- */


#define G_TYPE_META_INSTRUCTION            g_meta_instruction_get_type()
#define G_META_INSTRUCTION(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_META_INSTRUCTION, GMetaInstruction))
#define G_IS_META_INSTRUCTION(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_META_INSTRUCTION))
#define G_META_INSTRUCTION_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_META_INSTRUCTION, GMetaInstructionClass))
#define G_IS_META_INSTRUCTION_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_META_INSTRUCTION))
#define G_META_INSTRUCTION_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_META_INSTRUCTION, GMetaInstructionClass))


/* Définition d'une instruction de rassemblement (instance) */
typedef struct _GMetaInstruction GMetaInstruction;

/* Définition d'une instruction de rassemblement (classe) */
typedef struct _GMetaInstructionClass GMetaInstructionClass;


/* Indique le type défini pour une instruction inconnue d'architecture. */
GType g_meta_instruction_get_type(void);

/* Crée une instruction rassemblant d'autres instructions. */
GArchInstruction *g_meta_instruction_new(GArchInstruction *);

/* Intègre une nouvelle instruction dans un rassemblement. */
void g_meta_instruction_add_child(GMetaInstruction *, GArchInstruction *, bool);



#endif  /* _ARCH_META_H */
