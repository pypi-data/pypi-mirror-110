
/* Chrysalide - Outil d'analyse de fichiers binaires
 * plugin.h - prototypes pour les interactions avec un greffon Python
 *
 * Copyright (C) 2018 Cyrille Bagard
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


#ifndef _PLUGINS_PYCHRYSALIDE_PLUGINS_PLUGIN_H
#define _PLUGINS_PYCHRYSALIDE_PLUGINS_PLUGIN_H


#include <Python.h>
#include <glib-object.h>
#include <stdbool.h>


#include <plugins/plugin.h>



/* --------------------- INTERFACE INTERNE POUR GREFFONS PYTHON --------------------- */


#define G_TYPE_PYTHON_PLUGIN                (g_python_plugin_get_type())
#define G_PYTHON_PLUGIN(obj)                (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_PYTHON_PLUGIN, GPythonPlugin))
#define G_IS_PYTHON_PLUGIN(obj)             (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_PYTHON_PLUGIN))
#define G_PYTHON_PLUGIN_CLASS(klass)        (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_PYTHON_PLUGIN, GPythonPluginClass))
#define G_IS_PYTHON_PLUGIN_CLASS(klass)     (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_PYTHON_PLUGIN))
#define G_PYTHON_PLUGIN_GET_CLASS(obj)      (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_PYTHON_PLUGIN, GPythonPluginClass))


/* Ligne de représentation de code binaire (instance) */
typedef struct _GPythonPlugin GPythonPlugin;

/* Ligne de représentation de code binaire (classe) */
typedef struct _GPythonPluginClass GPythonPluginClass;


/* Indique le type défini par la GLib pour le greffon Python. */
GType g_python_plugin_get_type(void);

/* Crée un greffon à partir de code Python. */
GPluginModule *g_python_plugin_new(const char *, const char *);



/* ------------------------- MODULE PYTHON POUR LES SCRIPTS ------------------------- */


/* Fournit un accès à une définition de type à diffuser. */
PyTypeObject *get_python_plugin_module_type(void);

/* Prend en charge l'objet 'pychrysalide.plugins.PluginModule'. */
bool ensure_python_plugin_module_is_registered(void);



#endif  /* _PLUGINS_PYCHRYSALIDE_PLUGINS_PLUGIN_H */
