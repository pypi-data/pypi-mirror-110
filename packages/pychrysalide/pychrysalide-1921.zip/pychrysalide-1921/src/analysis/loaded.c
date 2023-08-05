
/* Chrysalide - Outil d'analyse de fichiers binaires
 * loaded.c - intégration des contenus chargés
 *
 * Copyright (C) 2017-2019 Cyrille Bagard
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


#include "loaded.h"


#include <assert.h>


#include "loaded-int.h"
#include "../core/global.h"
#include "../core/queue.h"
#include "../glibext/chrysamarshal.h"
#include "../glibext/gloadedpanel.h"
#include "../glibext/named-int.h"
#include "../plugins/pglist.h"



/* Analyse de contenu chargé (instance) */
typedef struct _GLoadedAnalysis GLoadedAnalysis;



/* ---------------------- GESTION SOUS FORME DE CONTENU CHARGE ---------------------- */


/* Procède à l'initialisation de l'interface de contenu chargé. */
static void g_loaded_content_default_init(GLoadedContentInterface *);

/* Acquitte la fin d'une tâche d'analyse différée et complète. */
static void on_loaded_content_analysis_completed(GLoadedAnalysis *, GLoadedContent *);



/* -------------------------- PHASE D'ANALYSE EN PARALLELE -------------------------- */


#define G_TYPE_LOADED_ANALYSIS            g_loaded_analysis_get_type()
#define G_LOADED_ANALYSIS(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_LOADED_ANALYSIS, GDelayedDisassembly))
#define G_IS_LOADED_ANALYSIS(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_LOADED_ANALYSIS))
#define G_LOADED_ANALYSIS_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_LOADED_ANALYSIS, GDelayedDisassemblyClass))
#define G_IS_LOADED_ANALYSIS_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_LOADED_ANALYSIS))
#define G_LOADED_ANALYSIS_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_LOADED_ANALYSIS, GDelayedDisassemblyClass))


/* Analyse de contenu chargé (instance) */
struct _GLoadedAnalysis
{
    GDelayedWork parent;                    /* A laisser en premier        */

    GLoadedContent *content;                /* Cible de l'analyse à mener  */
    bool connect;                           /* Lancement de connexions ?   */
    bool cache;                             /* Degré d'opération à mener   */

    bool success;                           /* Bilan de l'opération        */

};

/* Analyse de contenu chargé (classe) */
typedef struct _GLoadedAnalysisClass
{
    GDelayedWorkClass parent;               /* A laisser en premier        */

} GLoadedAnalysisClass;


/* Indique le type défini pour les tâches d'analyse différée. */
static GType g_loaded_analysis_get_type(void);

/* Initialise la classe des tâches d'analyse différées. */
static void g_loaded_analysis_class_init(GLoadedAnalysisClass *);

/* Initialise une tâche d'analyse de contenu différée. */
static void g_loaded_analysis_init(GLoadedAnalysis *);

/* Supprime toutes les références externes. */
static void g_loaded_analysis_dispose(GLoadedAnalysis *);

/* Procède à la libération totale de la mémoire. */
static void g_loaded_analysis_finalize(GLoadedAnalysis *);

/* Crée une tâche d'analyse de contenu différée. */
static GLoadedAnalysis *g_loaded_analysis_new(GLoadedContent *, bool, bool);

/* Assure l'analyse d'un contenu chargé en différé. */
static void g_loaded_analysis_process(GLoadedAnalysis *, GtkStatusStack *);



/* ---------------------------------------------------------------------------------- */
/*                        GESTION SOUS FORME DE CONTENU CHARGE                        */
/* ---------------------------------------------------------------------------------- */


/* Détermine le type d'une interface pour l'intégration de contenu chargé. */
G_DEFINE_INTERFACE(GLoadedContent, g_loaded_content, G_TYPE_OBJECT);


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de contenu chargé. *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_loaded_content_default_init(GLoadedContentInterface *iface)
{
    g_signal_new("analyzed",
                 G_TYPE_LOADED_CONTENT,
                 G_SIGNAL_RUN_LAST,
                 G_STRUCT_OFFSET(GLoadedContentIface, analyzed),
                 NULL, NULL,
                 g_cclosure_marshal_VOID__BOOLEAN,
                 G_TYPE_NONE, 1, G_TYPE_BOOLEAN);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de composant nommé.*
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_loaded_content_named_interface_init(GNamedWidgetIface *iface)
{
    iface->get_name = (get_named_widget_name_fc)g_loaded_content_describe;
    iface->get_widget = (get_named_widget_widget_fc)g_loaded_content_build_default_view;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à traiter.                          *
*                xdoc    = structure XML en cours d'édition.                  *
*                context = contexte à utiliser pour les recherches.           *
*                path    = chemin d'accès réservé au binaire.                 *
*                                                                             *
*  Description : Interprète un contenu chargé avec un appui XML.              *
*                                                                             *
*  Retour      : true si l'opération a bien tourné, false sinon.              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_loaded_content_restore(GLoadedContent *content, xmlDocPtr xdoc, xmlXPathContextPtr context, const char *path)
{
    bool result;                            /* Bilan à faire remonter      */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    if (iface->restore != NULL)
        result = iface->restore(content, xdoc, context, path);

    else
        result = true;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à traiter.                          *
*                xdoc    = structure XML en cours d'édition.                  *
*                context = contexte à utiliser pour les recherches.           *
*                path    = chemin d'accès réservé à l'élément.                *
*                                                                             *
*  Description : Ecrit une sauvegarde de l'élément dans un fichier XML.       *
*                                                                             *
*  Retour      : true si l'opération a bien tourné, false sinon.              *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_loaded_content_save(GLoadedContent *content, xmlDocPtr xdoc, xmlXPathContextPtr context, const char *path)
{
    bool result;                            /* Bilan à faire remonter      */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    if (iface->save != NULL)
        result = iface->save(content, xdoc, context, path);

    else
        result = true;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à manipuler.                        *
*                                                                             *
*  Description : Fournit le contenu représenté de l'élément chargé.           *
*                                                                             *
*  Retour      : Contenu représenté.                                          *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GBinContent *g_loaded_content_get_content(const GLoadedContent *content)
{
    GBinContent *result;                    /* Contenu interne à renvoyer  */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->get_content(content);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à manipuler.                        *
*                                                                             *
*  Description : Fournit le format associé à l'élément chargé.                *
*                                                                             *
*  Retour      : Format associé à l'élément chargé.                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

char *g_loaded_content_get_format_name(const GLoadedContent *content)
{
    char *result;                           /* Contenu interne à renvoyer  */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->get_format_name(content);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à manipuler.                        *
*                connect = organise le lancement des connexions aux serveurs. *
*                cache   = précise si la préparation d'un rendu est demandée. *
*                                                                             *
*  Description : Lance l'analyse propre à l'élément chargé.                   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_loaded_content_analyze(GLoadedContent *content, bool connect, bool cache)
{
    GLoadedAnalysis *analysis;              /* Analyse à mener             */
    GWorkQueue *queue;                      /* Gestionnaire de différés    */

    analysis = g_loaded_analysis_new(content, connect, cache);

    g_signal_connect(analysis, "work-completed",
                     G_CALLBACK(on_loaded_content_analysis_completed), content);

    queue = get_work_queue();

    g_work_queue_schedule_work(queue, G_DELAYED_WORK(analysis), DEFAULT_WORK_GROUP);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : analysis = tâche d'analyse menée à bien.                     *
*                content  = contenu chargé dont l'analyse est terminée.       *
*                                                                             *
*  Description : Acquitte la fin d'une tâche d'analyse différée et complète.  *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void on_loaded_content_analysis_completed(GLoadedAnalysis *analysis, GLoadedContent *content)
{
    g_signal_emit_by_name(content, "analyzed", analysis->success);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à manipuler.                        *
*                connect = organise le lancement des connexions aux serveurs. *
*                cache   = précise si la préparation d'un rendu est demandée. *
*                                                                             *
*  Description : Lance l'analyse de l'élément chargé et attend sa conclusion. *
*                                                                             *
*  Retour      : Conclusion obtenue suite à l'analyse.                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_loaded_content_analyze_and_wait(GLoadedContent *content, bool connect, bool cache)
{
    bool result;                            /* Bilan à retourner           */
    GLoadedAnalysis *analysis;              /* Analyse à mener             */
    GWorkQueue *queue;                      /* Gestionnaire de différés    */
    wgroup_id_t gid;                        /* Identifiant pour les tâches */

    analysis = g_loaded_analysis_new(content, connect, cache);
    g_object_ref(G_OBJECT(analysis));

    queue = get_work_queue();

    gid = g_work_queue_define_work_group(queue);

    g_work_queue_schedule_work(queue, G_DELAYED_WORK(analysis), gid);

    g_work_queue_wait_for_completion(queue, gid);

    g_work_queue_delete_work_group(queue, gid);

    result = analysis->success;
    g_object_unref(G_OBJECT(analysis));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à consulter.                        *
*                full    = précise s'il s'agit d'une version longue ou non.   *
*                                                                             *
*  Description : Fournit le désignation associée à l'élément chargé.          *
*                                                                             *
*  Retour      : Description courante.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

char *g_loaded_content_describe(const GLoadedContent *content, bool full)
{
    char *result;                           /* Description à retourner     */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->describe(content, full);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = élément chargé à consulter.                        *
*                version = précise si les versions doivent être recherchées.  *
*                count   = nombre de types d'obscurcissement trouvés. [OUT]   *
*                                                                             *
*  Description : Etablit une liste d'obscurcissements présents.               *
*                                                                             *
*  Retour      : Désignations humaines correspondantes à libérer après usage  *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

char **g_loaded_content_detect_obfuscators(const GLoadedContent *content, bool version, size_t *count)
{
    char **result;                          /* Liste à retourner           */

    result = NULL;
    *count = 0;

    detect_external_tools(PGA_DETECTION_OBFUSCATORS, content, version, &result, count);

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                             GESTION DYNAMIQUE DES VUES                             */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à consulter.                        *
*                                                                             *
*  Description : Détermine le nombre de vues disponibles pour un contenu.     *
*                                                                             *
*  Retour      : Quantité strictement positive.                               *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

unsigned int g_loaded_content_count_views(const GLoadedContent *content)
{
    unsigned int result;                    /* Quantité de vues à renvoyer */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->count_views(content);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à consulter.                        *
*                index   = indice de la vue ciblée.                           *
*                                                                             *
*  Description : Fournit le nom d'une vue donnée d'un contenu chargé.         *
*                                                                             *
*  Retour      : Désignation humainement lisible.                             *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

char *g_loaded_content_get_view_name(const GLoadedContent *content, unsigned int index)
{
    char *result;                           /* Désignation à retourner     */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    assert(index <= g_loaded_content_count_views(content));

    result = iface->get_view_name(content, index);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à consulter.                        *
*                                                                             *
*  Description : Met en place la vue initiale pour un contenu chargé.         *
*                                                                             *
*  Retour      : Composant graphique nouveau.                                 *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GtkWidget *g_loaded_content_build_default_view(GLoadedContent *content)
{
    GtkWidget *result;                      /* Support à retourner         */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->build_def_view(content);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à consulter.                        *
*                index   = indice de la vue ciblée.                           *
*                                                                             *
*  Description : Met en place la vue demandée pour un contenu chargé.         *
*                                                                             *
*  Retour      : Composant graphique nouveau.                                 *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GtkWidget *g_loaded_content_build_view(GLoadedContent *content, unsigned int index)
{
    GtkWidget *result;                      /* Support à retourner         */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    assert(index <= g_loaded_content_count_views(content));

    result = iface->build_view(content, index);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à consulter.                        *
*                index   = composant graphique en place.                      *
*                                                                             *
*  Description : Retrouve l'indice correspondant à la vue donnée d'un contenu.*
*                                                                             *
*  Retour      : Indice de la vue représentée, ou -1 en cas d'erreur.         *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

unsigned int g_loaded_content_get_view_index(GLoadedContent *content, GtkWidget *view)
{
    unsigned int result;                    /* Indice à retourner          */
    GLoadedContentIface *iface;             /* Interface utilisée          */

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->get_view_index(content, view);

    assert(result == -1 || result <= g_loaded_content_count_views(content));

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à consulter.                        *
*                index   = composant graphique à cibler.                      *
*                                                                             *
*  Description : Fournit toutes les options d'affichage pour un contenu.      *
*                                                                             *
*  Retour      : Gestionnaire de paramètres.                                  *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GDisplayOptions *g_loaded_content_get_display_options(const GLoadedContent *content, unsigned int index)
{
    GDisplayOptions *result;                /* Accès aux options à renvoyer*/
    GLoadedContentIface *iface;             /* Interface utilisée          */

    assert(index <= g_loaded_content_count_views(content));

    iface = G_LOADED_CONTENT_GET_IFACE(content);

    result = iface->get_options(content, index);

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                            PHASE D'ANALYSE EN PARALLELE                            */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour les tâches d'analyse différée. */
G_DEFINE_TYPE(GLoadedAnalysis, g_loaded_analysis, G_TYPE_DELAYED_WORK);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe des tâches d'analyse différées.         *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_loaded_analysis_class_init(GLoadedAnalysisClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GDelayedWorkClass *work;                /* Version en classe parente   */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_loaded_analysis_dispose;
    object->finalize = (GObjectFinalizeFunc)g_loaded_analysis_finalize;

    work = G_DELAYED_WORK_CLASS(klass);

    work->run = (run_task_fc)g_loaded_analysis_process;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : analysis = instance à initialiser.                           *
*                                                                             *
*  Description : Initialise une tâche d'analyse de contenu différée.          *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_loaded_analysis_init(GLoadedAnalysis *analysis)
{
    analysis->success = false;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : disass = instance d'objet GLib à traiter.                    *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_loaded_analysis_dispose(GLoadedAnalysis *analysis)
{
    g_clear_object(&analysis->content);

    G_OBJECT_CLASS(g_loaded_analysis_parent_class)->dispose(G_OBJECT(analysis));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : analysis = instance d'objet GLib à traiter.                  *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_loaded_analysis_finalize(GLoadedAnalysis *analysis)
{
    G_OBJECT_CLASS(g_loaded_analysis_parent_class)->finalize(G_OBJECT(analysis));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : content = contenu chargé à traiter.                          *
*                connect = organise le lancement des connexions aux serveurs. *
*                cache   = précise si la préparation d'un rendu est demandée. *
*                                                                             *
*  Description : Crée une tâche d'analyse de contenu différée.                *
*                                                                             *
*  Retour      : Tâche créée.                                                 *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static GLoadedAnalysis *g_loaded_analysis_new(GLoadedContent *content, bool connect, bool cache)
{
    GLoadedAnalysis *result;            /* Tâche à retourner           */

    result = g_object_new(G_TYPE_LOADED_ANALYSIS, NULL);

    result->content = content;
    g_object_ref(G_OBJECT(content));

    result->connect = connect;
    result->cache = cache;

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : analysis = analyse à mener.                                  *
*                status   = barre de statut à tenir informée.                 *
*                                                                             *
*  Description : Assure l'analyse d'un contenu chargé en différé.             *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_loaded_analysis_process(GLoadedAnalysis *analysis, GtkStatusStack *status)
{
    GLoadedContentIface *iface;             /* Interface utilisée          */
    GWorkQueue *queue;                      /* Gestionnaire de différés    */
    wgroup_id_t gid;                        /* Identifiant pour les tâches */

    iface = G_LOADED_CONTENT_GET_IFACE(analysis->content);

    queue = get_work_queue();

    gid = g_work_queue_define_work_group(queue);

    analysis->success = iface->analyze(analysis->content, analysis->connect, analysis->cache, gid, status);

    if (analysis->success)
        handle_loaded_content(PGA_CONTENT_ANALYZED, analysis->content, gid, status);

    g_work_queue_delete_work_group(queue, gid);

}



/* ---------------------------------------------------------------------------------- */
/*                         VUES ET BASCULEMENT ENTRE LES VUES                         */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : panel = panneau affichant un contenu binaire.                *
*                                                                             *
*  Description : Fournit la station d'accueil d'un panneau d'affichage.       *
*                                                                             *
*  Retour      : Composant GTK fourni sans transfert de propriété.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GtkDockStation *get_dock_station_for_view_panel(GtkWidget *panel)
{
    GtkWidget *result;                      /* Support trouvé à retourner  */

    /**
     * La hiérarchie des composants empilés est la suivante :
     *
     *  - GtkBlockView / GtkGraphView / GtkSourceView (avec GtkViewport intégré)
     *  - GtkScrolledWindow
     *  - GtkDockStation
     *
     */

    result = gtk_widget_get_parent(panel);  /* ScrolledWindow */
    result = gtk_widget_get_parent(result);             /* DockStation */

    return GTK_DOCK_STATION(result);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : panel = panneau affichant un contenu binaire.                *
*                                                                             *
*  Description : Fournit le support défilant d'un panneau d'affichage.        *
*                                                                             *
*  Retour      : Composant GTK fourni sans transfert de propriété.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GtkWidget *get_scroll_window_for_view_panel(GtkWidget *panel)
{
    GtkWidget *result;                      /* Support trouvé à retourner  */

    /**
     * La hiérarchie des composants empilés est la suivante :
     *
     *  - GtkBlockView / GtkGraphView / GtkSourceView (avec GtkViewport intégré)
     *  - GtkScrolledWindow
     *  - GtkDockStation
     *
     */

    result = gtk_widget_get_parent(panel);  /* ScrolledWindow */

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : view = composant retourné par un contenu chargé.             *
*                                                                             *
*  Description : Fournit le panneau chargé inclus dans un affichage.          *
*                                                                             *
*  Retour      : Composant GTK fourni sans transfert de propriété.            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

GtkWidget *get_loaded_panel_from_built_view(GtkWidget *view)
{
    GtkWidget *result;                      /* Support trouvé à retourner  */

    if (G_IS_LOADED_PANEL(view))
        result = view;

    else
    {
        assert(GTK_IS_CONTAINER(view));

        result = NULL;

        void track_loaded_panel(GtkWidget *widget, GtkWidget **found)
        {
            if (*found == NULL)
            {
                if (G_IS_LOADED_PANEL(widget))
                    *found = widget;

                else if (GTK_IS_CONTAINER(widget))
                    gtk_container_foreach(GTK_CONTAINER(widget), (GtkCallback)track_loaded_panel, found);

            }

        }

        gtk_container_foreach(GTK_CONTAINER(view), (GtkCallback)track_loaded_panel, &result);

        assert(result != NULL);

    }

    g_object_ref(G_OBJECT(result));

    return result;

}
