
/* Chrysalide - Outil d'analyse de fichiers binaires
 * pair.c - équivalent Python du fichier "plugins/yaml/pair.c"
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
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */


#include "pair.h"


#include <assert.h>
#include <pygobject.h>


#include <plugins/pychrysalide/helpers.h>


#include "collection.h"
#include "line.h"
#include "node.h"
#include "../pair.h"



/* Crée un nouvel objet Python de type 'YamlPair'. */
static PyObject *py_yaml_pair_new(PyTypeObject *, PyObject *, PyObject *);

/* Fournit la clef représentée dans une paire en Yaml. */
static PyObject *py_yaml_pair_get_key(PyObject *, void *);

/* Fournit l'éventuelle valeur d'une paire en Yaml. */
static PyObject *py_yaml_pair_get_value(PyObject *, void *);

/* Attache une collection de noeuds Yaml à un noeud. */
static int py_yaml_pair_set_collection(PyObject *, PyObject *, void *);

/* Fournit une éventuelle collection rattachée à un noeud. */
static PyObject *py_yaml_pair_get_collection(PyObject *, void *);



/******************************************************************************
*                                                                             *
*  Paramètres  : type = type de l'objet à instancier.                         *
*                args = arguments fournis à l'appel.                          *
*                kwds = arguments de type key=val fournis.                    *
*                                                                             *
*  Description : Crée un nouvel objet Python de type 'YamlPair'.              *
*                                                                             *
*  Retour      : Instance Python mise en place.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_pair_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *result;                       /* Instance à retourner        */
    GYamlLine *key;                         /* Ligne principale du noeud   */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlPair *node;                      /* Création GLib à transmettre */

#define YAML_PAIR_DOC                                                   \
    "YamlPair handles a key/value pair node in a Yaml tree.\n"          \
    "\n"                                                                \
    "Instances can be created using the following constructor:\n"       \
    "\n"                                                                \
    "    YamlPair(line)\n"                                              \
    "\n"                                                                \
    "Where key is the original Yaml line for the pair."

    ret = PyArg_ParseTuple(args, "O&", &convert_to_yaml_line, &key);
    if (!ret) return NULL;

    node = g_yaml_pair_new(key);

    g_object_ref_sink(G_OBJECT(node));
    result = pygobject_new(G_OBJECT(node));
    g_object_unref(node);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit la clef représentée dans une paire en Yaml.          *
*                                                                             *
*  Retour      : Clef sous forme de chaîne de caractères.                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_pair_get_key(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlPair *node;                        /* Version GLib du noeud       */
    const char *key;                        /* Chaîne à transmettre        */

#define YAML_PAIR_KEY_ATTRIB PYTHON_GET_DEF_FULL    \
(                                                   \
    key, py_yaml_pair,                              \
    "Key linked to the Yaml key/value pair node."   \
)

    node = G_YAML_PAIR(pygobject_get(self));

    key = g_yaml_pair_get_key(node);
    assert(key != NULL);

    result = PyUnicode_FromString(key);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                closure = non utilisé ici.                                   *
*                                                                             *
*  Description : Fournit l'éventuelle valeur d'une paire en Yaml.             *
*                                                                             *
*  Retour      : Valeur sous forme de chaîne de caractères ou None.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_pair_get_value(PyObject *self, void *closure)
{
    PyObject *result;                       /* Résultat à retourner        */
    GYamlPair *node;                        /* Version GLib du type        */
    const char *value;                      /* Chaîne à transmettre        */

#define YAML_PAIR_VALUE_ATTRIB PYTHON_GET_DEF_FULL          \
(                                                           \
    value, py_yaml_pair,                                    \
    "Value linked to the Yaml key/value pair node or None." \
)

    node = G_YAML_PAIR(pygobject_get(self));

    value = g_yaml_pair_get_value(node);

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
*  Paramètres  : self    = contenu binaire à manipuler.                       *
*                value   = collection de noeuds Yaml.                         *
*                closure = adresse non utilisée ici.                          *
*                                                                             *
*  Description : Attache une collection de noeuds Yaml à un noeud.            *
*                                                                             *
*  Retour      : Jeu d'attributs liés au contenu courant.                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static int py_yaml_pair_set_collection(PyObject *self, PyObject *value, void *closure)
{
    int result;                             /* Bilan à renvoyer            */
    GYamlPair *node;                        /* Version GLib du noeud       */
    GYamlCollection *collec;                /* Version GLib de la valeur   */

    node = G_YAML_PAIR(pygobject_get(self));

    if (value == Py_None)
    {
        g_yaml_pair_set_collection(node, NULL);
        result = 0;
    }

    else
    {
        if (!convert_to_yaml_collection(value, &collec))
            result = -1;

        else
        {
            g_yaml_pair_set_collection(node, collec);
            result = 0;
        }

    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = contenu binaire à manipuler.                       *
*                closure = adresse non utilisée ici.                          *
*                                                                             *
*  Description : Fournit une éventuelle collection rattachée à un noeud.      *
*                                                                             *
*  Retour      : Collection de noeuds Yaml ou None.                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_pair_get_collection(PyObject *self, void *closure)
{
    PyObject *result;                       /* Instance à retourner        */
    GYamlPair *node;                        /* Version GLib du noeud       */
    GYamlCollection *collec;                /* Collection à transmettre    */

#define YAML_PAIR_COLLECTION_ATTRIB PYTHON_GETSET_DEF_FULL                      \
(                                                                               \
    collection, py_yaml_pair,                                                   \
    "Provide or define the collection of nodes attached to another Yaml node."  \
)

    node = G_YAML_PAIR(pygobject_get(self));

    collec = g_yaml_pair_get_collection(node);

    if (collec == NULL)
    {
        result = Py_None;
        Py_INCREF(result);
    }

    else
    {
        result = pygobject_new(G_OBJECT(collec));
        g_object_unref(collec);
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

PyTypeObject *get_python_yaml_pair_type(void)
{
    static PyMethodDef py_yaml_pair_methods[] = {
        { NULL }
    };

    static PyGetSetDef py_yaml_pair_getseters[] = {
        YAML_PAIR_KEY_ATTRIB,
        YAML_PAIR_VALUE_ATTRIB,
        YAML_PAIR_COLLECTION_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_yaml_pair_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.plugins.yaml.YamlPair",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT,

        .tp_doc         = YAML_PAIR_DOC,

        .tp_methods     = py_yaml_pair_methods,
        .tp_getset      = py_yaml_pair_getseters,
        .tp_new         = py_yaml_pair_new

    };

    return &py_yaml_pair_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.plugins.....YamlPair.  *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool register_python_yaml_pair(PyObject *module)
{
    PyTypeObject *type;                     /* Type Python 'YamlPair'      */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_yaml_pair_type();

    dict = PyModule_GetDict(module);

    if (!register_class_for_pygobject(dict, G_TYPE_YAML_PAIR, type, get_python_yaml_node_type()))
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

int convert_to_yaml_pair(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_yaml_pair_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to Yaml key/value pair");
            break;

        case 1:
            *((GYamlPair **)dst) = G_YAML_PAIR(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
