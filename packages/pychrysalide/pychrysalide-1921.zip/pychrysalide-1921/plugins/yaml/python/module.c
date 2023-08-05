
/* Chrysalide - Outil d'analyse de fichiers binaires
 * module.c - intégration du répertoire yaml en tant que module
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


#include "module.h"


#include <assert.h>
#include <Python.h>


#include <plugins/pychrysalide/access.h>
#include <plugins/pychrysalide/helpers.h>


#include "collection.h"
#include "line.h"
#include "node.h"
#include "pair.h"
#include "reader.h"
#include "scalar.h"
#include "tree.h"



/******************************************************************************
*                                                                             *
*  Paramètres  : -                                                            *
*                                                                             *
*  Description : Ajoute le module 'plugins.yaml' au module Python.            *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool add_yaml_module_to_python_module(void)
{
    bool result;                            /* Bilan à retourner           */
    PyObject *super;                        /* Module à compléter          */
    PyObject *module;                       /* Sous-module mis en place    */

#define PYCHRYSALIDE_PLUGINS_YAML_DOC                           \
    "yaml is a module providing access to Yaml content."

    static PyModuleDef py_chrysalide_yaml_module = {

        .m_base = PyModuleDef_HEAD_INIT,

        .m_name = "pychrysalide.plugins.yaml",
        .m_doc = PYCHRYSALIDE_PLUGINS_YAML_DOC,

        .m_size = -1,

    };

    result = false;

    super = get_access_to_python_module("pychrysalide.plugins");

    module = build_python_module(super, &py_chrysalide_yaml_module);

    result = (module != NULL);

    assert(result);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : -                                                            *
*                                                                             *
*  Description : Intègre les objets du module 'plugins.yaml'.                 *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool populate_yaml_module(void)
{
    bool result;                            /* Bilan à retourner           */
    PyObject *module;                       /* Module à recompléter        */

    result = true;

    module = get_access_to_python_module("pychrysalide.plugins.yaml");

    if (result) result = register_python_yaml_node(module);
    if (result) result = register_python_yaml_collection(module);
    if (result) result = register_python_yaml_line(module);
    if (result) result = register_python_yaml_pair(module);
    if (result) result = register_python_yaml_reader(module);
    if (result) result = register_python_yaml_scalar(module);
    if (result) result = register_python_yaml_tree(module);

    assert(result);

    return result;

}
