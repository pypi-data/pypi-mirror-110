
/* Chrysalide - Outil d'analyse de fichiers binaires
 * line.c - ligne de contenu Yaml
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


#include "line.h"


#include <malloc.h>
#include <string.h>


#include <core/logs.h>



/* Ligne de données au format Yaml (instance) */
struct _GYamlLine
{
    GObject parent;                         /* A laisser en premier        */

    char *raw;                              /* Contenu brut de la ligne    */
    size_t number;                          /* Indice associé              */

    size_t indent;                          /* Niveau d'indentation        */
    bool is_list_item;                      /* Elément de liste ?          */

    const char *payload;                    /* Charge utile du contenu     */

    char *key;                              /* Clef de la ligne Yaml       */
    char *value;                            /* Valeyr de la ligne Yaml     */

};

/* Ligne de données au format Yaml (classe) */
struct _GYamlLineClass
{
    GObjectClass parent;                    /* A laisser en premier        */

};


/* Initialise la classe des lignes de contenu Yaml. */
static void g_yaml_line_class_init(GYamlLineClass *);

/* Initialise une instance de ligne de contenu Yaml. */
static void g_yaml_line_init(GYamlLine *);

/* Supprime toutes les références externes. */
static void g_yaml_line_dispose(GYamlLine *);

/* Procède à la libération totale de la mémoire. */
static void g_yaml_line_finalize(GYamlLine *);



/* Indique le type défini pour une ligne de données au format Yaml. */
G_DEFINE_TYPE(GYamlLine, g_yaml_line, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des lignes de contenu Yaml.             *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_line_class_init(GYamlLineClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_yaml_line_dispose;
    object->finalize = (GObjectFinalizeFunc)g_yaml_line_finalize;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = instance à initialiser.                               *
*                                                                             *
*  Description : Initialise une instance de ligne de contenu Yaml.            *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_line_init(GYamlLine *line)
{
    line->raw = NULL;
    line->number = -1;

    line->indent = 0;
    line->is_list_item = false;

    line->payload = NULL;
    line->key = NULL;
    line->value = NULL;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = instance d'objet GLib à traiter.                      *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_line_dispose(GYamlLine *line)
{
    G_OBJECT_CLASS(g_yaml_line_parent_class)->dispose(G_OBJECT(line));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = instance d'objet GLib à traiter.                      *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_yaml_line_finalize(GYamlLine *line)
{
    if (line->raw != NULL)
        free(line->raw);

    if (line->key != NULL)
        free(line->key);

    if (line->value != NULL)
        free(line->value);

    G_OBJECT_CLASS(g_yaml_line_parent_class)->finalize(G_OBJECT(line));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : raw    = contenu brut d'une ligne au format Yaml.            *
*                number = indice associé à la ligne.                          *
*                                                                             *
*  Description : Met en place un gestionnaire pour ligne au format Yaml.      *
*                                                                             *
*  Retour      : Instance mise en place ou NULL en cas d'échec.               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GYamlLine *g_yaml_line_new(const char *raw, size_t number)
{
    GYamlLine *result;                      /* Structure à retourner       */
    char *iter;                             /* Boucle de parcours          */
    bool string_content[2];                 /* Ouvertures de chaînes       */
    bool escape;                            /* Echappement de marquant     */

    result = g_object_new(G_TYPE_YAML_LINE, NULL);

    result->raw = strdup(raw);
    result->number = number;

    /* Indentation */

    for (iter = result->raw; *iter != '\0'; iter++)
    {
        if (*iter != ' ')
            break;

        result->indent++;

    }

    if (*iter == '-')
    {
        result->is_list_item = true;

        for (iter++; *iter != '\0'; iter++)
            if (*iter != ' ')
                break;

    }

    result->payload = iter;

    /* Eventuel couple clef/valeur */

    string_content[0] = false;
    string_content[1] = false;

    for (; *iter != '\0'; iter++)
    {
        if (*iter == '\'' && !string_content[1])
        {
            if (iter == result->payload)
                escape = false;

            else
                escape = *(iter - 1) == '\'';

            if (!escape)
                string_content[0] = !string_content[0];

        }

        else if (*iter == '"' && !string_content[0])
        {
            if (iter == result->payload)
                escape = false;

            else
                escape = *(iter - 1) == '\\';

            if (!escape)
                string_content[1] = !string_content[1];

        }

        else if (!string_content[0] && !string_content[1])
        {

            if (*iter == ':')
                break;


        }

    }

    if (*iter != '\0')
    {
        result->key = strndup(result->payload, iter - result->payload);

        for (iter++; *iter != '\0'; iter++)
            if (*iter != ' ')
                break;

        if (*iter != '\0')
            result->value = strdup(iter);

    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = ligne au format Yaml à consulter.                     *
*                                                                             *
*  Description : Fournit la taille de l'indentation d'une ligne Yaml.         *
*                                                                             *
*  Retour      : Taille de l'indentation rencontrée.                          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

size_t g_yaml_line_count_indent(const GYamlLine *line)
{
    size_t result;                          /* Quantité à retourner        */

    result = line->indent;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = ligne au format Yaml à consulter.                     *
*                                                                             *
*  Description : Indique si la ligne représente un élément de liste.          *
*                                                                             *
*  Retour      : Statut de l'état lié à une liste d'éléments.                 *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_yaml_line_is_list_item(const GYamlLine *line)
{
    bool result;                            /* Statut à retourner          */

    result = line->is_list_item;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = ligne au format Yaml à consulter.                     *
*                                                                             *
*  Description : Fournit la charge utile associée à une ligne Yaml.           *
*                                                                             *
*  Retour      : Contenu sous forme de chaîne de caractères.                  *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

const char *g_yaml_line_get_payload(const GYamlLine *line)
{
    const char *result;                     /* Valeur à retourner          */

    result = line->payload;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = ligne au format Yaml à consulter.                     *
*                                                                             *
*  Description : Fournit la clef associée à une ligne Yaml si elle existe.    *
*                                                                             *
*  Retour      : Clef sous forme de chaîne de caractères ou NULL.             *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

const char *g_yaml_line_get_key(const GYamlLine *line)
{
    char *result;                           /* Valeur à retourner          */

    result = line->key;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : line = ligne au format Yaml à consulter.                     *
*                                                                             *
*  Description : Fournit la valeur associée à une ligne Yaml si elle existe.  *
*                                                                             *
*  Retour      : Valeur sous forme de chaîne de caractères ou NULL.           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

const char *g_yaml_line_get_value(const GYamlLine *line)
{
    char *result;                           /* Valeur à retourner          */

    result = line->value;

    return result;

}
