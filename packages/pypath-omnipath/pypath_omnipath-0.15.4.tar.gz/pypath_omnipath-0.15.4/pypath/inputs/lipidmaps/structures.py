#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright
#  2014-2023
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  Authors: Dénes Türei (turei.denes@gmail.com)
#           Nicolàs Palacio
#           Sebastian Lobentanzer
#           Erva Ulusoy
#           Olga Ivanova
#           Ahmet Rifaioglu
#           Sebastian Lobentanzer
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

"""
Structures from the Human Metabolome Database (HMDB).
"""

import pypath.formats.sdf as sdfparser
import pypath.resources.urls as urls
import pypath.share.curl as curl


def sdf():
    """
    Download and open the SDF file with all LipidMaps (LMSD) structures.
    """

    url = urls.urls['lipidmaps']['sdf']
    c = curl.Curl(
        url,
        large = True,
        silent = False,
        default_mode = 'rb',
        compr = 'zip',
        files_needed = ['structures.sdf'],
    )

    return sdfparser.SdfReader(
        c.result['structures.sdf'],
        names = {
            'HMDB_ID': 'hmdb_id',
            'SMILES': 'smiles',
            'PUBCHEM_CID': 'pubchem',
            'SWISSLIPIDS_ID': 'swisslipids',
            'LM_ID': 'lipidmaps',
        }
    )
