
/* Chrysalide - Outil d'analyse de fichiers binaires
 * scalar.c - équivalent Python du fichier "plugins/yaml/scalar.c"
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


#include "scalar.h"


#include <pygobject.h>


#include <plugins/pychrysalide/helpers.h>


#include "collection.h"
#include "line.h"
#include "node.h"
#include "../scalar.h"



/* Crée un nouvel objet Python de type 'YamlScalar'. */
static PyObject *py_yaml_scalar_new(PyTypeObject *, PyObject *, PyObject *);

/* Attache une collection de noeuds Yaml à un noeud. */
static int py_yaml_scalar_set_collection(PyObject *, PyObject *, void *);

/* Fournit une éventuelle collection rattachée à un noeud. */
static PyObject *py_yaml_scalar_get_collection(PyObject *, void *);



/******************************************************************************
*                                                                             *
*  Paramètres  : type = type de l'objet à instancier.                         *
*                args = arguments fournis à l'appel.                          *
*                kwds = arguments de type key=val fournis.                    *
*                                                                             *
*  Description : Crée un nouvel objet Python de type 'YamlScalar'.            *
*                                                                             *
*  Retour      : Instance Python mise en place.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_yaml_scalar_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *result;                       /* Instance à retourner        */
    GYamlLine *key;                         /* Ligne principale du noeud   */
    int ret;                                /* Bilan de lecture des args.  */
    GYamlScalar *node;                      /* Création GLib à transmettre */

#define YAML_SCALAR_DOC                                                 \
    "YamlScalar handles a scalar node in a Yaml tree.\n"                \
    "\n"                                                                \
    "Instances can be created using the following constructor:\n"       \
    "\n"                                                                \
    "    YamlScalar(key)\n"                                             \
    "\n"                                                                \
    "Where key is the main Yaml line for the scalar."

    ret = PyArg_ParseTuple(args, "O&", &convert_to_yaml_line, &key);
    if (!ret) return NULL;

    node = g_yaml_scalar_new(key);

    g_object_ref_sink(G_OBJECT(node));
    result = pygobject_new(G_OBJECT(node));
    g_object_unref(node);

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

static int py_yaml_scalar_set_collection(PyObject *self, PyObject *value, void *closure)
{
    int result;                             /* Bilan à renvoyer            */
    GYamlScalar *node;                      /* Version GLib du noeud       */
    GYamlCollection *collec;                /* Version GLib de la valeur   */

    node = G_YAML_SCALAR(pygobject_get(self));

    if (value == Py_None)
    {
        g_yaml_scalar_set_collection(node, NULL);
        result = 0;
    }

    else
    {
        if (!convert_to_yaml_collection(value, &collec))
            result = -1;

        else
        {
            g_yaml_scalar_set_collection(node, collec);
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

static PyObject *py_yaml_scalar_get_collection(PyObject *self, void *closure)
{
    PyObject *result;                       /* Instance à retourner        */
    GYamlScalar *node;                      /* Version GLib du noeud       */
    GYamlCollection *collec;                /* Collection à transmettre    */

#define YAML_SCALAR_COLLECTION_ATTRIB PYTHON_GETSET_DEF_FULL                    \
(                                                                               \
    collection, py_yaml_scalar,                                                 \
    "Provide or define the collection of nodes attached to another Yaml node."  \
)

    node = G_YAML_SCALAR(pygobject_get(self));

    collec = g_yaml_scalar_get_collection(node);

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

PyTypeObject *get_python_yaml_scalar_type(void)
{
    static PyMethodDef py_yaml_scalar_methods[] = {
        { NULL }
    };

    static PyGetSetDef py_yaml_scalar_getseters[] = {
        YAML_SCALAR_COLLECTION_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_yaml_scalar_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.plugins.yaml.YamlScalar",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT,

        .tp_doc         = YAML_SCALAR_DOC,

        .tp_methods     = py_yaml_scalar_methods,
        .tp_getset      = py_yaml_scalar_getseters,
        .tp_new         = py_yaml_scalar_new

    };

    return &py_yaml_scalar_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.plugins.....YamlScalar.*
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool register_python_yaml_scalar(PyObject *module)
{
    PyTypeObject *type;                     /* Type Python 'YamlScalar'    */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_yaml_scalar_type();

    dict = PyModule_GetDict(module);

    if (!register_class_for_pygobject(dict, G_TYPE_YAML_SCALAR, type, get_python_yaml_node_type()))
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

int convert_to_yaml_scalar(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_yaml_scalar_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to Yaml scalar");
            break;

        case 1:
            *((GYamlScalar **)dst) = G_YAML_SCALAR(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
