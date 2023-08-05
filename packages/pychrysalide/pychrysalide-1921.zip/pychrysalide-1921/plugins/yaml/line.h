
/* Chrysalide - Outil d'analyse de fichiers binaires
 * line.h - prototypes pour une ligne de contenu Yaml
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


#ifndef PLUGINS_YAML_LINE_H
#define PLUGINS_YAML_LINE_H


#include <glib-object.h>
#include <stdbool.h>



#define G_TYPE_YAML_LINE            g_yaml_line_get_type()
#define G_YAML_LINE(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_YAML_LINE, GYamlLine))
#define G_IS_YAML_LINE(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_YAML_LINE))
#define G_YAML_LINE_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_YAML_LINE, GYamlLineClass))
#define G_IS_YAML_LINE_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_YAML_LINE))
#define G_YAML_LINE_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_YAML_LINE, GYamlLineClass))


/* Ligne de données au format Yaml (instance) */
typedef struct _GYamlLine GYamlLine;

/* Ligne de données au format Yaml (classe) */
typedef struct _GYamlLineClass GYamlLineClass;


/* Indique le type défini pour une ligne de données au format Yaml. */
GType g_yaml_line_get_type(void);

/* Met en place un gestionnaire pour ligne au format Yaml. */
GYamlLine *g_yaml_line_new(const char *, size_t);

/* Fournit la taille de l'indentation d'une ligne Yaml. */
size_t g_yaml_line_count_indent(const GYamlLine *);

/* Indique si la ligne représente un élément de liste. */
bool g_yaml_line_is_list_item(const GYamlLine *);

/* Fournit la charge utile associée à une ligne Yaml. */
const char *g_yaml_line_get_payload(const GYamlLine *);

/* Fournit la clef associée à une ligne Yaml si elle existe. */
const char *g_yaml_line_get_key(const GYamlLine *);

/* Fournit la valeur associée à une ligne Yaml si elle existe. */
const char *g_yaml_line_get_value(const GYamlLine *);



#define g_yaml_line_get_number(l) 0



#endif  /* PLUGINS_YAML_LINE_H */
