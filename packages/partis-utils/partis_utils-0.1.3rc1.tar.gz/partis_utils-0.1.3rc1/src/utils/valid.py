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
def isinstance_any( obj, cls ):
  cls = ensure_iterable( cls )

  return any( isinstance(obj, c) for c in cls )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def issubclass_any( obj, cls ):
  cls = ensure_iterable( cls )

  return any( issubclass_any(obj, c) for c in cls )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def valid_list( obj, size = None, types = None, classes = None, validate = None ):
  """
  Parameters
  ----------
  obj : list<object>
    List to be validated
  size : None | int
    Valid list size.
  types : None | class | list<class>
    Valid instance classes.
  classes : None | class | list<class>
    Valid subclass classes.
  validate : None | callable
    Extra validation function for items in list:

      ``validate( o : object ) -> bool``

  Returns
  -------
  valid : bool
    True if validation passed.
  """

  if size is not None and len( obj ) != size:
    return False

  if types is not None:
    types = ensure_iterable( types )

    if not all( any( isinstance( o, t ) for t in types ) for o in obj ):
      return False

  if classes is not None:
    classes = ensure_iterable( classes )

    if not all( any( issubclass( o, t ) for t in classes ) for o in obj ):
      return False

  if validate is not None:

    if not all( validate( o ) for o in obj ):
      return False

  return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def ensure_iterable(
  obj,
  size = None,
  cls = None,
  iter_types = None ):
  """Ensures a list, converting to a list if necessary

  Parameters
  ----------
  obj : None | object

    If a list, returns the list.
    If None, converts to an empty list, or a list of None of ``size``.
    Otherwise, creates a list with ``obj`` as the only item, or replicated
    to a list of ``size``.

  size : None | int

    If not None, and ``obj`` is not a list, creates a list of this size with
    ``obj`` replicated.

  cls : None | type

    default: list

  iter_types : None | set<type>

    List of iterable types that should not be expanded to a list, instead ensuring
    a list of items of those types.
    ( default: { str, dict, bytes, bytearray, memoryview } )

  Returns
  -------
  cls
  """

  if cls is None:
    cls = list

  if isinstance( obj, cls ):
    return obj

  if obj is None:
    # empty list.
    if size is None:
      return cls()
    else:
      return cls( [ None, ] * size )

  if iter_types is None:
    iter_types = { str, dict, bytes, bytearray, memoryview }

  if any( isinstance( obj, t ) for t in iter_types ):
    if size is None:
      return cls([ obj, ])
    else:
      return cls([ obj, ] * size)

  try:
    # blindly convert to list
    return cls( obj )

  except TypeError:
    # not iterable
    if size is None:
      return cls([ obj, ])
    else:
      return cls([ obj, ] * size )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def ensure_callable(
  obj,
  default = None ):
  """Ensures a callable, converting to a value to function

  Parameters
  ----------
  obj : None | object

    If a callable, returns the callable.
    If object, converts to a callable that returns the object

  default : None | object

    Default value to use if `obj` is `None`

  Returns
  -------
  : callable
  """

  if obj is None:
    obj = default

  if callable( obj ):
    return obj

  return lambda *args, **kwargs: obj
