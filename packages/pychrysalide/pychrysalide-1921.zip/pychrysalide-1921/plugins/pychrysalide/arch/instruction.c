
/* Chrysalide - Outil d'analyse de fichiers binaires
 * instruction.c - équivalent Python du fichier "arch/instruction.h"
 *
 * Copyright (C) 2018-2020 Cyrille Bagard
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


#include "instruction.h"


#include <assert.h>
#include <malloc.h>
#include <string.h>
#include <pygobject.h>


#include <i18n.h>
#include <arch/instruction-int.h>
#include <plugins/dt.h>


#include "constants.h"
#include "operand.h"
#include "vmpa.h"
#include "../access.h"
#include "../helpers.h"
#include "../glibext/linegen.h"



/* -------------------- INTERFACE INTERNE POUR EXTENSIONS PYTHON -------------------- */


/* Définition générique d'une instruction d'architecture (instance) */
typedef struct _GPyArchInstruction
{
    GArchInstruction parent;                /* A laisser en premier        */

    char *cached_keyword;                   /* Conservation de constante   */

} GPyArchInstruction;


/* Définition générique d'une instruction d'architecture (classe) */
typedef struct _GPyArchInstructionClass
{
    GArchInstructionClass parent;           /* A laisser en premier        */

} GPyArchInstructionClass;


#define G_TYPE_PYARCH_INSTRUCTION            g_pyarch_instruction_get_type()
#define G_PYARCH_INSTRUCTION(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), G_TYPE_PYARCH_INSTRUCTION, GPyArchInstruction))
#define G_IS_PYTHON_INSTRUCTION(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), G_TYPE_PYARCH_INSTRUCTION))
#define G_PYARCH_INSTRUCTION_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), G_TYPE_PYARCH_INSTRUCTION, GPyArchInstructionClass))
#define G_IS_PYTHON_INSTRUCTION_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), G_TYPE_PYARCH_INSTRUCTION))
#define G_PYARCH_INSTRUCTION_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS((obj), G_TYPE_PYARCH_INSTRUCTION, GPyArchInstructionClass))


/* Indique le type défini pour une instruction d'architecture en Python. */
GType g_pyarch_instruction_get_type(void);

/* Initialise la classe générique des instructions en Python. */
static void g_pyarch_instruction_class_init(GPyArchInstructionClass *);

/* Initialise une instance d'opérande d'architecture. */
static void g_pyarch_instruction_init(GPyArchInstruction *);

/* Supprime toutes les références externes. */
static void g_pyarch_instruction_dispose(GPyArchInstruction *);

/* Procède à la libération totale de la mémoire. */
static void g_pyarch_instruction_finalize(GPyArchInstruction *);

/* Fournit le nom humain de l'instruction manipulée. */
static const char *g_pyarch_instruction_get_keyword(GPyArchInstruction *);



/* ------------------------ GLUE POUR CREATION DEPUIS PYTHON ------------------------ */


/* Accompagne la création d'une instance dérivée en Python. */
static PyObject *py_arch_instruction_new(PyTypeObject *, PyObject *, PyObject *);

/* Initialise la classe générique des instructions. */
static void py_arch_instruction_init_gclass(GPyArchInstructionClass *, gpointer);

/* Initialise une instance sur la base du dérivé de GObject. */
static int py_arch_instruction_init(PyObject *, PyObject *, PyObject *);



/* --------------------------- MANIPULATION DES OPERANDES --------------------------- */


/* Attache un opérande supplémentaire à une instruction. */
static PyObject *py_arch_instruction_attach_extra_operand(PyObject *, PyObject *);

/* Fournit tous les opérandes d'une instruction. */
static PyObject *py_arch_instruction_get_operands(PyObject *, void *);

/* Remplace un opérande d'une instruction par un autre. */
static PyObject *py_arch_instruction_replace_operand(PyObject *, PyObject *);

/* Détache un opérande liée d'une instruction. */
static PyObject *py_arch_instruction_detach_operand(PyObject *, PyObject *);

/* Détermine le chemin conduisant à un opérande. */
static PyObject *py_arch_instruction_find_operand_path(PyObject *, PyObject *);

/* Obtient l'opérande correspondant à un chemin donné. */
static PyObject *py_arch_instruction_get_operand_from_path(PyObject *, PyObject *);



/* ------------------- DEFINITION DES LIAISONS ENTRE INSTRUCTIONS ------------------- */


/* Fournit les origines d'une instruction donnée. */
static PyObject *py_arch_instruction_get_sources(PyObject *, void *);

/* Fournit les destinations d'une instruction donnée. */
static PyObject *py_arch_instruction_get_destinations(PyObject *, void *);



/* --------------------- INSTRUCTIONS D'ARCHITECTURES EN PYTHON --------------------- */


/* Fournit l'identifiant unique pour un ensemble d'instructions. */
static PyObject *py_arch_instruction_get_unique_id(PyObject *, void *);

/* Fournit la place mémoire d'une instruction. */
static PyObject *py_arch_instruction_get_range(PyObject *, void *);

/* Définit la localisation d'une instruction. */
static int py_arch_instruction_set_range(PyObject *, PyObject *, void *);

/* Fournit le nom humain de l'instruction manipulée. */
static PyObject *py_arch_instruction_get_keyword(PyObject *, void *);



/* ---------------------------------------------------------------------------------- */
/*                      INTERFACE INTERNE POUR EXTENSIONS PYTHON                      */
/* ---------------------------------------------------------------------------------- */


/* Indique le type défini pour une instruction d'architecture en Python. */
G_DEFINE_TYPE(GPyArchInstruction, g_pyarch_instruction, G_TYPE_ARCH_INSTRUCTION);


/******************************************************************************
*                                                                             *
*  Paramètres  : klass = classe à initialiser.                                *
*                                                                             *
*  Description : Initialise la classe générique des instructions en Python.   *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_pyarch_instruction_class_init(GPyArchInstructionClass *klass)
{
    GObjectClass *object;                   /* Autre version de la classe  */
    GArchInstructionClass *instr;           /* Encore une autre vision...  */

    object = G_OBJECT_CLASS(klass);

    object->dispose = (GObjectFinalizeFunc/* ! */)g_pyarch_instruction_dispose;
    object->finalize = (GObjectFinalizeFunc)g_pyarch_instruction_finalize;

    instr = G_ARCH_INSTRUCTION_CLASS(klass);

    instr->get_keyword = (get_instruction_keyword_fc)g_pyarch_instruction_get_keyword;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instance à initialiser.                              *
*                                                                             *
*  Description : Initialise une instance d'instruction d'architecture.        *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_pyarch_instruction_init(GPyArchInstruction *instr)
{

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instance d'objet GLib à traiter.                     *
*                                                                             *
*  Description : Supprime toutes les références externes.                     *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_pyarch_instruction_dispose(GPyArchInstruction *instr)
{
    G_OBJECT_CLASS(g_pyarch_instruction_parent_class)->dispose(G_OBJECT(instr));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instance d'objet GLib à traiter.                     *
*                                                                             *
*  Description : Procède à la libération totale de la mémoire.                *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_pyarch_instruction_finalize(GPyArchInstruction *instr)
{
    if (instr->cached_keyword)
        free(instr->cached_keyword);

    G_OBJECT_CLASS(g_pyarch_instruction_parent_class)->finalize(G_OBJECT(instr));

}


/******************************************************************************
*                                                                             *
*  Paramètres  : instr = instruction d'assemblage à consulter.                *
*                                                                             *
*  Description : Fournit le nom humain de l'instruction manipulée.            *
*                                                                             *
*  Retour      : Mot clef de bas niveau.                                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static const char *g_pyarch_instruction_get_keyword(GPyArchInstruction *instr)
{
    const char *result;                     /* Désignation à retourner     */

    result = instr->cached_keyword;

    return result;

}


/* ---------------------------------------------------------------------------------- */
/*                          GLUE POUR CREATION DEPUIS PYTHON                          */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : type = type du nouvel objet à mettre en place.               *
*                args = éventuelle liste d'arguments.                         *
*                kwds = éventuel dictionnaire de valeurs mises à disposition. *
*                                                                             *
*  Description : Accompagne la création d'une instance dérivée en Python.     *
*                                                                             *
*  Retour      : Nouvel objet Python mis en place ou NULL en cas d'échec.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *result;                       /* Objet à retourner           */
    PyTypeObject *base;                     /* Type de base à dériver      */
    bool first_time;                        /* Evite les multiples passages*/
    GType gtype;                            /* Nouveau type de processeur  */
    bool status;                            /* Bilan d'un enregistrement   */

    /* Validations diverses */

    base = get_python_arch_instruction_type();

    if (type == base)
    {
        result = NULL;
        PyErr_Format(PyExc_RuntimeError, _("%s is an abstract class"), type->tp_name);
        goto exit;
    }

    /* Mise en place d'un type dédié */

    first_time = (g_type_from_name(type->tp_name) == 0);

    gtype = build_dynamic_type(G_TYPE_PYARCH_INSTRUCTION, type->tp_name,
                               (GClassInitFunc)py_arch_instruction_init_gclass, NULL, NULL);

    if (first_time)
    {
        status = register_class_for_dynamic_pygobject(gtype, type, base);

        if (!status)
        {
            result = NULL;
            goto exit;
        }

    }

    /* On crée, et on laisse ensuite la main à PyGObject_Type.tp_init() */

    result = PyType_GenericNew(type, args, kwds);

 exit:

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : class  = classe à initialiser.                               *
*                unused = données non utilisées ici.                          *
*                                                                             *
*  Description : Initialise la classe générique des instructions.             *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void py_arch_instruction_init_gclass(GPyArchInstructionClass *class, gpointer unused)
{
    /// ....

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = objet à initialiser (théoriquement).                  *
*                args = arguments fournis à l'appel.                          *
*                kwds = arguments de type key=val fournis.                    *
*                                                                             *
*  Description : Initialise une instance sur la base du dérivé de GObject.    *
*                                                                             *
*  Retour      : 0.                                                           *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static int py_arch_instruction_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    unsigned short int uid;                 /* Indentifiant unique de type */
    const char *keyword;                    /* Désignation d'instruction   */
    int ret;                                /* Bilan de lecture des args.  */
    GPyArchInstruction *instr;              /* Instruction à manipuler     */

    static char *kwlist[] = { "uid", "keyword", NULL };

    /* Récupération des paramètres */

    ret = PyArg_ParseTupleAndKeywords(args, kwds, "Hs", kwlist, &uid, &keyword);
    if (!ret) return -1;

    /* Initialisation d'un objet GLib */

    ret = forward_pygobjet_init(self);
    if (ret == -1) return -1;

    /* Eléments de base */

    instr = G_PYARCH_INSTRUCTION(pygobject_get(self));

    instr->cached_keyword = strdup(keyword);

    g_arch_instruction_set_unique_id(G_ARCH_INSTRUCTION(instr), uid);

    return 0;

}



/* ---------------------------------------------------------------------------------- */
/*                             MANIPULATION DES OPERANDES                             */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : self = architecture concernée par la procédure.              *
*                args = instruction représentant le point de départ.          *
*                                                                             *
*  Description : Attache un opérande supplémentaire à une instruction.        *
*                                                                             *
*  Retour      : None.                                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_attach_extra_operand(PyObject *self, PyObject *args)
{
    GArchOperand *op;                       /* Opérande concerné à ajouter */
    int ret;                                /* Bilan de lecture des args.  */
    GArchInstruction *instr;                /* Instruction manipulée       */

    ret = PyArg_ParseTuple(args, "O&", convert_to_arch_operand, &op);
    if (!ret) return NULL;

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    g_object_ref(G_OBJECT(op));

    g_arch_instruction_attach_extra_operand(instr, op);

    Py_RETURN_NONE;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self   = objet représentant une instruction.                 *
*                unused = adresse non utilisée ici.                           *
*                                                                             *
*  Description : Fournit tous les opérandes d'une instruction.                *
*                                                                             *
*  Retour      : Valeur associée à la propriété consultée.                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_operands(PyObject *self, void *unused)
{
    PyObject *result;                       /* Instance à retourner        */
    GArchInstruction *instr;                /* Version native              */
    size_t count;                           /* Nombre d'opérandes présents */
    size_t i;                               /* Boucle de parcours          */
    GArchOperand *operand;                  /* Opérande à manipuler        */
    PyObject *opobj;                        /* Version Python              */
#ifndef NDEBUG
    int ret;                                /* Bilan d'une écriture d'arg. */
#endif

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    g_arch_instruction_lock_operands(instr);

    count = _g_arch_instruction_count_operands(instr);

    result = PyTuple_New(count);

    for (i = 0; i < count; i++)
    {
        operand = _g_arch_instruction_get_operand(instr, i);

        opobj = pygobject_new(G_OBJECT(operand));

#ifndef NDEBUG
        ret = PyTuple_SetItem(result, i, Py_BuildValue("O", opobj));
        assert(ret == 0);
#else
        PyTuple_SetItem(result, i, Py_BuildValue("O", opobj));
#endif

        g_object_unref(G_OBJECT(operand));

    }

    g_arch_instruction_unlock_operands(instr);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = architecture concernée par la procédure.              *
*                args = instruction représentant le point de départ.          *
*                                                                             *
*  Description : Remplace un opérande d'une instruction par un autre.         *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_replace_operand(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Bilan à retourner           */
    GArchOperand *old;                      /* Ancien opérande à remplacer */
    GArchOperand *new;                      /* Nouvel opérande à intégrer  */
    int ret;                                /* Bilan de lecture des args.  */
    GArchInstruction *instr;                /* Instruction manipulée       */
    bool status;                            /* Bilan de l'opération        */

    ret = PyArg_ParseTuple(args, "O&O&", convert_to_arch_operand, &old, convert_to_arch_operand, &new);
    if (!ret) return NULL;

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    status = g_arch_instruction_replace_operand(instr, old, new);

    if (status)
        g_object_ref(G_OBJECT(new));

    result = status ? Py_True : Py_False;
    Py_INCREF(result);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = architecture concernée par la procédure.              *
*                args = instruction représentant le point de départ.          *
*                                                                             *
*  Description : Détache un opérande liée d'une instruction.                  *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_detach_operand(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Bilan à retourner           */
    GArchOperand *target;                   /* Opérande ciblé par l'action */
    int ret;                                /* Bilan de lecture des args.  */
    GArchInstruction *instr;                /* Instruction manipulée       */
    bool status;                            /* Bilan de l'opération        */

    ret = PyArg_ParseTuple(args, "O&", convert_to_arch_operand, &target);
    if (!ret) return NULL;

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    status = g_arch_instruction_detach_operand(instr, target);

    result = status ? Py_True : Py_False;
    Py_INCREF(result);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = architecture concernée par la procédure.              *
*                args = instruction représentant le point de départ.          *
*                                                                             *
*  Description : Détermine le chemin conduisant à un opérande.                *
*                                                                             *
*  Retour      : Chemin d'accès à l'opérande ou None en cas d'absence.        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_find_operand_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Chemin à retourner          */
    GArchOperand *target;                   /* Opérande ciblé par l'action */
    int ret;                                /* Bilan de lecture des args.  */
    GArchInstruction *instr;                /* Instruction manipulée       */
    char *path;                             /* Chemin déterminé            */

#define ARCH_INSTRUCTION_FIND_OPERAND_PATH_METHOD PYTHON_METHOD_DEF         \
(                                                                           \
    find_operand_path, "$self, target, /",                                  \
    METH_VARARGS, py_arch_instruction,                                      \
    "Compute the path leading to an instruction operand.\n"                 \
    "\n"                                                                    \
    "The *target* has to be an instance of pychrysalide.arch.ArchOperand"   \
    " included in the instruction.\n"                                       \
    "\n"                                                                    \
    "The result is a string of the form 'n[:n:n:n]', where n is an"         \
    " internal index, or None if the *target* is not found. This kind of"   \
    " path is aimed to be built for the"                                    \
    " pychrysalide.arch.ArchInstruction.find_operand_path() function."      \
)

    ret = PyArg_ParseTuple(args, "O&", convert_to_arch_operand, &target);
    if (!ret) return NULL;

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    path = g_arch_instruction_find_operand_path(instr, target);

    if (path != NULL)
    {
        result = PyUnicode_FromString(path);
        free(path);
    }
    else
    {
        result = Py_None;
        Py_INCREF(result);
    }

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self = architecture concernée par la procédure.              *
*                args = instruction représentant le point de départ.          *
*                                                                             *
*  Description : Obtient l'opérande correspondant à un chemin donné.          *
*                                                                             *
*  Retour      : Opérande trouvé ou None en cas d'échec.                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_operand_from_path(PyObject *self, PyObject *args)
{
    PyObject *result;                       /* Trouvaille à retourner      */
    const char *path;                       /* Chemin à parcourir          */
    int ret;                                /* Bilan de lecture des args.  */
    GArchInstruction *instr;                /* Instruction manipulée       */
    GArchOperand *op;                       /* Opérande retrouvé           */

#define ARCH_INSTRUCTION_GET_OPERAND_FROM_PATH_METHOD PYTHON_METHOD_DEF     \
(                                                                           \
    get_operand_from_path, "$self, path, /",                                \
    METH_VARARGS, py_arch_instruction,                                      \
    "Retrieve an operand from an instruction by its path.\n"                \
    "\n"                                                                    \
    "This *path* is a string of the form 'n[:n:n:n]', where n is an"        \
    " internal index. Such a path is usually built by the"                  \
    " pychrysalide.arch.ArchInstruction.find_operand_path() function.\n"    \
    "\n"                                                                    \
    "The result is an pychrysalide.arch.ArchOperand instance, or"           \
    " None if no operand was found."                                        \
)

    ret = PyArg_ParseTuple(args, "s", &path);
    if (!ret) return NULL;

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    op = g_arch_instruction_get_operand_from_path(instr, path);

    if (op != NULL)
    {
        result = pygobject_new(G_OBJECT(op));
        g_object_unref(G_OBJECT(op));
    }
    else
    {
        result = Py_None;
        Py_INCREF(result);
    }

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                     DEFINITION DES LIAISONS ENTRE INSTRUCTIONS                     */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : self   = instruction d'architecture à manipuler.             *
*                unused = adresse non utilisée ici.                           *
*                                                                             *
*  Description : Fournit les origines d'une instruction donnée.               *
*                                                                             *
*  Retour      : Nombre de ces origines.                                      *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_sources(PyObject *self, void *unused)
{
    PyObject *result;                       /* Instance à retourner        */
    GArchInstruction *instr;                /* Version native              */
    size_t count;                           /* Nombre de liens présents    */
    size_t i;                               /* Boucle de parcours          */
    const instr_link_t *source;             /* Origine des liens           */
    PyObject *linked;                       /* Source de lien Python       */
    PyObject *type;                         /* Nature du lien en Python    */
#ifndef NDEBUG
    int ret;                                /* Bilan d'une écriture d'arg. */
#endif

#define ARCH_INSTRUCTION_SOURCES_ATTRIB PYTHON_GET_DEF_FULL                 \
(                                                                           \
    sources, py_arch_instruction,                                           \
    "Provide the instructions list driving to the current instruction.\n"   \
    "\n"                                                                    \
    "Each item of the resulting tuple is a pair of"                         \
    " pychrysalide.arch.ArchInstruction instance and"                       \
    " pychrysalide.arch.ArchInstruction.InstructionLinkType value."         \
)

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    g_arch_instruction_lock_src(instr);

    count = g_arch_instruction_count_sources(instr);

    result = PyTuple_New(count);

    for (i = 0; i < count; i++)
    {
        source = g_arch_instruction_get_source(instr, i);

        linked = pygobject_new(G_OBJECT(source->linked));
        type = cast_with_constants_group_from_type(get_python_arch_instruction_type(),
                                                   "InstructionLinkType", source->type);

#ifndef NDEBUG
        ret = PyTuple_SetItem(result, i, Py_BuildValue("(OO)", linked, type));
        assert(ret == 0);
#else
        PyTuple_SetItem(result, i, Py_BuildValue("(OO)", linked, type));
#endif

        unref_instr_link(source);

    }

    g_arch_instruction_unlock_src(instr);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self   = instruction d'architecture à manipuler.             *
*                unused = adresse non utilisée ici.                           *
*                                                                             *
*  Description : Fournit les destinations d'une instruction donnée.           *
*                                                                             *
*  Retour      : Nombre de ces destinations.                                  *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_destinations(PyObject *self, void *unused)
{
    PyObject *result;                       /* Instance à retourner        */
    GArchInstruction *instr;                /* Version native              */
    size_t count;                           /* Nombre de liens présents    */
    size_t i;                               /* Boucle de parcours          */
    const instr_link_t *dest;               /* Destination des liens       */
    PyObject *linked;                       /* Destination de lien Python  */
    PyObject *type;                         /* Nature du lien en Python    */
#ifndef NDEBUG
    int ret;                                /* Bilan d'une écriture d'arg. */
#endif

#define ARCH_INSTRUCTION_DESTINATIONS_ATTRIB PYTHON_GET_DEF_FULL            \
(                                                                           \
    destinations, py_arch_instruction,                                      \
    "Provide the instructions list following the current instruction.\n"    \
    "\n"                                                                    \
    "Each item of the resulting tuple is a pair of"                         \
    " pychrysalide.arch.ArchInstruction instance and"                       \
    " pychrysalide.arch.ArchInstruction.InstructionLinkType value."         \
)

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    g_arch_instruction_lock_dest(instr);

    count = g_arch_instruction_count_destinations(instr);

    result = PyTuple_New(count);

    for (i = 0; i < count; i++)
    {
        dest = g_arch_instruction_get_destination(instr, i);

        linked = pygobject_new(G_OBJECT(dest->linked));
        type = cast_with_constants_group_from_type(get_python_arch_instruction_type(),
                                                   "InstructionLinkType", dest->type);

#ifndef NDEBUG
        ret = PyTuple_SetItem(result, i, Py_BuildValue("(OO)", linked, type));
        assert(ret == 0);
#else
        PyTuple_SetItem(result, i, Py_BuildValue("(OO)", linked, type));
#endif

        unref_instr_link(dest);

    }

    g_arch_instruction_unlock_dest(instr);

    return result;

}



/* ---------------------------------------------------------------------------------- */
/*                       INSTRUCTIONS D'ARCHITECTURES EN PYTHON                       */
/* ---------------------------------------------------------------------------------- */


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = classe représentant une instruction.               *
*                closure = adresse non utilisée ici.                          *
*                                                                             *
*  Description : Fournit l'identifiant unique pour un ensemble d'instructions.*
*                                                                             *
*  Retour      : Identifiant unique par type d'instruction.                   *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_unique_id(PyObject *self, void *closure)
{
    PyObject *result;                       /* Conversion à retourner      */
    GArchInstruction *instr;                /* Version native              */
    itid_t uid;                             /* Identifiant unique associé  */

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));

    uid = g_arch_instruction_get_unique_id(instr);

    result = PyLong_FromUnsignedLong(uid);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = classe représentant une instruction.               *
*                closure = adresse non utilisée ici.                          *
*                                                                             *
*  Description : Fournit la place mémoire d'une instruction.                  *
*                                                                             *
*  Retour      : Valeur associée à la propriété consultée.                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_range(PyObject *self, void *closure)
{
    PyObject *result;                       /* Conversion à retourner      */
    GArchInstruction *instr;                /* Version native              */
    const mrange_t *range;                  /* Espace mémoire à exporter   */

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));
    range = g_arch_instruction_get_range(instr);

    result = build_from_internal_mrange(range);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self    = objet Python concerné par l'appel.                 *
*                value   = valeur fournie à intégrer ou prendre en compte.    *
*                closure = adresse non utilisée ici.                          *
*                                                                             *
*  Description : Définit la localisation d'une instruction.                   *
*                                                                             *
*  Retour      : Bilan de l'opération pour Python.                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static int py_arch_instruction_set_range(PyObject *self, PyObject *value, void *closure)
{
    int ret;                                /* Bilan d'analyse             */
    mrange_t *range;                        /* Espace mémoire à manipuler  */
    GArchInstruction *instr;                /* Version native              */

    ret = PyObject_IsInstance(value, (PyObject *)get_python_mrange_type());
    if (!ret) return -1;

    range = get_internal_mrange(value);

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));
    g_arch_instruction_set_range(instr, range);

    return 0;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : self   = classe représentant une instruction.                *
*                unused = adresse non utilisée ici.                           *
*                                                                             *
*  Description : Fournit le nom humain de l'instruction manipulée.            *
*                                                                             *
*  Retour      : Valeur associée à la propriété consultée.                    *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static PyObject *py_arch_instruction_get_keyword(PyObject *self, void *unused)
{
    PyObject *result;                       /* Trouvailles à retourner     */
    GArchInstruction *instr;                /* Version native              */
    const char *kw;                         /* Valeur récupérée            */

    instr = G_ARCH_INSTRUCTION(pygobject_get(self));
    kw = g_arch_instruction_get_keyword(instr);

    result = PyUnicode_FromString(kw);

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

PyTypeObject *get_python_arch_instruction_type(void)
{
    static PyMethodDef py_arch_instruction_methods[] = {
        {
            "attach_operand", py_arch_instruction_attach_extra_operand,
            METH_VARARGS,
            "attach_operand($self, op, /)\n--\n\nAdd a new operand to the instruction."
        },
        {
            "replace_operand", py_arch_instruction_replace_operand,
            METH_VARARGS,
            "replace_operand($self, old, new, /)\n--\n\nReplace an old instruction operand by a another one."
        },
        {
            "detach_operand", py_arch_instruction_detach_operand,
            METH_VARARGS,
            "detach_operand($self, target, /)\n--\n\nRemove an operand from the instruction."
        },
        ARCH_INSTRUCTION_FIND_OPERAND_PATH_METHOD,
        ARCH_INSTRUCTION_GET_OPERAND_FROM_PATH_METHOD,
        { NULL }
    };

    static PyGetSetDef py_arch_instruction_getseters[] = {
        {
            "uid", py_arch_instruction_get_unique_id, NULL,
            "Provide the unique identification number given to this kind of instruction.", NULL
        },
        {
            "range", py_arch_instruction_get_range, py_arch_instruction_set_range,
            "Give access to the memory range covered by the current instruction.", NULL
        },
        {
            "keyword", (getter)py_arch_instruction_get_keyword, (setter)NULL,
            "Give le name of the assembly instruction.", NULL
        },
        {
            "operands", (getter)py_arch_instruction_get_operands, (setter)NULL,
            "Provide the list of instruction attached operands.", NULL
        },
        ARCH_INSTRUCTION_SOURCES_ATTRIB,
        ARCH_INSTRUCTION_DESTINATIONS_ATTRIB,
        { NULL }
    };

    static PyTypeObject py_arch_instruction_type = {

        PyVarObject_HEAD_INIT(NULL, 0)

        .tp_name        = "pychrysalide.arch.ArchInstruction",
        .tp_basicsize   = sizeof(PyGObject),

        .tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_IS_ABSTRACT | Py_TPFLAGS_BASETYPE,

        .tp_doc         = "PyChrysalide instruction for a given architecture.",

        .tp_methods     = py_arch_instruction_methods,
        .tp_getset      = py_arch_instruction_getseters,

        .tp_init        = py_arch_instruction_init,
        .tp_new         = py_arch_instruction_new,

    };

    return &py_arch_instruction_type;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : module = module dont la définition est à compléter.          *
*                                                                             *
*  Description : Prend en charge l'objet 'pychrysalide.arch.ArchInstruction'. *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool ensure_python_arch_instruction_is_registered(void)
{
    PyTypeObject *type;                     /* Type Python 'ArchInstruc...'*/
    PyObject *module;                       /* Module à recompléter        */
    PyObject *dict;                         /* Dictionnaire du module      */

    type = get_python_arch_instruction_type();

    if (!PyType_HasFeature(type, Py_TPFLAGS_READY))
    {
        module = get_access_to_python_module("pychrysalide.arch");

        dict = PyModule_GetDict(module);

        if (!ensure_python_line_generator_is_registered())
            return false;

        if (!_register_class_for_pygobject(dict, G_TYPE_PYARCH_INSTRUCTION, type,
                                           &PyGObject_Type, get_python_line_generator_type(), NULL))
            return false;

        if (!define_arch_instruction_constants(type))
            return false;

    }

    return true;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : arg = argument quelconque à tenter de convertir.             *
*                dst = destination des valeurs récupérées en cas de succès.   *
*                                                                             *
*  Description : Tente de convertir en instruction d'architecture.            *
*                                                                             *
*  Retour      : Bilan de l'opération, voire indications supplémentaires.     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int convert_to_arch_instruction(PyObject *arg, void *dst)
{
    int result;                             /* Bilan à retourner           */

    result = PyObject_IsInstance(arg, (PyObject *)get_python_arch_instruction_type());

    switch (result)
    {
        case -1:
            /* L'exception est déjà fixée par Python */
            result = 0;
            break;

        case 0:
            PyErr_SetString(PyExc_TypeError, "unable to convert the provided argument to arch instruction");
            break;

        case 1:
            *((GArchInstruction **)dst) = G_ARCH_INSTRUCTION(pygobject_get(arg));
            break;

        default:
            assert(false);
            break;

    }

    return result;

}
