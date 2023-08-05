
/* Chrysalide - Outil d'analyse de fichiers binaires
 * tree.c - ligne de contenu Yaml
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


#include "tree.h"


#include <assert.h>
#include <malloc.h>
#include <string.h>


#include <i18n.h>
#include <core/logs.h>


#include "pair.h"
#include "collection.h"



/* Arborescence de lignes au format Yaml (instance) */
struct _GYamlTree
{
    GObject parent;                         /* A laisser en premier        */

    GYamlNode *root;                        /* Racine des noeuds           */

};

/* Arborescence de lignes au format Yaml (classe) */
struct _GYamlTreeClass
{
    GObjectClass parent;                    /* A laisser en premier        */

};


/* Initialise la classe des arborescence de lignes Yaml. */
static void g_yaml_tree_class_init(GYamlTreeClass *);

/* Initialise une instance d'arborescence de lignes Yaml. */
static void g_yaml_tree_init(GYamlTree *);

/* Supprime toutes les références externes. */
static void g_yaml_tree_dispose(GYamlTree *);

/* Procède à la libération totale de la mémoire. */
static void g_yaml_tree_finalize(GYamlTree *);

/* Construit une collection de noeuds avec une arborescence. */
static bool g_yaml_tree_build_node(GYamlCollection *, GYamlLine **, size_t, size_t, size_t *);



/* Indique le type défini pour une arborescence de lignes au format Yaml. */
G_DEFINE_TYPE(GYamlTree, g_yaml_tree, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des arborescence de lignes Yaml.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_tree_class_init(GYamlTreeClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_yaml_tree_dispose;
    object->finalize = (GObjectFinalizeFunc)g_yaml_tree_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : tree = instance à initialiser.                               *
*                                                                             *
*  Description : Initialise une instance d'arborescence de lignes Yaml.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_tree_init(GYamlTree *tree)
{
    tree->root = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : tree = instance d'objet GLib à traiter.                      *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_tree_dispose(GYamlTree *tree)
{
    g_clear_object(&tree->root);

    G_OBJECT_CLASS(g_yaml_tree_parent_class)->dispose(G_OBJECT(tree));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : tree = instance d'objet GLib à traiter.                      *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_tree_finalize(GYamlTree *tree)
{
    G_OBJECT_CLASS(g_yaml_tree_parent_class)->finalize(G_OBJECT(tree));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : lines  = ensemble de lignes à constituer en arborescence.    *
*                count  = taille de cet ensemble de lignes.                   *
*                                                                             *
*  Description : Construit une arborescence à partir de lignes Yaml.          *
*                                                                             *
*  Retour      : Instance mise en place ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlTree *g_yaml_tree_new(GYamlLine **lines, size_t count)
{
    GYamlTree *result;                      /* Structure à retourner       */
    GYamlCollection *collec;                /* Collection de noeuds        */
    size_t indent;                          /* Indentation initiale        */
    size_t processed;                       /* Quantité de noeuds traités  */
    bool status;                            /* Bilan de construction       */

    result = g_object_new(G_TYPE_YAML_TREE, NULL);

    if (count > 0)
    {
        collec = g_yaml_collection_new(g_yaml_line_is_list_item(lines[0]));

        result->root = G_YAML_NODE(collec);

        indent = g_yaml_line_count_indent(lines[0]);
        processed = 0;

        status = g_yaml_tree_build_node(collec, lines, count, indent, &processed);

        if (status)
            assert(processed == count);

        else
        {
            g_object_unref(G_OBJECT(result));
            result = NULL;
        }

    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : lines    = ensemble de lignes à constituer en arborescence.  *
*                count    = taille de cet ensemble de lignes.                 *
*                expected = niveau d'identation attendu.                      *
*                cur      = position courante dans les lignes. [OUT]          *
*                                                                             *
*  Description : Construit une collection de noeuds avec une arborescence.    *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static bool g_yaml_tree_build_node(GYamlCollection *collec, GYamlLine **lines, size_t count, size_t expected, size_t *cur)
{
    bool result;                            /* Bilan à retourner           */
    bool first;                             /* Marque d'un premier élément */
    GYamlNode *last;                        /* Mémorisation du dernier     */
    GYamlLine *line;                        /* Ligne de parcours courante  */
    size_t indent;                          /* Indentation de ligne        */
    bool is_item;                           /* Elément d'une liste ?       */
    GYamlCollection *sub;                   /* Nouvelle sous-collection    */

    result = true;

    first = true;
    last = NULL;

    for (; *cur < count; )
    {
        line = lines[*cur];

        indent = g_yaml_line_count_indent(line);
        is_item = g_yaml_line_is_list_item(line);

        /**
         * Si la première ligne traitée commence par un élément de liste,
         * alors un appel parent a constitué une collection qui n'est pas une séquence.
         *
         * L'objectif est de créer une simple association de 'clefs: valeurs'.
         *
         * Si la collection n'est pas adaptée, alors le parcours n'est pas encore
         * arrivé à ce stade de construction.
         */
        if (first && is_item && !g_yaml_collection_is_sequence(collec))
        {
            indent += 2; /* 2 == strlen("- ") */
            is_item = false;
        }

        first = false;

        /* Fin de l'ensemble courant */
        if (indent < expected)
            goto done;

        /* Début d'un sous-ensemble */
        else if (indent > expected)
        {
            if (last == NULL)
            {
                result = false;
                goto done;
            }

            sub = g_yaml_collection_new(is_item);
            g_yaml_pair_set_collection(G_YAML_PAIR(last), sub);

            result = g_yaml_tree_build_node(sub, lines, count, indent, cur);
            if (!result) goto done;

        }

        /* Elément de même niveau */
        else
        {
            if (is_item)
            {
                /* Vérification de cohérence */
                if (!g_yaml_collection_is_sequence(collec))
                {
                    log_variadic_message(LMT_BAD_BINARY, _("A list item was expected at line %zu"),
                                         g_yaml_line_get_number(line));

                    result = false;
                    goto done;

                }

                sub = g_yaml_collection_new(false);
                g_yaml_collection_add_node(collec, G_YAML_NODE(sub));

                result = g_yaml_tree_build_node(sub, lines, count, expected + 2 /* 2 == strlen("- ") */, cur);
                if (!result) goto done;

            }

            else
            {
                /* Vérification de cohérence */
                if (g_yaml_collection_is_sequence(collec))
                {
                    log_variadic_message(LMT_BAD_BINARY, _("A mapping item was expected at line %zu"),
                                         g_yaml_line_get_number(line));


                    result = false;
                    goto done;

                }

                last = G_YAML_NODE(g_yaml_pair_new(line));

                if (last == NULL)
                {
                    result = false;
                    goto done;
                }

                g_yaml_collection_add_node(collec, last);

                (*cur)++;

            }

        }

    }

 done:

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : tree  = ligne au format Yaml à consulter.                    *
*                                                                             *
*  Description : Fournit le noeud constituant la racine d'arborescence Yaml.  *
*                                                                             *
*  Retour      : Noeud constituant la racine de l'arborescence.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlNode *g_yaml_tree_get_root(const GYamlTree *tree)
{
    GYamlNode *result;                      /* Liste à retourner           */

    result = tree->root;

    if (result != NULL)
        g_object_ref(G_OBJECT(result));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : tree    = ligne au format Yaml à consulter.                  *
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

void g_yaml_tree_find_by_path(const GYamlTree *tree, const char *path, bool prepare, GYamlNode ***nodes, size_t *count)
{
    g_yaml_node_find_by_path(tree->root, path, prepare, nodes, count);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : tree    = ligne au format Yaml à consulter.                  *
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

GYamlNode *g_yaml_tree_find_one_by_path(GYamlTree *tree, const char *path, bool prepare)
{
    GYamlNode *result;                      /* Trouvaille unique à renvoyer*/

    result = g_yaml_node_find_one_by_path(tree->root, path, prepare);

    return result;

}
