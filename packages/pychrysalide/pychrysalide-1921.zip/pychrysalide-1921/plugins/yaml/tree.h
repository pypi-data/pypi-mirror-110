
/* Chrysalide - Outil d'analyse de fichiers binaires
 * tree.h - prototypes pour une ligne de contenu Yaml
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


#ifndef PLUGINS_YAML_TREE_H
#define PLUGINS_YAML_TREE_H


#include <glib-object.h>
#include <stdbool.h>


#include "line.h"
#include "node.h"



#define G_TYPE_YAML_TREE            g_yaml_tree_get_type()
#define G_YAML_TREE(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_YAML_TREE, GYamlTree))
#define G_IS_YAML_TREE(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_YAML_TREE))
#define G_YAML_TREE_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_YAML_TREE, GYamlTreeClass))
#define G_IS_YAML_TREE_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_YAML_TREE))
#define G_YAML_TREE_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_YAML_TREE, GYamlTreeClass))


/* Arborescence de lignes au format Yaml (instance) */
typedef struct _GYamlTree GYamlTree;

/* Arborescence de lignes au format Yaml (classe) */
typedef struct _GYamlTreeClass GYamlTreeClass;


/* Indique le type défini pour une arborescence de lignes au format Yaml. */
GType g_yaml_tree_get_type(void);

/* Construit une arborescence à partir de lignes Yaml. */
GYamlTree *g_yaml_tree_new(GYamlLine **, size_t);

/* Fournit le noeud constituant la racine d'arborescence Yaml. */
GYamlNode *g_yaml_tree_get_root(const GYamlTree *);

/* Recherche les noeuds correspondant à un chemin. */
void g_yaml_tree_find_by_path(const GYamlTree *, const char *, bool, GYamlNode ***, size_t *);

/* Recherche l'unique noeud correspondant à un chemin. */
GYamlNode *g_yaml_tree_find_one_by_path(GYamlTree *, const char *, bool);



#endif  /* PLUGINS_YAML_TREE_H */
