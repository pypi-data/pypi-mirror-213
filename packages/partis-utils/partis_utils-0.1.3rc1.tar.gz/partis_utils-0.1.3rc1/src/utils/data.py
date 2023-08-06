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
from collections.abc import (
  Sequence,
  Mapping,
  MutableMapping )

log = logging.getLogger(__name__)

protected_attr = [ '_p_', '__' ]
mapping_attrs = [ 'get', 'items', 'values', 'keys' ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def attrs_modifiable( obj ):
  return (
    not hasattr( obj, '_p_attrs_modify' )
    or obj._p_attrs_modify )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class attrs_modify:
  #-----------------------------------------------------------------------------
  def __init__( self, obj ):
    self._obj = obj

  #-----------------------------------------------------------------------------
  def __enter__(self):
    self._obj._p_attrs_modify = True

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):
    self._obj._p_attrs_modify = False


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class adict_frozen( Mapping ):
  """Attribute accessed ordered dictionary with fixed attribute values

  .. note::

    New (key,value) items must be added using the Mapping method(s), but once
    added they may be accessed as attributes.
    Attempting to assign a new key as an attributed before doing this will
    raise an AttributeError.
    This is only needed the first time the attribute is defined.
    Subsequent accesses to an existing attribute do not need to use the context.

  .. note::

    Classes deriving from this class must using the context manager
    :class:`attrs_modify <partis.utils.data.attrs_modify>` whenever new
    instance attributes need to be added (those not part of the mapping).

  """
  #-----------------------------------------------------------------------------
  def __new__( cls, *args, **kwargs ):

    self = super().__new__( cls )
    self._p_attrs_modify = False

    with attrs_modify( self ):
      self._p_dict = None

    return self

  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):

    self._p_dict = odict( *args, **kwargs )


  #-----------------------------------------------------------------------------
  def __copy__( self ):
    obj = copy(super())
    obj._p_dict = copy( self._p_dict )
    return obj

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return f"{type(self).__name__}({list(self._p_dict.items())})"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  def __setattr__( self, name, val ):
    """
    Parameters
    ----------
    name : str
    val : object
    """

    try:

      if name != '_p_attrs_modify' and not attrs_modifiable( self ):
        super().__getattribute__(name)

      object.__setattr__( self, name, val )

    except AttributeError as e:

      if self._p_dict is not None and name in self._p_dict:
        self._p_dict[name] = val

      else:
        raise AttributeError(
          f"'{type(self).__name__}' object has no key '{name}'."
          " New keys must be added using a Mapping method;"
          f" E.G. x['{name}'] = {val}" ) from e


  #-----------------------------------------------------------------------------
  def __getattribute__( self, name ):
    """
    Parameters
    ----------
    name : str
      Key to set in underlying dictionary

    Returns
    -------
    val :
      Value for key
    """

    try:
      return super().__getattribute__(name)

    except AttributeError as e:

      if self._p_dict is not None and name in self._p_dict:
        return self._p_dict[name]

      raise AttributeError(
        f"'{type(self).__name__}' object has no key '{name}'") from e


  #-----------------------------------------------------------------------------
  def __len__( self ):
    return len(self._p_dict)

  #-----------------------------------------------------------------------------
  def __iter__( self ):
    """Iterator of underlying dictionary items

    Returns
    -------
     : iterator[ tuple[ object, object ] ]
    """
    return iter(self._p_dict)

  #-----------------------------------------------------------------------------
  def keys( self ):
    return self._p_dict.keys()

  #-----------------------------------------------------------------------------
  def values( self ):
    return self._p_dict.values()

  #-----------------------------------------------------------------------------
  def items( self ):
    return self._p_dict.items()

  #-----------------------------------------------------------------------------
  def get( self, key, default = None ):
    return self._p_dict.get( key, default )

  #-----------------------------------------------------------------------------
  def __getitem__( self, key ):
    if key not in self._p_dict:
      raise KeyError(
        f"'{key}'")

    return self._p_dict[key]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class adict_struct( adict_frozen ):
  """Attribute accessed ordered dictionary with fixed attributes

  """

  #-----------------------------------------------------------------------------
  def __setitem__( self, key, val ):

    if key not in self._p_dict:
      raise ValueError(
        f"'{type(self).__name__}' keys may not be added dynamically: {key}")


    self._p_dict[ key ] = val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class adict( adict_struct, MutableMapping ):
  """Attribute access to an underlying ordered dictionary

  This class does not have the typical dictionary attribute/methods, but does act
  as an iterable of the underlying dictionary items.

  Note
  ----
  Only string keys may be accessed as attributes.
  """

  #-----------------------------------------------------------------------------
  def __setitem__( self, key, val ):

    self._p_dict[ key ] = val

  #-----------------------------------------------------------------------------
  def __delitem__( self, key ):
    self._p_dict.__delitem__( key )

  #-----------------------------------------------------------------------------
  def popitem( self ):
    """Remove and return a (key, value) pair from the dictionary.
    Pairs are returned in LIFO order.
    """
    return self._p_dict.popitem()

  #-----------------------------------------------------------------------------
  def clear( self ):
    """Remove all items from the dictionary.
    """
    return self._p_dict.clear()

  #-----------------------------------------------------------------------------
  def update( self, other ):
    """Update the dictionary with the key/value pairs from other,
    overwriting existing keys
    """
    for k, v in other.items():
      self[k] = v

  #-----------------------------------------------------------------------------
  def setdefault( self, key, default = None ):
    """If key is in the dictionary, return its value.
    If not, insert key with a value of default and return default.
    default defaults to None.
    """
    return self._p_dict.setdefault( key, default )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class owdict( odict ):
  """Ordered dictionary of weak-reference values

  Note
  ----
  https://docs.python.org/3/library/weakref.html
  Several built-in types such as list and dict do not directly support weak
  references but can add support through subclassing:
  CPython implementation detail: Other built-in types such as tuple and int do
  not support weak references even when subclassed.
  """

  #-----------------------------------------------------------------------------
  def __getitem__( self, key ):
    ref = super().__getitem__( key )

    return ref()

  #-----------------------------------------------------------------------------
  def __setitem__( self, key, value ):

    super().__setitem__( key, weakref.ref( value ) )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class rdict( odict ):
  """Recursively accessed ordered dictionary
  """

  #-----------------------------------------------------------------------------
  def __getitem__( self, *args ):

    if len(args) == 1:
      key = args[0]
    else:
      key = args

    if isinstance( key, list ) or isinstance( key, tuple ):
      val = None

      if len(key) > 0:
        val = super().__getitem__( key[0] )

      if len(key) > 1:
        val = val[ key[1:] ]

      return val

    return super().__getitem__( key )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class rlist( list ):
  """Recursively accessed list
  """

  #-----------------------------------------------------------------------------
  def __getitem__( self, *args ):

    if len(args) == 1:
      key = args[0]
    else:
      key = args

    if isinstance( key, list ) or isinstance( key, tuple ):
      val = self

      if len(key) == 0:
        raise ValueError("recursive keys must have at least one entry")

      for k in key:
        val = val[k]

      return val

    return super().__getitem__( key )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def update_recursive( d, u ):
  """Recusively updates a dictionary and/or list with a new set of values

  - Dictionaries are merged, d updated by u
  - Lists are appended, d + u
  - Tuples are *replaced* by u.
  - If any value is None, the existing value is *not* overriden.
  """

  log.debug(f"update_override: {d} + {u}")

  if d is None:
    return u

  if u is None:
    return d

  if isinstance( u, Sequence ) and not isinstance(u, str):
    if isinstance(u, tuple):
      return u

    if isinstance(d, tuple):
      return d

    if not isinstance( d, Sequence ) or isinstance(d, str):
      raise ValueError(f"input is not a Sequence: {type(d)}")

    _d = list(d)

    _d += [v for v in u if (v is not None and v not in _d)]

    return _d

  if isinstance( u, Mapping ):
    if not isinstance( d, Mapping ):
      raise ValueError(f"input is not a Mapping: {type(d)}")

    keys = list(d.keys())
    keys += [k for k in u.keys() if k not in keys]

    _d = {}

    for k in keys:
      _d[k] = update_recursive(d.get(k, None), u.get(k, None))

    return _d

  return u
