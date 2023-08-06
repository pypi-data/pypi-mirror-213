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
import threading
from types import MethodType
from copy import copy, deepcopy

from collections import OrderedDict as odict
import rich
import rich.theme
import rich.logging
import rich.highlighter

from .fmt import (
  f )

from .hint import (
  HINT_LEVELS,
  HINT_LEVELS_DESC,
  HINT_LEVELS_TO_NUM,
  hint_level_num,
  hint_level_name,
  ModelHint,
  Loc )

# NOTE: import getLogger from here to ensure that the logger class has been
# customized before instantiated in by calling getLogger

#1cdc9a
#00d7af

# Extra Rich themes needed to render hints
custom_theme = rich.theme.Theme({
  'date' : 'dodger_blue1',
  'time' : 'bold cyan3',
  'time_us' : 'turquoise4',
  'tree' : 'grey50',
  'omit' : 'bold red1',
  'punctuate' : 'cyan',
  'qualifier' : 'bright_black',
  'literal' : 'grey50',
  'block' : 'grey82 on grey19',
  'repr.literal' : 'navajo_white1',
  'repr.code' : 'grey82 on grey19',
  'notset' : 'grey78',
  'trace' : 'grey78',
  'debug' : 'medium_purple1',
  'detail' : 'light_sky_blue1',
  'info' : 'light_sky_blue1',
  'success' : 'pale_green1',
  'warning' : 'orange3',
  'error' : '#ff5f5f',
  'critical' : 'red1' })

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
log_levels = HINT_LEVELS_TO_NUM

# levels which are not defined in base logging module
custom_log_levels = [
  (k,n,v)
  for (k,n,v) in HINT_LEVELS
  if not hasattr( logging, k ) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def add_log_level( cls, num, name ):
  """Add custom logging level to a logger
  """
  # uname = name.upper()
  name = name.lower()

  prev_log = getattr(cls, name, None)

  if prev_log is not None and not callable(prev_log):
    raise ValueError(f"Conflicting definitions for logger method: {name}")

  # This method was inspired by the answers to Stack Overflow post
  # http://stackoverflow.com/q/2183233/2988730, especially
  # http://stackoverflow.com/a/13638084/2988730
  def log_for_level( self, message, *args, **kwargs):
    if isinstance(message, ModelHint):
      message.level = name

    if prev_log is not None:
      return prev_log(self, message, *args, **kwargs )

    if self.isEnabledFor( num ):
      return self._log( num, message, args, **kwargs )

  setattr( cls, name, log_for_level )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CustomLogger(logging.getLoggerClass()):
  def hint( self, *args, **kwargs):
    if isinstance(args[0], ModelHint):
      hint = args[0]
      args = args[1:]

    elif isinstance(args[0], Exception):
      hint = ModelHint.cast(args[0], *args, **kwargs)
      args = tuple()
      kwargs = {}

    else:
      hint = ModelHint(*args, **kwargs)
      args = tuple()
      kwargs = {}

    self.log( hint.level_num, hint, *args, **kwargs )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
for name, num, v in HINT_LEVELS:
  add_log_level( CustomLogger, num, name )

logging.setLoggerClass(CustomLogger)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
getLogger = logging.getLogger

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def should_do_markup(file):
  """From pytest terminalwriter
  """
  if os.environ.get("PY_COLORS") == "1":
    return True
  if os.environ.get("PY_COLORS") == "0":
    return False
  if "NO_COLOR" in os.environ:
    return False
  if "FORCE_COLOR" in os.environ:
    return True
  return (
    hasattr(file, "isatty") and file.isatty() and os.environ.get("TERM") != "dumb" )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def feat_enabled(enabled, disabled):
  if not ( enabled or disabled ):
    return None

  if enabled:
    return True

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def logging_parser_add(parser):

  verbosity_default = 'info'
  verbosity_help = ""

  for name, doc in HINT_LEVELS_DESC.items():
    name = name.lower()
    msg_default = ' (default)' if name == verbosity_default else ''
    verbosity_help += f"  '{name}' {msg_default}: {doc}\n"

  parser.add_argument( "-l", "--log",
    type = str,
    default = None,
    help = "Redirect output to the given log file" )

  parser.add_argument( "-v", "--verbosity",
    type = str,
    default = verbosity_default,
    help = f"Log verbosity:\n{verbosity_help}" )

  parser.add_argument( "--color",
    action = 'store_true',
    help = "Enable color log output" )

  parser.add_argument( "--no-color",
    action = 'store_true',
    help = "Disable color log output" )

  parser.add_argument( "--ascii",
    action = 'store_true',
    help = "Disable non-ascii log output" )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def logging_parser_get(args):
  return dict(
    level = args.verbosity,
    filename = args.log,
    with_color = feat_enabled(args.color, args.no_color),
    with_unicode = not args.ascii )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def logging_parser_init(args):
  return init_logging(**logging_parser_get(args))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def init_logging(
  level,
  rank = None,
  filename = None,
  with_color = False,
  with_unicode = True ):

  # adapted from logging/__init__.py

  try:
    'f\ubaaar'.encode(sys.stdout.encoding)
  except UnicodeEncodeError:
    with_unicode = False

  force_terminal = True if with_color else None

  if with_color is None:
    with_color = should_do_markup(sys.stdout)

  _lock = threading.RLock()

  if _lock:
    _lock.acquire()

  try:

    # make sure custom hint levels are defined in loggers
    for name, num, v in custom_log_levels:
      logging.addLevelName( num, name.upper() )

    if isinstance( level, str ):
      log_level = hint_level_num( level )

    else:
      try:
        log_level = int( level )
      except:
        raise ValueError(
          f"Log verbosity must be string or integer {log_levels}: {level}")

    # if log_level < logging.INFO:
    #   if rank is None:
    #     format = "{name}:{levelname}: {message}"
    #   else:
    #     format = "%d:{name}:{levelname}: {message}" % rank
    # else:
    #   format = "{message}"

    format = "{message}"


    if filename and os.path.exists(filename):
      os.remove( filename )

    root = getLogger()

    for h in root.handlers[:]:
      root.removeHandler(h)
      h.close()


    fmt = HintFormatter(
      # level is needed here also to filter level nested hints
      level = log_level,
      fmt = format,
      style = '{',
      with_rich = with_color,
      with_unicode = with_unicode )

    handlers = list()

    if with_color:
      console = rich.console.Console(
        file = sys.stdout,
        theme = custom_theme,
        emoji = False,
        tab_size = 2,
        force_terminal = force_terminal,
        highlighter = rich.highlighter.NullHighlighter() )

      h_stdout = RichConsoleHandler(
        console = console )

    else:
      h_stdout = logging.StreamHandler(
        stream = sys.stdout )

    h_stdout.setFormatter( fmt )
    handlers.append( h_stdout )


    if filename:
      h_file = logging.FileHandler(
        filename,
        mode = 'a',
        encoding = 'ascii',
        errors = 'backslashreplace' )

      h_file.setFormatter( HintFormatter(
        # level is needed here also to filter level nested hints
        level = log_level,
        fmt = format,
        style = '{',
        with_rich = False ) )

      handlers.append( h_file )


    for h in handlers:

      root.addHandler( h )

    root.setLevel( log_level )

    logging.captureWarnings(True)

    # logging.info( f"Initialized logging: {hint_level_name(log_level)} ({log_level})" )

  finally:
    if _lock:
      _lock.release()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def record_to_hint( record ):
  """converts a logging record msg to be a ModelHint
  """

  hints = list()

  if record.exc_info is not None:
    _type, _value, _traceback = record.exc_info

    hints.append( ModelHint.cast( _value ) )

  msg = record.msg

  if not isinstance( msg, ModelHint ):
    if isinstance(msg, str) and record.args:
      msg = msg % record.args

    if hasattr(msg, 'model_hint'):
      hint = ModelHint.cast(msg)
      hint.hints.extend(hints)

    else:
      hint = ModelHint(
        msg,
        level = record.levelno)

  else:
    hint = type(msg)(
      msg = msg.msg,
      data = msg.data,
      format = msg.format,
      # NOTE: this overwrites the level of the original hint to be that was logged
      level = max( msg.level_num, record.levelno ),
      # loc = msg.loc if msg.loc else Loc(owner = record.name, time = record.created),
      loc = msg.loc,
      hints = msg.hints + hints )

    # if not hint.loc.time:
    #   hint.loc.time = record.created

  return hint

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogListHandler( logging.Handler ):
  """Collects log records in local list of hints

  Parameters
  ----------
  level : int
    The level enabled for the handler
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, level = logging.NOTSET ):
    super().__init__( level )

    self._hints = list()
    self._logs = list()

  #-----------------------------------------------------------------------------
  @property
  def hints(self):
    return self._hints

  #-----------------------------------------------------------------------------
  @property
  def logs(self):
    return self._logs

  #-----------------------------------------------------------------------------
  def clear( self ):
    self.hints.clear()
    self.logs.clear()

  #-----------------------------------------------------------------------------
  def emit( self, record ):

    hint = record_to_hint( record )

    self._hints.append( hint )

    self._logs.append( hint.to_dict() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RichConsoleHandler( logging.Handler ):
  """Collects log records in local list of hints

  Parameters
  ----------
  console : rich.console.Console
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, console, level = logging.NOTSET ):
    super().__init__( level )

    self._console = console

  #-----------------------------------------------------------------------------
  def emit( self, record ):

    try:
      self._console.print( self.format(record) )
    except Exception:
      self.handleError(record)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogChannelHandler( logging.Handler ):
  """Collects log records in local list

  Parameters
  ----------
  send_channel : SendChannel
  level : int
    The level enabled for the handler
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, send_channel, level = logging.NOTSET, **kwargs ):
    super().__init__( level )

    self._send_channel = send_channel
    self._kwargs = kwargs

  #-----------------------------------------------------------------------------
  def emit(self, record):

    exc_info = None

    if record.exc_info is not None:
      type, value, traceback = record.exc_info

      exc_info = ModelHint.cast( value, **self._kwargs ).to_dict()

    send_channel.send( dict(
      msg = record.msg,
      level = record.levelname,
      exc_info = exc_info ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintFormatter( logging.Formatter ):
  #-----------------------------------------------------------------------------
  def __init__( self,
    level,
    with_rich = False,
    with_unicode = True,
    *args, **kwargs ):
    super().__init__( *args, **kwargs )

    self._level_num = hint_level_num( level )
    self._with_rich = with_rich
    self._with_unicode = with_unicode

  #-----------------------------------------------------------------------------
  def format( self, record ):

    msg = record.msg

    if not isinstance(msg, ModelHint):
      # msg = ModelHint(
      #   msg,
      #   level = hint_level_name( record.levelno ) )

      msg = record_to_hint( record )

    msg = msg.fmt(
      level = self._level_num,
      with_rich = self._with_rich,
      with_unicode = self._with_unicode )

    return msg

    # hint = record.msg
    # record.msg = ""
    #
    # base = super().format( record )
    #
    # hint.level = record.levelno
    #
    # fhint = hint.fmt(
    #   level = self._level_num,
    #   with_rich = self._with_rich )
    #
    # message = base + fhint
    #
    # if self._with_rich:
    #   message = rich.text.Text.from_markup(message)
    #
    # return message

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class branched_log:
  #-----------------------------------------------------------------------------
  def __init__(self, log, name, msg):

    self._log_ori = log
    self._log = self._log_ori.getChild(name)
    self._log.propagate = False

    # NOTE: setting to logging.NOTSET delegates the level to the parent, but here
    # we want to capture all events, and filter them out later
    self._log.setLevel(1)

    self._handler = LogListHandler()
    self._log.addHandler( self._handler )
    self._msg = msg

  #-----------------------------------------------------------------------------
  def __enter__(self):
    self._handler.clear()
    return self._log

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):

    hint = ModelHint(
      self._msg,
      hints = self._handler.hints )

    self._log_ori.log(hint.level_num, hint)

    self._handler.clear()
    # don't handle errors here
    return False
