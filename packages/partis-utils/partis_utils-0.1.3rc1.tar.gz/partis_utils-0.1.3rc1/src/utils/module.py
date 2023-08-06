
import sys
import os.path as osp
import types
import importlib


from importlib.abc import MetaPathFinder
from importlib.util import find_spec

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LazyModule ( types.ModuleType ):
  """A module that lazily imports sub-modules/packages
  """

  #-----------------------------------------------------------------------------
  def __init__( self, name ):
    super().__init__( name )

    self._p_children = list()

  #-----------------------------------------------------------------------------
  def define( self,
    children ):
    """
    Parameters
    ----------
    children : list<str>
      list of sub-modules/packages that should be importable
    """

    self._p_children = children

  #-----------------------------------------------------------------------------
  def __getattribute__( self, name ):

    try:
      return super().__getattribute__(name)

    except AttributeError as e:

      if name in self._p_children:
        child = importlib.import_module(f"{self.__name__}.{name}")
        setattr( self, name, child )
        return child

      raise AttributeError(
        f"'{type(self).__name__}' object has no attribute '{name}'") from e


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AliasMetaFinder(MetaPathFinder):
  """Provides for aliasing module import

  Parameters
  ----------
  fullname : str
    Fully qualified name of the module
  aliasname : str
    An alias import path for the module that will be re-directed to `fullname`
  """

  def __init__(self, fullname, aliasname):
    self.fullname = fullname
    self.aliasname = aliasname

  def find_spec(self, fullname, path, target=None):

    if fullname.startswith(self.aliasname):
      if fullname == self.aliasname:
        return find_spec(self.fullname)

      sub = fullname[len(self.aliasname):]

      if sub[0] == '.':
        return find_spec(self.fullname + sub) 

    return None
