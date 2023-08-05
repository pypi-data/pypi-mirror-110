
/* Chrysalide - Outil d'analyse de fichiers binaires
 * node-int.h - prototypes internes pour la définition d'un noeud Yaml
 *
 * Copyright (C) 2019-2020 Cyrille Bagard
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


#ifndef PLUGINS_YAML_NODE_INT_H
#define PLUGINS_YAML_NODE_INT_H


#include "node.h"



/* Recherche les noeuds correspondant à un chemin. */
typedef void (* find_yaml_node_fc) (const GYamlNode *, const char *, bool, GYamlNode ***, size_t *);


/* Noeud d'une arborescence au format Yaml (instance) */
struct _GYamlNode
{
    GObject parent;                         /* A laisser en premier        */

    GYamlLine *line;                        /* Line Yaml d'origine         */

};

/* Noeud d'une arborescence au format Yaml (classe) */
struct _GYamlNodeClass
{
    GObjectClass parent;                    /* A laisser en premier        */

    find_yaml_node_fc find;                 /* Recherche par chemin        */

};


/* Recherche les noeuds correspondant à un chemin. */
void _g_yaml_node_find_by_path(const GYamlNode *, const char *, bool, GYamlNode ***, size_t *);



#endif  /* PLUGINS_YAML_NODE_INT_H */
