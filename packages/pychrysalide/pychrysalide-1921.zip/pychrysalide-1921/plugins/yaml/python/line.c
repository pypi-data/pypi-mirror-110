
/* Chrysalide - Outil d'analyse de fichiers binaires
 * line.c - équivalent Python du fichier "plugins/yaml/line.c"
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


#include "line.h"


#include <pygobject.h>


#include <plugins/pychrysalide/helpers.h>


#include "../line.h"



/* Crée un nouvel objet Python de type 'YamlLine'. */
static PyObject *py_yaml_line_new(PyTypeObject *, PyObject *, PyObject *);

/* Fournit la taille de l'indentation d'une ligne Yaml. */
static PyObject *py_yaml_line_get_indent(PyObject *, void *);

/* Indique si la ligne représente un élément de liste. */
static PyObject *py_yaml_line_is_list_item(PyObject *, void *);

/* Fournit la charge utile associée à une ligne Yaml. */
static PyObject *py_yaml_line_get_payload(PyObject *, void *);

/* Fournit la clef associée à une ligne Yaml si elle existe. */
static PyObject *py_yaml_line_get_key(PyObject *, void *);

/* Fournit la valeur associée à une ligne Yaml si elle existe. */
static PyObject *py_yaml_line_get_value(PyObject *, void *);



/******************************************************************************
*                                                                             *
*  Paramètres  : type = type de l'objet à instancier.                         *
*                args = arguments fournis à l'appel.                          *
*                kwds = arguments de type key=val fournis.                    *
*                                                                             *
*  Description : Crée un nouvel objet Python de type 'YamlLine'.              *
*                                                                             *
*  Retour      : Instance Python mise en place.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_line_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *result;                       /* Instance à retourner        */
    const char *raw;                        /* Données Yaml brutes         */
    Py_ssize_t index;                       /* Indice de ligne associée    */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlLine *line;                        /* Création GLib à transmettre */

#define YAML_LINE_DOC                                                   \
    "YamlLine handles a line of Yaml data.\n"                           \
    "\n"                                                                \
    "The data may be a couple of key/value, a comment, aso.\n"          \
    "\n"                                                                \
    "Instances can be created using the following constructor:\n"       \
    "\n"                                                                \
    "    YamlTree(raw, number)"                                         \
    "\n"                                                                \
    "Where raw is a string providing raw data and number the index"     \
    " of the line in the overall stream."

    ret = PyArg_ParseTuple(args, "sn", &raw, &index);
    if (!ret) return NULL;

    line = g_yaml_line_new(raw, index);

    if (line == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
    {
        g_object_ref_sink(G_OBJECT(line));
        result = pygobject_new(G_OBJECT(line));
        g_object_unref(line);
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit la taille de l'indentation d'une ligne Yaml.         *
*                                                                             *
*  Retour      : Taille de l'indentation rencontrée.                          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_line_get_indent(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlLine *line;                        /* Version GLib du type        */
    size_t indent;                          /* Taille de l'indentation     */

#define YAML_LINE_INDENT_ATTRIB PYTHON_GET_DEF_FULL     \
(                                                       \
    indent, py_yaml_line,                               \
    "Quantity of characters used for the indentation."  \
)

    line = G_YAML_LINE(pygobject_get(self));

    indent = g_yaml_line_count_indent(line);

    result = PyLong_FromSize_t(indent);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Indique si la ligne représente un élément de liste.          *
*                                                                             *
*  Retour      : Statut de l'état lié à une liste d'éléments.                 *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_line_is_list_item(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlLine *line;                        /* Version GLib du type        */
    bool status;                            /* Statut de la ligne          */

#define YAML_LINE_IS_LIST_ITEM_ATTRIB PYTHON_IS_DEF_FULL    \
(                                                           \
    list_item, py_yaml_line,                                \
    "Tell if the line starts a new list item."              \
)

    line = G_YAML_LINE(pygobject_get(self));

    status = g_yaml_line_is_list_item(line);

    result = status ? Py_True : Py_False;
    Py_INCREF(result);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit la charge utile associée à une ligne Yaml.           *
*                                                                             *
*  Retour      : Contenu sous forme de chaîne de caractères.                  *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_line_get_payload(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlLine *line;                        /* Version GLib du type        */
    const char *payload;                    /* Chaîne à transmettre        */

#define YAML_LINE_PAYLOAD_ATTRIB PYTHON_GET_DEF_FULL    \
(                                                       \
    payload, py_yaml_line,                              \
    "Payload of the Yaml line."                         \
)

    line = G_YAML_LINE(pygobject_get(self));

    payload = g_yaml_line_get_payload(line);

    result = PyUnicode_FromString(payload);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit la clef associée à une ligne Yaml si elle existe.    *
*                                                                             *
*  Retour      : Clef sous forme de chaîne de caractères ou None.             *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_line_get_key(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlLine *line;                        /* Version GLib du type        */
    const char *key;                        /* Chaîne à transmettre        */

#define YAML_LINE_KEY_ATTRIB PYTHON_GET_DEF_FULL    \
(                                                   \
    key, py_yaml_line,                              \
    "Key linked to the Yaml line or None."          \
)

    line = G_YAML_LINE(pygobject_get(self));

    key = g_yaml_line_get_key(line);

    if (key == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
        result = PyUnicode_FromString(key);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit la valeur associée à une ligne Yaml si elle existe.  *
*                                                                             *
*  Retour      : Valeur sous forme de chaîne de caractères ou None.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_line_get_value(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlLine *line;                        /* Version GLib du type        */
    const char *value;                      /* Chaîne à transmettre        */

#define YAML_LINE_VALUE_ATTRIB PYTHON_GET_DEF_FULL  \
(                                                   \
    value, py_yaml_line,                            \
    "Value linked to the Yaml line or None."        \
)

    line = G_YAML_LINE(pygobject_get(self));

    value = g_yaml_line_get_value(line);

    if (value == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
        result = PyUnicode_FromString(value);

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

PyTypeObject *get_python_yaml_line_type(void)
{
    static PyMethodDef py_yaml_line_methods[] = {
        { NULL }
    };

    static PyGetSetDef py_yaml_line_getseters[] = {
        YAML_LINE_INDENT_ATTRIB,
        YAML_LINE_IS_LIST_ITEM_ATTRIB,
        YAML_LINE_PAYLOAD_ATTRIB,
        YAML_LINE_KEY_ATTRIB,
        YAML_LINE_VALUE_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_yaml_line_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.plugins.yaml.YamlLine",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT,

        .tp_doc         = YAML_LINE_DOC,

        .tp_methods     = py_yaml_line_methods,
        .tp_getset      = py_yaml_line_getseters,
        .tp_new         = py_yaml_line_new

    };

    return &py_yaml_line_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.plugins.....YamlLine.  *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool register_python_yaml_line(PyObject *module)
{
    PyTypeObject *type;                     /* Type Python 'YamlLine'      */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_yaml_line_type();

    dict = PyModule_GetDict(module);

    if (!register_class_for_pygobject(dict, G_TYPE_YAML_LINE, type, &PyGObject_Type))
        return false;

    return true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : arg = argument quelconque à tenter de convertir.             *
*                dst = destination des valeurs récupérées en cas de succès.   *
*                                                                             *
*  Description : Tente de convertir en ligne de données au format Yaml.       *
*                                                                             *
*  Retour      : Bilan de l'opération, voire indications supplémentaires.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int convert_to_yaml_line(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_yaml_line_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to Yaml line");
            break;

        case 1:
            *((GYamlLine **)dst) = G_YAML_LINE(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
