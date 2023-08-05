
/* Chrysalide - Outil d'analyse de fichiers binaires
 * pair.c - noeud Yaml de paire clef/valeur
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


#include "pair.h"


#include <malloc.h>
#include <string.h>


#include "node-int.h"



/* Noeud d'une arborescence au format Yaml (instance) */
struct _GYamlPair
{
    GYamlNode parent;                       /* A laisser en premier        */

    char *key;                              /* Clef présente dans le noeud */
    char *value;                            /* Valeur associée             */

    GYamlCollection *collection;            /* Collection de noeuds        */

};

/* Noeud d'une arborescence au format Yaml (classe) */
struct _GYamlPairClass
{
    GYamlNodeClass parent;                  /* A laisser en premier        */

};


/* Initialise la classe des noeuds d'arborescence Yaml. */
static void g_yaml_pair_class_init(GYamlPairClass *);

/* Initialise une instance de noeud d'arborescence Yaml. */
static void g_yaml_pair_init(GYamlPair *);

/* Supprime toutes les références externes. */
static void g_yaml_pair_dispose(GYamlPair *);

/* Procède à la libération totale de la mémoire. */
static void g_yaml_pair_finalize(GYamlPair *);

/* Recherche les noeuds correspondant à un chemin. */
static void g_yaml_pair_find_by_path(const GYamlPair *, const char *, bool, GYamlNode ***, size_t *);



/* Indique le type défini pour un noeud d'arborescence Yaml. */
G_DEFINE_TYPE(GYamlPair, g_yaml_pair, G_TYPE_YAML_NODE);


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

static void g_yaml_pair_class_init(GYamlPairClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GYamlNodeClass *node;                   /* Version parente de classe   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_yaml_pair_dispose;
    object->finalize = (GObjectFinalizeFunc)g_yaml_pair_finalize;

    node = G_YAML_NODE_CLASS(klass);

    node->find = (find_yaml_node_fc)g_yaml_pair_find_by_path;

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

static void g_yaml_pair_init(GYamlPair *node)
{
    node->key = NULL;
    node->value = NULL;

    node->collection = NULL;

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

static void g_yaml_pair_dispose(GYamlPair *node)
{
    g_clear_object(&node->collection);

    G_OBJECT_CLASS(g_yaml_pair_parent_class)->dispose(G_OBJECT(node));

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

static void g_yaml_pair_finalize(GYamlPair *node)
{
    if (node->key != NULL)
        free(node->key);

    if (node->value != NULL)
        free(node->value);

    G_OBJECT_CLASS(g_yaml_pair_parent_class)->finalize(G_OBJECT(node));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = ligne Yaml à l'origine du futur noeud.                *
*                                                                             *
*  Description : Construit un noeud d'arborescence Yaml.                      *
*                                                                             *
*  Retour      : Instance mise en place ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlPair *g_yaml_pair_new(GYamlLine *line)
{
    GYamlPair *result;                      /* Structure à retourner       */
    const char *key;                        /* Clef associée au noeud      */
    const char *value;                      /* Eventuelle valeur associée  */

    key = g_yaml_line_get_key(line);
    value = g_yaml_line_get_value(line);

    if (key == NULL)
        result = NULL;

    else
    {
        result = g_object_new(G_TYPE_YAML_PAIR, NULL);

        G_YAML_NODE(result)->line = line;
        g_object_ref(G_OBJECT(line));

        result->key = strdup(key);

        if (value == NULL)
            result->value = NULL;
        else
            result->value = strdup(value);

    }

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

static void g_yaml_pair_find_by_path(const GYamlPair *node, const char *path, bool prepare, GYamlNode ***nodes, size_t *count)
{
    char *next;                             /* Prochaine partie du chemin  */
    size_t cmplen;                          /* Etendue de la comparaison   */
    int ret;                                /* Bilan d'une comparaison     */

    if (path[0] == '\0')
        goto exit;

    /* Correspondance au niveau du noeud ? */

    if (path[0] == '/')
    {
        path++;

        if (path[0] == '\0')
            goto matched;

    }

    next = strchr(path, '/');

    if (next == NULL)
        ret = strcmp(path, node->key);

    else
    {
        cmplen = next - path;

        if (cmplen == 0)
            goto cont;

        ret = strncmp(path, node->key, cmplen);

    }

    if (ret != 0)
        goto done;

    else if (next != NULL)
    {
        path += cmplen;
        goto cont;
    }

 matched:

    *nodes = realloc(*nodes, ++(*count) * sizeof(GYamlNode **));

    g_object_ref(G_OBJECT(node));
    (*nodes)[*count - 1] = G_YAML_NODE(node);

    goto done;

 cont:

    if (node->collection != NULL)
        _g_yaml_node_find_by_path(G_YAML_NODE(node->collection), path, prepare, nodes, count);

 done:

 exit:

    ;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = noeud d'arborescence Yaml à consulter.                *
*                                                                             *
*  Description : Fournit la clef représentée dans une paire en Yaml.          *
*                                                                             *
*  Retour      : Clef sous forme de chaîne de caractères.                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

const char *g_yaml_pair_get_key(const GYamlPair *node)
{
    char *result;                           /* Valeur à retourner          */

    result = node->key;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = noeud d'arborescence Yaml à consulter.                *
*                                                                             *
*  Description : Fournit l'éventuelle valeur d'une paire en Yaml.             *
*                                                                             *
*  Retour      : Valeur sous forme de chaîne de caractères ou NULL.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

const char *g_yaml_pair_get_value(const GYamlPair *node)
{
    char *result;                           /* Valeur à retourner          */

    result = node->value;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node   = noeud d'arborescence Yaml à compléter.              *
*                collec = collection de noeuds Yaml.                          *
*                                                                             *
*  Description : Attache une collection de noeuds Yaml à un noeud.            *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_yaml_pair_set_collection(GYamlPair *node, GYamlCollection *collec)
{
    g_clear_object(&node->collection);

    g_object_ref_sink(G_OBJECT(collec));
    node->collection = collec;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = noeud d'arborescence Yaml à consulter.                *
*                                                                             *
*  Description : Fournit une éventuelle collection rattachée à un noeud.      *
*                                                                             *
*  Retour      : Collection de noeuds Yaml ou NULL.                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlCollection *g_yaml_pair_get_collection(const GYamlPair *node)
{
    GYamlCollection *result;                /* Collection à renvoyer       */

    result = node->collection;

    if (result != NULL)
        g_object_ref(G_OBJECT(result));

    return result;

}
