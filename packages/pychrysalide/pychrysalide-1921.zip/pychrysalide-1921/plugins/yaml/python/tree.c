
/* Chrysalide - Outil d'analyse de fichiers binaires
 * tree.c - équivalent Python du fichier "plugins/yaml/tree.c"
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
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */


#include "tree.h"


#include <pygobject.h>


#include <i18n.h>
#include <plugins/pychrysalide/helpers.h>


#include "line.h"
#include "../tree.h"



/* Crée un nouvel objet Python de type 'YamlTree'. */
static PyObject *py_yaml_tree_new(PyTypeObject *, PyObject *, PyObject *);

/* Recherche les noeuds correspondant à un chemin. */
static PyObject *py_yaml_tree_find_by_path(PyObject *, PyObject *);

/* Fournit le noeud constituant la racine d'arborescence Yaml. */
static PyObject *py_yaml_tree_get_root(PyObject *, void *);



/******************************************************************************
*                                                                             *
*  Paramètres  : type = type de l'objet à instancier.                         *
*                args = arguments fournis à l'appel.                          *
*                kwds = arguments de type key=val fournis.                    *
*                                                                             *
*  Description : Crée un nouvel objet Python de type 'YamlTree'.              *
*                                                                             *
*  Retour      : Instance Python mise en place.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_tree_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *result;                       /* Instance à retourner        */
    PyObject *tuple;                        /* Liste de lignes Yaml        */
    int ret;                                /* Bilan de lecture des args.  */
    size_t count;                           /* Nombre d'éléments présents  */
    GYamlLine **lines;                      /* Lignes au format Yaml       */
    GYamlTree *tree;                        /* Création GLib à transmettre */
    size_t i;                               /* Boucle de parcours #1       */
    PyObject *item;                         /* Elément de la liste fournie */
    size_t k;                               /* Boucle de parcours #2       */

#define YAML_TREE_DOC                                                       \
    "YamlTree offers a hierarchical access to Yaml lines as a tree.\n"      \
    "\n"                                                                    \
    "Instances can be created using the following constructor:\n"           \
    "\n"                                                                    \
    "    YamlTree(lines)"                                                   \
    "\n"                                                                    \
    "Where lines are a tuple of Yaml lines used to built the tree."

    ret = PyArg_ParseTuple(args, "O!", &PyTuple_Type, &tuple);
    if (!ret) return NULL;

    count = PyTuple_Size(tuple);

    lines = (GYamlLine **)malloc(count * sizeof(GYamlLine *));

    tree = NULL;

    for (i = 0; i < count; i++)
    {
        item = PyTuple_GetItem(tuple, i);

        ret = convert_to_yaml_line(item, &lines[i]);

        if (ret == 0)
            g_object_ref(G_OBJECT(lines[i]));

        else
            goto arg_error;

    }

    tree = g_yaml_tree_new(lines, count);

 arg_error:

    for (k = 0; k < i; k++)
        g_object_unref(G_OBJECT(lines[i]));

    free(lines);

    /* S'il y a eu une erreur... */
    if (i < count) return NULL;

    if (tree == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
    {
        g_object_ref_sink(G_OBJECT(tree));
        result = pygobject_new(G_OBJECT(tree));
        g_object_unref(tree);
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = variable non utilisée ici.                            *
*                args = arguments fournis à l'appel.                          *
*                                                                             *
*  Description : Recherche les noeuds correspondant à un chemin.              *
*                                                                             *
*  Retour      : Liste de noeuds trouvés, éventuellement vide.                *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_tree_find_by_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Instance à retourner        */
    int prepare;                            /* Orientation des résultats   */
    const char *path;                       /* Chemin d'accès à traiter    */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlTree *tree;                        /* Version GLib du type        */
    GYamlNode **found;                      /* Créations GLib à transmettre*/
    size_t count;                           /* Quantité de trouvailles     */
    size_t i;                               /* Boucle de parcours          */

#define YAML_TREE_FIND_BY_PATH_METHOD PYTHON_METHOD_DEF                     \
(                                                                           \
    find_by_path, "path, /, prepare=False",                                 \
    METH_VARARGS, py_yaml_tree,                                             \
    "Find nodes in a Yaml tree using a path.\n"                             \
    "\n"                                                                    \
    "Paths are node keys separated by '/', such as '/my/path/to/node'."     \
    "\n"                                                                    \
    "In case where the path ends with a trailing '/', the operation can"    \
    " be used to prepare a further look by returning a node which can be"   \
    " searched by a new call to this function instead of returning all its" \
    " contained nodes."                                                     \
)

    prepare = 0;

    ret = PyArg_ParseTuple(args, "s|p", &path, &prepare);
    if (!ret) return NULL;

    tree = G_YAML_TREE(pygobject_get(self));

    g_yaml_tree_find_by_path(tree, path, prepare, &found, &count);

    result = PyTuple_New(count);

    for (i = 0; i < count; i++)
    {
#ifndef NDEBUG
        ret = PyTuple_SetItem(result, i, pygobject_new(G_OBJECT(found[i])));
        assert(ret == 0);
#else
        PyTuple_SetItem(result, i, pygobject_new(G_OBJECT(found[i])));
#endif

        g_object_unref(G_OBJECT(found[i]));

    }

    if (found != NULL)
        free(found);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = variable non utilisée ici.                            *
*                args = arguments fournis à l'appel.                          *
*                                                                             *
*  Description : Recherche l'unique noeud correspondant à un chemin.          *
*                                                                             *
*  Retour      : Noeud avec correspondance établie ou None.                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_tree_find_one_by_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Instance à retourner        */
    int prepare;                            /* Orientation des résultats   */
    const char *path;                       /* Chemin d'accès à traiter    */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlTree *tree;                        /* Version GLib du type        */
    GYamlNode *found;                       /* Création GLib à transmettre */

#define YAML_TREE_FIND_ONE_BY_PATH_METHOD PYTHON_METHOD_DEF                 \
(                                                                           \
    find_one_by_path, "path, /, prepare=False",                             \
    METH_VARARGS, py_yaml_tree,                                             \
    "Find a given node from a Yaml node using a path.\n"                    \
    "\n"                                                                    \
    "Paths are node keys separated by '/', such as '/my/path/to/node'."     \
    "\n"                                                                    \
    "Only one node has to match the path for the function success."         \
    "\n"                                                                    \
    "In case where the path ends with a trailing '/', the operation can"    \
    " be used to prepare a further look by returning a node which can be"   \
    " searched by a new call to this function instead of returning all its" \
    " contained nodes."                                                     \
)

    prepare = 0;

    ret = PyArg_ParseTuple(args, "s|p", &path, &prepare);
    if (!ret) return NULL;

    tree = G_YAML_TREE(pygobject_get(self));

    found = g_yaml_tree_find_one_by_path(tree, path, prepare);

    if (found == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }
    else
    {
        result = pygobject_new(G_OBJECT(found));
        g_object_unref(G_OBJECT(found));
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit le noeud constituant la racine d'arborescence Yaml.  *
*                                                                             *
*  Retour      : Noeud constituant la racine de l'arborescence.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_tree_get_root(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlTree *tree;                        /* Version GLib du type        */
    GYamlNode *root;                        /* Noeud racine d'arborescence */

#define YAML_TREE_ROOT_ATTRIB PYTHON_GET_DEF_FULL           \
(                                                           \
    root, py_yaml_tree,                                     \
    "Yaml node which is the root of the whole tree nodes."  \
)

    tree = G_YAML_TREE(pygobject_get(self));

    root = g_yaml_tree_get_root(tree);

    result = pygobject_new(G_OBJECT(root));
    g_object_unref(G_OBJECT(root));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : -                                                            *
*                                                                             *
*  Description : Fournit un accès à une définition de type à diffuser.        *
*                                                                             *
*  Retour      : Définition d'objet pour Python.                              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

PyTypeObject *get_python_yaml_tree_type(void)
{
    static PyMethodDef py_yaml_tree_methods[] = {
        YAML_TREE_FIND_BY_PATH_METHOD,
        YAML_TREE_FIND_ONE_BY_PATH_METHOD,
        { NULL }
    };

    static PyGetSetDef py_yaml_tree_getseters[] = {
        YAML_TREE_ROOT_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_yaml_tree_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.plugins.yaml.YamlTree",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT,

        .tp_doc         = YAML_TREE_DOC,

        .tp_methods     = py_yaml_tree_methods,
        .tp_getset      = py_yaml_tree_getseters,
        .tp_new         = py_yaml_tree_new

    };

    return &py_yaml_tree_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.plugins.....YamlTree.  *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool register_python_yaml_tree(PyObject *module)
{
    PyTypeObject *type;                     /* Type Python 'YamlTree'      */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_yaml_tree_type();

    dict = PyModule_GetDict(module);

    if (!register_class_for_pygobject(dict, G_TYPE_YAML_TREE, type, &PyGObject_Type))
        return false;

    return true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : arg = argument quelconque à tenter de convertir.             *
*                dst = destination des valeurs récupérées en cas de succès.   *
*                                                                             *
*  Description : Tente de convertir en arborescence de lignes au format Yaml. *
*                                                                             *
*  Retour      : Bilan de l'opération, voire indications supplémentaires.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int convert_to_yaml_tree(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_yaml_tree_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to Yaml tree");
            break;

        case 1:
            *((GYamlTree **)dst) = G_YAML_TREE(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
