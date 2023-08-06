# -*- coding: UTF-8 -*-

import sys
import os
import gc
import inspect
import weakref
from inspect import getframeinfo, stack
import logging
import pprint
import traceback
import linecache
from copy import copy, deepcopy

from collections import OrderedDict as odict

log = logging.getLogger(__name__)




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def obj_referrer_chains( obj, depth = 10, fmt = False, width = 70, ignore = None, _depth = None, _chain = None ):
  """Gets all referrer chains to a given object

  Parameters
  ----------
  obj : object
  depth : int
    Maximum length of chain to return, starting at object
  fmt : bool
    Whether to format the results as strings.
    If False, returns referrer objects.
  ignore : set<int>
    Objects to ignore, and internal book-keeping of already visited objects.
    Will be updated in-place with all visited objects.
  _depth : int
    Internal book-keeping of current depth
  _chain : list<object>
    Internal book-keeping of current working chain


  Returns
  -------
  chains : list< list< object > >
    Each list is one possible referrer chain, starting at the given object.
    Circular references stop before repeating.
    Once a referrer appears in a chain, it will not be repeated in subsequent chains.
    Chains terminate at module-level objects.

  """

  depth = max( 1, int(depth) )

  if obj is None:
    return [[None,],]

  if ignore is None:
    ignore = set()

  if _depth is None:
    _depth = depth

  frame_id = id(sys._getframe())
  ignore.add( frame_id )
  ignore.add( id(obj) )

  if _chain is None:
    _chain = list()
  else:
    _chain = copy(_chain)

  ignore.add( id(_chain) )
  _chain.append(obj)

  chains = list()


  if _depth > 0 and not inspect.ismodule(obj):

    refs = gc.get_referrers(obj)
    refs_id = id(refs)
    ignore.add( refs_id )


    for ref in refs:
      _id = id(ref)

      if _id not in ignore:
        chains.extend( obj_referrer_chains(
          ref,
          depth = depth,
          ignore = ignore,
          _depth = _depth-1,
          _chain = _chain ) )

    refs = None
    ignore.remove( refs_id )

  if len(chains) == 0:
    chains.append( _chain )


  if _depth == depth:
    _chains = list()

    for chain in chains:
      if len(chain) > 1:
        _chains.append( chain[1:] )

    chains = _chains

    if fmt:
      _chains = list()

      for chain in chains:

        _chain = list()

        for ref in chain:

          _ref_str = str(ref)
          src_line = fmt_src_line(ref)

          _ref_str = fmt_limit( _ref_str, width )

          if src_line != "":
            src_line = f", {src_line}"

          _ref_str = f"{ref.__class__.__name__}: {id(ref)}{src_line}, {_ref_str}"

          _chain.append(_ref_str )


        _chains.append( _chain )

      chains = _chains

  ignore.remove( frame_id )

  return chains
