
/* Chrysalide - Outil d'analyse de fichiers binaires
 * scalar.c - noeud Yaml de type "scalar"
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


#include "scalar.h"


#include <malloc.h>
#include <string.h>


#include "node-int.h"



/* Noeud d'une arborescence au format Yaml (instance) */
struct _GYamlScalar
{
    GYamlNode parent;                       /* A laisser en premier        */

    GYamlLine *key;                         /* Clef principale du noeud    */
    GYamlCollection *collection;            /* Collection de noeuds        */

};

/* Noeud d'une arborescence au format Yaml (classe) */
struct _GYamlScalarClass
{
    GYamlNodeClass parent;                  /* A laisser en premier        */

};


/* Initialise la classe des noeuds d'arborescence Yaml. */
static void g_yaml_scalar_class_init(GYamlScalarClass *);

/* Initialise une instance de noeud d'arborescence Yaml. */
static void g_yaml_scalar_init(GYamlScalar *);

/* Supprime toutes les références externes. */
static void g_yaml_scalar_dispose(GYamlScalar *);

/* Procède à la libération totale de la mémoire. */
static void g_yaml_scalar_finalize(GYamlScalar *);

/* Recherche les noeuds correspondant à un chemin. */
static void g_yaml_scalar_find_by_path(const GYamlScalar *, const char *, bool, GYamlNode ***, size_t *);



/* Indique le type défini pour un noeud d'arborescence Yaml. */
G_DEFINE_TYPE(GYamlScalar, g_yaml_scalar, G_TYPE_YAML_NODE);


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

static void g_yaml_scalar_class_init(GYamlScalarClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GYamlNodeClass *node;                   /* Version parente de classe   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_yaml_scalar_dispose;
    object->finalize = (GObjectFinalizeFunc)g_yaml_scalar_finalize;

    node = G_YAML_NODE_CLASS(klass);

    node->find = (find_yaml_node_fc)g_yaml_scalar_find_by_path;

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

static void g_yaml_scalar_init(GYamlScalar *node)
{
    node->key = NULL;
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

static void g_yaml_scalar_dispose(GYamlScalar *node)
{
    g_clear_object(&node->key);

    g_clear_object(&node->collection);

    G_OBJECT_CLASS(g_yaml_scalar_parent_class)->dispose(G_OBJECT(node));

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

static void g_yaml_scalar_finalize(GYamlScalar *node)
{
    G_OBJECT_CLASS(g_yaml_scalar_parent_class)->finalize(G_OBJECT(node));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : key = line Yaml représentant la clef du futur noeud.         *
*                                                                             *
*  Description : Construit un noeud d'arborescence Yaml.                      *
*                                                                             *
*  Retour      : Instance mise en place ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlScalar *g_yaml_scalar_new(GYamlLine *key)
{
    GYamlScalar *result;                    /* Structure à retourner       */

    result = g_object_new(G_TYPE_YAML_SCALAR, NULL);

    /**
     * Le paragraphe "3.2.2.1. Keys Order" des spécifications précise
     * qu'une séquence n'est qu'un noeud sans correspondance clef/valeur.
     *
     * Cette situation doit donc être prise en compte.
     */

    if (key != NULL)
    {
        result->key = key;
        g_object_ref(G_OBJECT(key));
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : node = noeud d'arborescence Yaml à consulter.                *
*                                                                             *
*  Description : Fournit la ligne principale associée à un noeud.             *
*                                                                             *
*  Retour      : Ligne Yaml à l'origine du noeud.                             *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlLine *g_yaml_scalar_get_yaml_line(const GYamlScalar *node)
{
    GYamlLine *result;                      /* Ligne d'origine à renvoyer  */

    result = node->key;

    if (result != NULL)
        g_object_ref(G_OBJECT(result));

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

void g_yaml_scalar_set_collection(GYamlScalar *node, GYamlCollection *collec)
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

GYamlCollection *g_yaml_scalar_get_collection(const GYamlScalar *node)
{
    GYamlCollection *result;                /* Collection à renvoyer       */

    result = node->collection;

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

static void g_yaml_scalar_find_by_path(const GYamlScalar *node, const char *path, bool prepare, GYamlNode ***nodes, size_t *count)
{
    GYamlLine *line;                        /* Ligne Yaml liée au noeud    */
    const char *key;                        /* Clef associée au noeud      */
    char *next;                             /* Prochaine partie du chemin  */
    size_t cmplen;                          /* Etendue de la comparaison   */
    int ret;                                /* Bilan d'une comparaison     */
    GYamlCollection *collec;                /* Collection de noeuds        */

    if (path[0] == '\0')
        goto exit;

    line = g_yaml_scalar_get_yaml_line(node);

    /* Correspondance au niveau du noeud ? */

    if (line != NULL)
    {
        if (path[0] == '/')
        {
            path++;

            if (path[0] == '\0')
                goto matched;

        }

        key = g_yaml_line_get_key(line);

        next = strchr(path, '/');

        if (next == NULL)
            ret = strcmp(path, key);

        else
        {
            cmplen = next - path;

            if (cmplen == 0)
                goto cont;

            ret = strncmp(path, key, cmplen);

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

    }

 cont:

    collec = g_yaml_scalar_get_collection(node);

    if (collec != NULL)
    {
        _g_yaml_node_find_by_path(G_YAML_NODE(collec), path, prepare, nodes, count);

        g_object_unref(G_OBJECT(collec));

    }

 done:

    if (line != NULL)
        g_object_unref(G_OBJECT(line));

 exit:

    ;

}
