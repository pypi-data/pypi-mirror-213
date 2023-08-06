# -*- coding: UTF-8 -*-

import os
import re

try:
  from importlib.metadata import distributions

except ImportError:
  from importlib_metadata import distributions

from partis.utils import getLogger
log = getLogger(__name__)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PluginError( Exception ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Plugin:
  """Base class for all Partis plugins
  """
  package = ''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PluginManager:
  """Manages plugins
  """
  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__(*args, **kwargs)

    self._loaded = False
    self._groups = set()
    self._plugins = list()

    # add all install partis package names as detected group names
    for dist in distributions():
      name = dist.metadata['Name']
      name = re.sub( r"[^\w]+", "_", name )

      if name.startswith(f"partis_"):
        self._groups.add(name)

  #-----------------------------------------------------------------------------
  def register_group( self, name ):
    self._groups.add(name)

  #-----------------------------------------------------------------------------
  def plugins( self, cls = Plugin ):
    """Get all plugins that are an instance of the given plugin class
    """
    self.ensure_loaded()

    if not issubclass( cls, Plugin ):
      raise PluginError(
        f"cls must be a subclass of Plugin: {cls}" )

    return [ p for p in self._plugins if isinstance( p, cls ) ]

  #-----------------------------------------------------------------------------
  def register_plugin( self,
    plugin ):

    if not isinstance( plugin, Plugin ):
      log.error(
        f"plugin must be a Plugin: {type(plugin)}")

      return

    if plugin not in self._plugins:
      self._plugins.append(plugin)

  #-----------------------------------------------------------------------------
  def ensure_loaded( self ):
    if self._loaded:
      return

    self.load_plugins()

  #-----------------------------------------------------------------------------
  def load_plugins( self ):

    self._loaded = True

    for dist in distributions():

      eps = [
        ep
        for ep in dist.entry_points
        if re.sub( r"[^\w]+", "_", ep.group ) in self._groups ]

      name = dist.metadata['Name']

      for ep in eps:

        try:

          plugins = ep.load()()

        except Exception as e:
          log.error(
            f'Entry point {name}, {ep.group}, {ep.name}, {ep.value}'
            f' schema plugin could not be loaded',
            exc_info = True )

          continue

        if isinstance( plugins, Plugin ):
          plugins = [ plugins, ]

        for plugin in plugins:
          try:
            plugin.package = name

            self.register_plugin( plugin = plugin )

          except PluginError as e:
            log.error(
              f'Entry point {ep.group}, {ep.name}, {ep.value} from {name}'
              f' plugin could not be registered: {plugin}',
              exc_info = True )

            continue

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
plugin_manager = PluginManager()
