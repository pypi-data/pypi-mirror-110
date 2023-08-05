
/* Chrysalide - Outil d'analyse de fichiers binaires
 * reader.c - équivalent Python du fichier "plugins/yaml/reader.c"
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
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */


#include "reader.h"


#include <pygobject.h>


#include <plugins/pychrysalide/helpers.h>


#include "../reader.h"



#define YAML_READER_DOC                                                                         \
    "YamlReader is the class which aims to provide a reader interface to Yaml content.\n"       \
    "\n"                                                                                        \
    "When no input error, the Yaml content can be retrieved line by line or thanks to a tree."



/* Crée un lecteur pour contenu au format Yaml. */
static PyObject *py_yaml_reader_new_from_content(PyObject *, PyObject *);

/* Crée un lecteur pour contenu au format Yaml. */
static PyObject *py_yaml_reader_new_from_path(PyObject *, PyObject *);

/* Fournit la liste des lignes lues depuis un contenu Yaml. */
static PyObject *py_yaml_reader_get_lines(PyObject *, void *);

/* Fournit l'arborescence associée à la lecture de lignes Yaml. */
static PyObject *py_yaml_reader_get_tree(PyObject *, void *);



/******************************************************************************
*                                                                             *
*  Paramètres  : self = variable non utilisée ici.                            *
*                args = arguments fournis à l'appel.                          *
*                                                                             *
*  Description : Crée un lecteur pour contenu au format Yaml.                 *
*                                                                             *
*  Retour      : Instance mise en place ou None en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_reader_new_from_content(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Instance à retourner        */
    const char *content;                    /* Contenu brut au format Yaml */
    int length;                             /* Taille de ce contenu        */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlReader *reader;                    /* Création GLib à transmettre */

#define YAML_READER_NEW_FROM_CONTENT_METHOD PYTHON_METHOD_DEF   \
(                                                               \
    new_from_content, "content",                                \
    METH_STATIC | METH_VARARGS, py_yaml_reader,                 \
    "Load a Yaml content."                                      \
)

    /**
     * La taille doit être de type 'int' et non 'Py_ssize_t', sinon les 32 bits
     * de poids fort ne sont pas initialisés !
     */

    ret = PyArg_ParseTuple(args, "s#", &content, &length);
    if (!ret) return NULL;

    reader = g_yaml_reader_new_from_content(content, length);

    if (reader == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
    {
        g_object_ref_sink(G_OBJECT(reader));
        result = pygobject_new(G_OBJECT(reader));
        g_object_unref(reader);
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = variable non utilisée ici.                            *
*                args = arguments fournis à l'appel.                          *
*                                                                             *
*  Description : Crée un lecteur pour contenu au format Yaml.                 *
*                                                                             *
*  Retour      : Instance mise en place ou None en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_reader_new_from_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Instance à retourner        */
    const char *path;                       /* Chemin d'accès à un contenu */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlReader *reader;                    /* Création GLib à transmettre */

#define YAML_READER_NEW_FROM_PATH_METHOD PYTHON_METHOD_DEF  \
(                                                           \
    new_from_path, "path",                                  \
    METH_STATIC | METH_VARARGS, py_yaml_reader,             \
    "Load a Yaml content from a path.\n"                    \
    "\n"                                                    \
    "The path can be a filename or a resource URI."         \
)

    ret = PyArg_ParseTuple(args, "s", &path);
    if (!ret) return NULL;

    reader = g_yaml_reader_new_from_path(path);

    if (reader == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
    {
        g_object_ref_sink(G_OBJECT(reader));
        result = pygobject_new(G_OBJECT(reader));
        g_object_unref(reader);
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit la liste des lignes lues depuis un contenu Yaml.     *
*                                                                             *
*  Retour      : Liste de lignes correspondant au contenu Yaml lu.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_reader_get_lines(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlReader *reader;                    /* Version GLib du type        */
    size_t count;                           /* Quantité de lignes à traiter*/
    GYamlLine **lines;                      /* Liste de lignes lues        */
    size_t i;                               /* Boucle de parcours          */
#ifndef NDEBUG
    int ret;                                /* Bilan d'une insertion       */
#endif

#define YAML_READER_LINES_ATTRIB PYTHON_GET_DEF_FULL    \
(                                                       \
    lines, py_yaml_reader,                              \
    "List of Yaml lines processed by the reader."       \
)

    reader = G_YAML_READER(pygobject_get(self));

    lines = g_yaml_reader_get_lines(reader, &count);

    result = PyTuple_New(count);

    for (i = 0; i < count; i++)
    {
#ifndef NDEBUG
        ret = PyTuple_SetItem(result, i, pygobject_new(G_OBJECT(lines[i])));
        assert(ret == 0);
#else
        PyTuple_SetItem(result, i, pygobject_new(G_OBJECT(lines[i])));
#endif

        g_object_unref(G_OBJECT(lines[i]));

    }

    if (lines != NULL)
        free(lines);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit l'arborescence associée à la lecture de lignes Yaml. *
*                                                                             *
*  Retour      : Arborescence constituée par la lecture du contenu Yaml.      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_reader_get_tree(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlReader *reader;                    /* Version GLib du type        */
    GYamlTree *tree;                        /* Arborescence associée       */

#define YAML_READER_TREE_ATTRIB PYTHON_GET_DEF_FULL     \
(                                                       \
    tree, py_yaml_reader,                               \
    "Tree of all nodes built from the Yaml content."    \
)

    reader = G_YAML_READER(pygobject_get(self));

    tree = g_yaml_reader_get_tree(reader);

    if (tree == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }
    else
    {
        result = pygobject_new(G_OBJECT(tree));
        g_object_unref(G_OBJECT(tree));
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

PyTypeObject *get_python_yaml_reader_type(void)
{
    static PyMethodDef py_yaml_reader_methods[] = {
        YAML_READER_NEW_FROM_CONTENT_METHOD,
        YAML_READER_NEW_FROM_PATH_METHOD,
        { NULL }
    };

    static PyGetSetDef py_yaml_reader_getseters[] = {
        YAML_READER_LINES_ATTRIB,
        YAML_READER_TREE_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_yaml_reader_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.plugins.yaml.YamlReader",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT,

        .tp_doc         = YAML_READER_DOC,

        .tp_methods     = py_yaml_reader_methods,
        .tp_getset      = py_yaml_reader_getseters,
        .tp_new         = no_python_constructor_allowed

    };

    return &py_yaml_reader_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.plugins.....YamlReader.*
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool register_python_yaml_reader(PyObject *module)
{
    PyTypeObject *type;                     /* Type Python 'YamlReader'    */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_yaml_reader_type();

    dict = PyModule_GetDict(module);

    if (!register_class_for_pygobject(dict, G_TYPE_YAML_READER, type, &PyGObject_Type))
        return false;

    return true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : arg = argument quelconque à tenter de convertir.             *
*                dst = destination des valeurs récupérées en cas de succès.   *
*                                                                             *
*  Description : Tente de convertir en lecteur de données au format Yaml.     *
*                                                                             *
*  Retour      : Bilan de l'opération, voire indications supplémentaires.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int convert_to_yaml_reader(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_yaml_reader_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to Yaml reader");
            break;

        case 1:
            *((GYamlReader **)dst) = G_YAML_READER(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
