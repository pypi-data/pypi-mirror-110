
/* Chrysalide - Outil d'analyse de fichiers binaires
 * reader.h - prototypes pour le lecteur de contenu Yaml
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


#ifndef PLUGINS_YAML_READER_H
#define PLUGINS_YAML_READER_H


#include <glib-object.h>
#include <stdbool.h>


#include "line.h"
#include "tree.h"



#define G_TYPE_YAML_READER            g_yaml_reader_get_type()
#define G_YAML_READER(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_YAML_READER, GYamlReader))
#define G_IS_YAML_READER(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_YAML_READER))
#define G_YAML_READER_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_YAML_READER, GYamlReaderClass))
#define G_IS_YAML_READER_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_YAML_READER))
#define G_YAML_READER_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_YAML_READER, GYamlReaderClass))


/* Lecteur de contenu Yaml (instance) */
typedef struct _GYamlReader GYamlReader;

/* Lecteur de contenu Yaml (classe) */
typedef struct _GYamlReaderClass GYamlReaderClass;


/* Indique le type défini pour un lecteur de contenu Yaml. */
GType g_yaml_reader_get_type(void);

/* Crée un lecteur pour contenu au format Yaml. */
GYamlReader *g_yaml_reader_new_from_content(const char *, size_t);

/* Crée un lecteur pour contenu au format Yaml. */
GYamlReader *g_yaml_reader_new_from_path(const char *);

/* Fournit la liste des lignes lues depuis un contenu Yaml. */
GYamlLine **g_yaml_reader_get_lines(const GYamlReader *, size_t *);

/* Fournit l'arborescence associée à la lecture de lignes Yaml. */
GYamlTree *g_yaml_reader_get_tree(const GYamlReader *);



#endif  /* PLUGINS_YAML_READER_H */
