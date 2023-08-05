
/* Chrysalide - Outil d'analyse de fichiers binaires
 * scalar.h - prototypes pour un noeud Yaml de type "scalar"
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


#ifndef PLUGINS_YAML_SCALAR_H
#define PLUGINS_YAML_SCALAR_H


#include <glib-object.h>
#include <stdbool.h>


#include "line.h"
#include "node.h"


/* Depuis collection.h : collection de noeuds au format Yaml (instance) */
typedef struct _GYamlCollection GYamlCollection;


#define G_TYPE_YAML_SCALAR            g_yaml_scalar_get_type()
#define G_YAML_SCALAR(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_YAML_SCALAR, GYamlScalar))
#define G_IS_YAML_SCALAR(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_YAML_SCALAR))
#define G_YAML_SCALAR_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_YAML_SCALAR, GYamlScalarClass))
#define G_IS_YAML_SCALAR_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_YAML_SCALAR))
#define G_YAML_SCALAR_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_YAML_SCALAR, GYamlScalarClass))


/* Noeud d'une arborescence au format Yaml (instance) */
typedef struct _GYamlScalar GYamlScalar;

/* Noeud d'une arborescence au format Yaml (classe) */
typedef struct _GYamlScalarClass GYamlScalarClass;


/* Indique le type défini pour un noeud d'arborescence Yaml. */
GType g_yaml_scalar_get_type(void);

/* Construit un noeud d'arborescence Yaml. */
GYamlScalar *g_yaml_scalar_new(GYamlLine *);

/* Fournit la ligne principale associée à un noeud. */
GYamlLine *g_yaml_scalar_get_yaml_line(const GYamlScalar *);

/* Attache une collection de noeuds Yaml à un noeud. */
void g_yaml_scalar_set_collection(GYamlScalar *, GYamlCollection *);

/* Fournit une éventuelle collection rattachée à un noeud. */
GYamlCollection *g_yaml_scalar_get_collection(const GYamlScalar *);



#endif  /* PLUGINS_YAML_SCALAR_H */
