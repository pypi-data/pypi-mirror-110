
/* Chrysalide - Outil d'analyse de fichiers binaires
 * node.c - équivalent Python du fichier "plugins/yaml/node.c"
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


#include "node.h"


#include <pygobject.h>


#include <plugins/pychrysalide/helpers.h>


#include "collection.h"
#include "line.h"
#include "../node.h"



#define YAML_NODE_DOC                                                                               \
    "YamlNode handles a node in a Yaml tree.\n"                                                     \
    "\n"                                                                                            \
    "There are three kinds of node contents defined in the Yaml specifications:\n"                  \
    "* scalar, implemented by the pychrysalide.plugins.yaml.YamlScalar object.\n"                   \
    "* sequence and mapping, implemented by the pychrysalide.plugins.yaml.YamlCollection object."



/* Recherche les noeuds correspondant à un chemin. */
static PyObject *py_yaml_node_find_by_path(PyObject *, PyObject *);

/* Recherche l'unique noeud correspondant à un chemin. */
static PyObject *py_yaml_node_find_one_by_path(PyObject *, PyObject *);

/* Fournit la ligne d'origine associée à un noeud. */
static PyObject *py_yaml_node_get_yaml_line(PyObject *, void *);



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

static PyObject *py_yaml_node_find_by_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Instance à retourner        */
    int prepare;                            /* Orientation des résultats   */
    const char *path;                       /* Chemin d'accès à traiter    */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlNode *node;                        /* Version GLib du noeud       */
    GYamlNode **found;                      /* Créations GLib à transmettre*/
    size_t count;                           /* Quantité de trouvailles     */
    size_t i;                               /* Boucle de parcours          */

#define YAML_NODE_FIND_BY_PATH_METHOD PYTHON_METHOD_DEF                     \
(                                                                           \
    find_by_path, "path, /, prepare=False",                                 \
    METH_VARARGS, py_yaml_node,                                             \
    "Find nodes from a Yaml node using a path.\n"                           \
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

    node = G_YAML_NODE(pygobject_get(self));

    g_yaml_node_find_by_path(node, path, prepare, &found, &count);

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

static PyObject *py_yaml_node_find_one_by_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Instance à retourner        */
    int prepare;                            /* Orientation des résultats   */
    const char *path;                       /* Chemin d'accès à traiter    */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlNode *node;                        /* Version GLib du noeud       */
    GYamlNode *found;                       /* Création GLib à transmettre */

#define YAML_NODE_FIND_ONE_BY_PATH_METHOD PYTHON_METHOD_DEF                 \
(                                                                           \
    find_one_by_path, "path, /, prepare=False",                             \
    METH_VARARGS, py_yaml_node,                                             \
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

    node = G_YAML_NODE(pygobject_get(self));

    found = g_yaml_node_find_one_by_path(node, path, prepare);

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
*  Description : Fournit la ligne principale associée à un noeud.             *
*                                                                             *
*  Retour      : Ligne Yaml à l'origine du noeud.                             *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_node_get_yaml_line(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlNode *node;                        /* Version GLib du noeud       */
    GYamlLine *line;                        /* Line Yaml associée          */

#define YAML_NODE_YAML_LINE_ATTRIB PYTHON_GET_DEF_FULL      \
(                                                           \
    yaml_line, py_yaml_node,                                \
    "Orginal Yaml line linked to the node."                 \
)

    node = G_YAML_NODE(pygobject_get(self));

    line = g_yaml_node_get_yaml_line(node);

    if (line == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }
    else
    {
        result = pygobject_new(G_OBJECT(line));
        g_object_unref(G_OBJECT(line));
    }

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

PyTypeObject *get_python_yaml_node_type(void)
{
    static PyMethodDef py_yaml_node_methods[] = {
        YAML_NODE_FIND_BY_PATH_METHOD,
        YAML_NODE_FIND_ONE_BY_PATH_METHOD,
        { NULL }
    };

    static PyGetSetDef py_yaml_node_getseters[] = {
        YAML_NODE_YAML_LINE_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_yaml_node_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.plugins.yaml.YamlNode",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_IS_ABSTRACT | Py_TPFLAGS_BASETYPE,

        .tp_doc         = YAML_NODE_DOC,

        .tp_methods     = py_yaml_node_methods,
        .tp_getset      = py_yaml_node_getseters,
        .tp_new         = no_python_constructor_allowed

    };

    return &py_yaml_node_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.plugins.....YamlNode.  *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool register_python_yaml_node(PyObject *module)
{
    PyTypeObject *type;                     /* Type Python 'YamlNode'      */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_yaml_node_type();

    dict = PyModule_GetDict(module);

    if (!register_class_for_pygobject(dict, G_TYPE_YAML_NODE, type, &PyGObject_Type))
        return false;

    return true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : arg = argument quelconque à tenter de convertir.             *
*                dst = destination des valeurs récupérées en cas de succès.   *
*                                                                             *
*  Description : Tente de convertir en noeud d'arborescence de format Yaml.   *
*                                                                             *
*  Retour      : Bilan de l'opération, voire indications supplémentaires.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int convert_to_yaml_node(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_yaml_node_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to Yaml node");
            break;

        case 1:
            *((GYamlNode **)dst) = G_YAML_NODE(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
