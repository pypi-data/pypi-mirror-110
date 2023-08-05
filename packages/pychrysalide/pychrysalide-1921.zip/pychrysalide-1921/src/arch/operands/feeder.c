
/* Chrysalide - Outil d'analyse de fichiers binaires
 * feeder.c - fourniture d'éléments non architecturaux
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
 *  along with Chrysalide.  If not, see <http://www.gnu.org/licenses/>.
 */


#include "feeder.h"


#include "feeder-int.h"



/* Procède à l'initialisation de l'interface de rassemblement. */
static void g_proxy_feeder_default_init(GProxyFeederInterface *);



/* Détermine le type d'une interface pour la Fourniture d'éléments non architecturaux. */
G_DEFINE_INTERFACE(GProxyFeeder, g_proxy_feeder, G_TYPE_OBJECT)


/******************************************************************************
*                                                                             *
*  Paramètres  : iface = interface GLib à initialiser.                        *
*                                                                             *
*  Description : Procède à l'initialisation de l'interface de rassemblement.  *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

static void g_proxy_feeder_default_init(GProxyFeederInterface *iface)
{

}


/******************************************************************************
*                                                                             *
*  Paramètres  : a = premier fournisseur à consulter.                         *
*                b = second fournisseur à consulter.                          *
*                                                                             *
*  Description : Compare un fournisseur avec un autre.                        *
*                                                                             *
*  Retour      : Bilan de la comparaison.                                     *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

int g_proxy_feeder_compare(const GProxyFeeder *a, const GProxyFeeder *b)
{
    int result;                             /* Bilan à retourner           */
    GProxyFeederIface *iface;               /* Interface utilisée          */

    iface = G_PROXY_FEEDER_GET_IFACE(a);

    result = iface->compare(a, b);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : feeder = fournisseur à traiter.                              *
*                line   = ligne tampon où imprimer l'élément donné.           *
*                                                                             *
*  Description : Traduit un fournisseur en version humainement lisible.       *
*                                                                             *
*  Retour      : -                                                            *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

void g_proxy_feeder_print(const GProxyFeeder *feeder, GBufferLine *line)
{
    GProxyFeederIface *iface;               /* Interface utilisée          */

    iface = G_PROXY_FEEDER_GET_IFACE(feeder);

    iface->print(feeder, line);

}


/******************************************************************************
*                                                                             *
*  Paramètres  : feeder = fournisseur à constituer.                           *
*                format = format binaire chargé associé à l'architecture.     *
*                pbuf   = zone tampon à remplir.                              *
*                                                                             *
*  Description : Charge un fournisseur depuis une mémoire tampon.             *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_proxy_feeder_unserialize(GProxyFeeder *feeder, GBinFormat *format, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GProxyFeederIface *iface;               /* Interface utilisée          */

    iface = G_PROXY_FEEDER_GET_IFACE(feeder);

    result = iface->unserialize(feeder, format, pbuf);

    return result;

}


/******************************************************************************
*                                                                             *
*  Paramètres  : feeder = fournisseur à consulter.                            *
*                pbuf   = zone tampon à remplir.                              *
*                                                                             *
*  Description : Sauvegarde un fournisseur dans une mémoire tampon.           *
*                                                                             *
*  Retour      : Bilan de l'opération.                                        *
*                                                                             *
*  Remarques   : -                                                            *
*                                                                             *
******************************************************************************/

bool g_proxy_feeder_serialize(const GProxyFeeder *feeder, packed_buffer_t *pbuf)
{
    bool result;                            /* Bilan à retourner           */
    GProxyFeederIface *iface;               /* Interface utilisée          */

    iface = G_PROXY_FEEDER_GET_IFACE(feeder);

    result = iface->serialize(feeder, pbuf);

    return result;

}
