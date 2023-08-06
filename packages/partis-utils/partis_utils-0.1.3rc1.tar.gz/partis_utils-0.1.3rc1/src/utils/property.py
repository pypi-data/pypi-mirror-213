from copy import copy

from .special import NOTSET


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class cached_property:
  """Simple cached property decorator, returns a *shallow copy* of the cached
  object on each call.
  """

  #-----------------------------------------------------------------------------
  def __init__( self, func, name = None ):

    self._func = func
    self.__doc__ = func.__doc__

    self._name = None if name is None else f'_p_{name}_cached'

  #-----------------------------------------------------------------------------
  def __set_name__(self, owner, name):
    self._name = f'_p_{name}_cached'

  #-----------------------------------------------------------------------------
  def __get__( self, obj, owner = None ):
    if obj is None:
      return self

    name = self._name

    # cannot use getattr since that may access from parents class cache
    val = obj.__dict__.get(name, NOTSET)

    if val is NOTSET:
      val = self._func(obj)
      # cannot set directly to __dict__
      setattr(obj, name, val)

    return copy(val)
