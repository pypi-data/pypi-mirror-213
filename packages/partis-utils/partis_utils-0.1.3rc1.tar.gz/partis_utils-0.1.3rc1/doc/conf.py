# -*- coding: utf-8 -*-

from partis.utils.sphinx import basic_conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# configuration
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

globals().update( basic_conf(
  package = 'partis-utils',
  copyright_year = '2022' ) )

intersphinx_mapping['partis.pyproj'] = (
  "https://nanohmics.bitbucket.io/doc/partis/pyproj",
  None )
