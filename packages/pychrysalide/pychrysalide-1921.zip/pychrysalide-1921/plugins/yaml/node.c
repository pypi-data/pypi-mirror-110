
/* Chrysalide - Outil d'analyse de fichiers binaires
 * node.c - définition de noeud Yaml
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


#include "node.h"


#include <string.h>


#include "node-int.h"



/* Initialise la classe des noeuds d'arborescence Yaml. */
static void g_yaml_node_class_init(GYamlNodeClass *);

/* Initialise une instance de noeud d'arborescence Yaml. */
static void g_yaml_node_init(GYamlNode *);

/* Supprime toutes les références externes. */
static void g_yaml_node_dispose(GYamlNode *);

/* Procède à la libération totale de la mémoire. */
static void g_yaml_node_finalize(GYamlNode *);



/* Indique le type défini pour un noeud d'arborescence Yaml. */
G_DEFINE_TYPE(GYamlNode, g_yaml_node, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des noeuds d'arborescence Yaml.         *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_node_class_init(GYamlNodeClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_yaml_node_dispose;
    object->finalize = (GObjectFinalizeFunc)g_yaml_node_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = instance à initialiser.                               *
*                                                                             *
*  Description : Initialise une instance de noeud d'arborescence Yaml.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_node_init(GYamlNode *node)
{
    node->line = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = instance d'objet GLib à traiter.                      *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_node_dispose(GYamlNode *node)
{
    g_clear_object(&node->line);

    G_OBJECT_CLASS(g_yaml_node_parent_class)->dispose(G_OBJECT(node));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = instance d'objet GLib à traiter.                      *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_node_finalize(GYamlNode *node)
{
    G_OBJECT_CLASS(g_yaml_node_parent_class)->finalize(G_OBJECT(node));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = noeud d'arborescence Yaml à consulter.                *
*                                                                             *
*  Description : Fournit la ligne d'origine associée à un noeud.              *
*                                                                             *
*  Retour      : Ligne Yaml à l'origine du noeud.                             *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlLine *g_yaml_node_get_yaml_line(const GYamlNode *node)
{
    GYamlLine *result;                      /* Ligne d'origine à renvoyer  */

    result = node->line;

    if (result != NULL)
        g_object_ref(G_OBJECT(result));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node    = noeud d'arborescence Yaml à consulter.             *
*                path    = chemin d'accès à parcourir.                        *
*                prepare = indication sur une préparation d'un prochain appel.*
*                nodes   = liste de noeuds avec correspondance établie. [OUT] *
*                count   = quantité de ces noeuds. [OUT]                      *
*                                                                             *
*  Description : Recherche les noeuds correspondant à un chemin.              *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void _g_yaml_node_find_by_path(const GYamlNode *node, const char *path, bool prepare, GYamlNode ***nodes, size_t *count)
{
    GYamlNodeClass *class;                  /* Classe de l'instance        */

    class = G_YAML_NODE_GET_CLASS(node);

    class->find(node, path, prepare, nodes, count);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node    = noeud d'arborescence Yaml à consulter.             *
*                path    = chemin d'accès à parcourir.                        *
*                prepare = indication sur une préparation d'un prochain appel.*
*                nodes   = liste de noeuds avec correspondance établie. [OUT] *
*                count   = quantité de ces noeuds. [OUT]                      *
*                                                                             *
*  Description : Recherche les noeuds correspondant à un chemin.              *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_yaml_node_find_by_path(const GYamlNode *node, const char *path, bool prepare, GYamlNode ***nodes, size_t *count)
{
    *nodes = NULL;
    *count = 0;

    _g_yaml_node_find_by_path(node, path, prepare, nodes, count);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node    = noeud d'arborescence Yaml à consulter.             *
*                path    = chemin d'accès à parcourir.                        *
*                prepare = indication sur une préparation d'un prochain appel.*
*                                                                             *
*  Description : Recherche l'unique noeud correspondant à un chemin.          *
*                                                                             *
*  Retour      : Noeud avec correspondance établie ou NULL.                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlNode *g_yaml_node_find_one_by_path(const GYamlNode *node, const char *path, bool prepare)
{
    GYamlNode *result;                      /* Trouvaille unique à renvoyer*/
    GYamlNode **nodes;                      /* Liste de noeuds trouvés     */
    size_t count;                           /* Taille de cette liste       */
    size_t i;                               /* Boucle de parcours          */

    g_yaml_node_find_by_path(node, path, prepare, &nodes, &count);

    if (count == 1)
    {
        result = nodes[0];
        g_object_ref(G_OBJECT(result));
    }
    else
        result = NULL;

    for (i = 0; i < count; i++)
        g_object_unref(G_OBJECT(nodes[i]));

    if (nodes != NULL)
        free(nodes);

    return result;

}
