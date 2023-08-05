
/* Chrysalide - Outil d'analyse de fichiers binaires
 * reader.c - lecteur de contenu Yaml
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
 *  along with Chrysalide.  If not, see <http://www.gnu.org/licenses/>.
 */


#include "reader.h"


#include <malloc.h>
#include <string.h>
#include <gio/gio.h>


#include "line.h"



/* Lecteur de contenu Yaml (instance) */
struct _GYamlReader
{
    GObject parent;                         /* A laisser en premier        */

    GYamlLine **lines;                      /* Lignes Yaml chargées        */
    size_t count;                           /* Quantié de ces lignes       */

    GYamlTree *tree;                        /* Arborescence constituée     */

};

/* Lecteur de contenu Yaml (classe) */
struct _GYamlReaderClass
{
    GObjectClass parent;                    /* A laisser en premier        */

};


/* Initialise la classe des lecteurs de contenus Yaml. */
static void g_yaml_reader_class_init(GYamlReaderClass *);

/* Initialise une instance de lecteur de contenu Yaml. */
static void g_yaml_reader_init(GYamlReader *);

/* Supprime toutes les références externes. */
static void g_yaml_reader_dispose(GYamlReader *);

/* Procède à la libération totale de la mémoire. */
static void g_yaml_reader_finalize(GYamlReader *);



/* Indique le type défini pour un lecteur de contenu Yaml. */
G_DEFINE_TYPE(GYamlReader, g_yaml_reader, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des lecteurs de contenus Yaml.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_reader_class_init(GYamlReaderClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_yaml_reader_dispose;
    object->finalize = (GObjectFinalizeFunc)g_yaml_reader_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reader = instance à initialiser.                             *
*                                                                             *
*  Description : Initialise une instance de lecteur de contenu Yaml.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_reader_init(GYamlReader *reader)
{
    reader->lines = NULL;
    reader->count = 0;

    reader->tree = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reader = instance d'objet GLib à traiter.                    *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_reader_dispose(GYamlReader *reader)
{
    size_t i;                               /* Boucle de parcours          */

    for (i = 0; i < reader->count; i++)
        g_clear_object(&reader->lines[i]);

    g_clear_object(&reader->tree);

    G_OBJECT_CLASS(g_yaml_reader_parent_class)->dispose(G_OBJECT(reader));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reader = instance d'objet GLib à traiter.                    *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_reader_finalize(GYamlReader *reader)
{
    if (reader->lines != NULL)
        free(reader->lines);

    G_OBJECT_CLASS(g_yaml_reader_parent_class)->finalize(G_OBJECT(reader));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = données brutes au format Yaml à charger.           *
*                length  = quantité de ces données.                           *
*                                                                             *
*  Description : Crée un lecteur pour contenu au format Yaml.                 *
*                                                                             *
*  Retour      : Instance mise en place ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlReader *g_yaml_reader_new_from_content(const char *content, size_t length)
{
    GYamlReader *result;                    /* Structure à retourner       */
    char *dumped;                           /* Contenu manipulable         */
    char *saved;                            /* Sauvegarde de position      */
    char *iter;                             /* Boucle de parcours          */
    size_t number;                          /* Indice de ligne courante    */
    GYamlLine *line;                        /* Nouvelle ligne Yaml         */

    result = g_object_new(G_TYPE_YAML_READER, NULL);

    dumped = malloc(length * sizeof(char));

    memcpy(dumped, content, length);

    for (iter = dumped, saved = strchr(iter, '\n'), number = 0;
         *iter != '\0';
         iter = ++saved, saved = strchr(iter, '\n'), number++)
    {
        if (saved != NULL)
            *saved = '\0';

        if (*iter != '\0')
        {
            line = g_yaml_line_new(iter, number);

            if (line == NULL)
                goto format_error;

            result->lines = realloc(result->lines, ++result->count * sizeof(GYamlLine *));

            g_object_ref_sink(G_OBJECT(line));
            result->lines[result->count - 1] = line;

        }

        if (saved == NULL)
            break;

    }

    free(dumped);

    result->tree = g_yaml_tree_new(result->lines, result->count);

    return result;

 format_error:

    g_object_unref(G_OBJECT(result));

    return NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : path = chemin d'accès à un contenu à charger.                *
*                                                                             *
*  Description : Crée un lecteur pour contenu au format Yaml.                 *
*                                                                             *
*  Retour      : Instance mise en place ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlReader *g_yaml_reader_new_from_path(const char *path)
{
    GYamlReader *result;                    /* Structure à retourner       */
    char *scheme;                           /* Préfixe d'URI identifié     */
    GFile *file;                            /* Accès au contenu visé       */
    GFileInputStream *stream;               /* Flux ouvert en lecture      */
    GFileInfo *info;                        /* Informations du flux        */
    size_t length;                          /* Quantité d'octets présents  */
    char *content;                          /* Données obtenues par lecture*/

    result = NULL;

    /* Ouverture du fichier */

    scheme = g_uri_parse_scheme(path);

    if (scheme != NULL)
    {
        g_free(scheme);
        file = g_file_new_for_uri(path);
    }

    else
        file = g_file_new_for_path(path);

    stream = g_file_read(file, NULL, NULL);

    if (stream == NULL)
        goto no_content;

    /* Détermination de sa taille */

    info = g_file_input_stream_query_info(stream, G_FILE_ATTRIBUTE_STANDARD_SIZE, NULL, NULL);

    if (info == NULL)
        goto no_size_info;

    length = g_file_info_get_size(info);

    /* Lecture des données */

    content = malloc(length + 1 * sizeof(char));

    if (!g_input_stream_read_all(G_INPUT_STREAM(stream), content, length, (gsize []) { 0 }, NULL, NULL))
        goto read_error;

    content[length] = '\0';

    result = g_yaml_reader_new_from_content(content, length + 1);

 read_error:

    free(content);

 no_size_info:

    g_object_unref(G_OBJECT(stream));

 no_content:

    g_object_unref(G_OBJECT(file));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reader = lecteur de contenu Yaml à consulter.                *
*                count  = taille de la liste constituée. [OUT]                *
*                                                                             *
*  Description : Fournit la liste des lignes lues depuis un contenu Yaml.     *
*                                                                             *
*  Retour      : Liste de lignes correspondant au contenu Yaml lu.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlLine **g_yaml_reader_get_lines(const GYamlReader *reader, size_t *count)
{
    GYamlLine **result;                     /* Liste à retourner           */
    size_t i;                               /* Boucle de parcours          */

    *count = reader->count;

    result = malloc(*count * sizeof(GYamlLine *));

    for (i = 0; i < *count; i++)
    {
        result[i] = reader->lines[i];
        g_object_ref(result[i]);
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : reader = lecteur de contenu Yaml à consulter.                *
*                                                                             *
*  Description : Fournit l'arborescence associée à la lecture de lignes Yaml. *
*                                                                             *
*  Retour      : Arborescence constituée par la lecture du contenu Yaml.      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlTree *g_yaml_reader_get_tree(const GYamlReader *reader)
{
    GYamlTree *result;                      /* Arborescence à retourner    */

    result = reader->tree;

    if (result != NULL)
        g_object_ref(G_OBJECT(result));

    return result;

}
