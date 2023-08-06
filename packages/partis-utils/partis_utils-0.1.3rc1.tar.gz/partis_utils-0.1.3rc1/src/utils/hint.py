from __future__ import annotations
from typing import (
  Any,
  Literal)
import os
import os.path as osp
import inspect
import importlib
import logging
import traceback
import linecache
from pathlib import Path
from collections import (
  OrderedDict as odict)
from collections.abc import (
  Mapping,
  Sequence)
from rich.text import (
  Span,
  Text)
from .fmt import (
  ReprHighlighter,
  rich_time,
  repr_rec,
  LiteralHighlighter,
  join_attr_path,
  split_lines,
  wrap_lines,
  indent_lines,
  fmt_obj)
from .special import (
  NoType,
  NotSet)

try:
  from ruamel.yaml.comments import CommentedBase, CommentedMap, CommentedSeq
except ImportError:

  CommentedBase = NoType
  CommentedMap = NoType
  CommentedSeq = NoType

log = logging.getLogger(__name__)

rich_repr_highlight = ReprHighlighter()
rich_literal_highlight = LiteralHighlighter()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
TREE_CHAR_U = {
  # alts: ⌘
  'loc'         : '◹ ',
  # alts: ┯
  'more'        : '● ',
  'branch'      : '├╸',
  # alts: ├━
  'branch_more' : '├─',
   # alts: ╎, ┆, ┊
  'skip'        : '│ ',
  'end'         : '╰╸',
  # alts: ╰━
  'end_more'    : '╰─',
  'related'     : ': ',
  'identity'    : ' ≡ ',
  'result'      : ' → '}

TREE_CHAR_A = {
  'loc'         : '> ',
  'more'        : '* ',
  'branch'      : '- ',
  'branch_more' : '+ ',
  'skip'        : '| ',
  'end'         : '- ',
  'end_more'    : '+ ',
  'related'     : ': ',
  'identity'    : ' := ',
  'result'      : ' -> ' }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HINT_LEVELS = [
  ( 'notset',
    logging.NOTSET,
    """Any information""" ),
  ( 'trace',
    ( logging.NOTSET + logging.DEBUG ) // 2,
    """Internal program state information, such as values of variables.""" ),
  ( 'debug',
    logging.DEBUG,
    """Debugging information, typically of interest only when diagnosing problems.""" ),
  ( 'detail',
    ( logging.DEBUG + logging.INFO ) // 2,
    """Detailed information about the progress of an operation that a user may
    find informative, such as the intermediate results of a larger operation.""" ),
  ( 'info',
    logging.INFO,
    """Information about an operation being performed.""" ),
  ( 'success',
    ( logging.INFO + logging.WARNING ) // 2,
    """Information of a result that is considered valid.""" ),
  ( 'warning',
    logging.WARNING,
    """Information of a result that is suspected to be invalid,
    but the expected progress of an operation was not interrupted.""" ),
  ( 'error',
    logging.ERROR,
    """Information of a result preventing the expected progress of an operation.""" ),
  ( 'critical',
    logging.CRITICAL,
    """An error occured that may prevent the program from continuing.""" ) ]

# sort by numeric levels to ensure proper order
HINT_LEVELS = sorted(
  HINT_LEVELS,
  key = lambda obj: obj[1] )

# cleanup description strings
HINT_LEVELS = [
  (str(k).upper().strip(), int(n), inspect.cleandoc(v) )
  for (k,n,v) in HINT_LEVELS ]

# mapping of level names to descriptions
HINT_LEVELS_NAME = tuple([ k for (k,n,v) in HINT_LEVELS ])
HINT_LEVELS_DESC = odict( [ (k,v) for (k,n,v) in HINT_LEVELS ] )
HINT_LEVELS_TO_NUM = odict( [ (k,n) for (k,n,v) in HINT_LEVELS ] )

globals().update(HINT_LEVELS_TO_NUM)

DATA_FORMATS = (
  'auto',
  'block',
  'literal',
  'markup')

DATA_RELATIONS = (
  'related',
  'identity',
  'result' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hint_level_name( num: int ) -> str:
  """Returns the closest textual representation of a numeric level

  Parameters
  ----------
  num:
    Level number in the range [0,50]

  Returns
  -------
  name:
    One of the textual level names :data:`HINT_LEVELS <partis.utils.hint.HINT_LEVELS>`
    that has the highest numeric level that is <= ``num``.

  """

  try:
    # ensure level can be cast to an integer
    num = int(num)
  except Exception as e:
    raise TypeError(f"Level must be a number: {num}") from e

  # search starting with highest numeric level
  for (k,n,v) in HINT_LEVELS[::-1]:
    # find highest level name that is less-than or equal to given level number
    if n <= num:
      return k

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hint_level_num( name ):
  """Returns the closest textual representation of a numeric level

  Parameters
  ----------
  name : str | int
    One of the textual level names :data:`HINT_LEVELS <partis.utils.hint.HINT_LEVELS>`.

  Returns
  -------
  num : int
    Level number in the range [0,50]

  """

  if isinstance( name, int ):
    # convenience use to simply ensure a level number
    return name

  if not isinstance( name, str ):
    raise ValueError(f"Level name must be a string: {name}")

  # standardize name case
  name = name.upper().strip()

  if name not in HINT_LEVELS_NAME:
    raise ValueError(f"Level must be one of {HINT_LEVELS_NAME}: {name}")

  return HINT_LEVELS_TO_NUM[name]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ModelHint:
  rf"""Hint for diagnosing/resolving a given application model error

  Parameters
  ----------
  msg:
    A message for the hint.
    :func:`inspect.cleandoc` is applied to the message.
  data:
    Data associated with the message.
    If not a string, the object will be converted to a string using :func:`fmt_obj`.
  format:
    Hint for the format of the data
    One of ``{DATA_FORMATS}``.
  relation:
    How the data is related to the message.
    One of ``{DATA_RELATIONS}``.
  loc:
    Information on the location to which the hint corresponds.
  level:
    Level of the model hint.
    If given as an integer number, the level number of the hint will also have
    this value, but the name will be set from highest numeric level that is
    <= the given number.
    One of ``{HINT_LEVELS_NAME}``.
    default: 'info'.
  hints:
    Additional (child) hints supporting this hint.
  """

  registry = []

  #-----------------------------------------------------------------------------
  def __init__( self,
    msg: str = None,
    data: Any = None,
    format: Literal[DATA_FORMATS] = None,
    relation: Literal[DATA_RELATIONS] = None,
    loc: Loc = None,
    level: Literal[HINT_LEVELS_NAME] = None,
    hints: list[ModelHint] = None ):

    if isinstance(hints, str) or not isinstance(hints, (Sequence, Mapping)):
      hints = [hints]

    if level is None:
      _hints = [h for h in hints if isinstance(h, ModelHint)]

      if len(_hints) > 0:
        level = max([ h.max_level_num for h in _hints])

      else:
        level = 'INFO'


    self._level = 'NotSet'
    self._level_num = 0
    self.level = level

    self.msg = msg
    self.data = data
    self.format = format
    self.relation = relation
    self.loc = loc
    self.hints = hints

  #-----------------------------------------------------------------------------
  def to_dict(self, checked = None):
    if checked is None:
      checked = list()

    elif self in checked:
      return {
        'msg' : f"[circular reference '{self.msg}']" }

    checked.append(self)

    return {
      'msg' : self._msg,
      'data' : self._data,
      'format' : self._format,
      'relation' : self._relation,
      'loc' : self._loc.to_dict(),
      'level' : self._level,
      'hints' : [ h.to_dict(checked = checked) for h in self._hints ] }

  #-----------------------------------------------------------------------------
  @classmethod
  def from_dict(cls, d):
    d = { k:v for k,v in d.items() if k in inspect.getfullargspec(cls.__init__)[0][1:] }

    loc = Loc.from_dict(d.pop('loc', None))

    hints = [cls.from_dict(h) for h in d.pop('hints', []) if h is not None]

    return cls(**d, loc = loc, hints = hints)

  #-----------------------------------------------------------------------------
  @property
  def msg( self ):
    return self._msg

  #-----------------------------------------------------------------------------
  @msg.setter
  def msg(self, val):

    if val is None:
      val = ""

    elif not isinstance(val, Text):
      val = inspect.cleandoc(str(val))

    self._msg = val

  #-----------------------------------------------------------------------------
  @property
  def data( self ):
    return self._data

  #-----------------------------------------------------------------------------
  @data.setter
  def data(self, val):

    if val is None:
      val = ""

    elif not isinstance(val, str):
      val = fmt_obj( val )

    self._data = val

  #-----------------------------------------------------------------------------
  @property
  def format( self ):
    return self._format

  #-----------------------------------------------------------------------------
  @format.setter
  def format(self, val):
    if val is None:
      val = DATA_FORMATS[0]

    if val not in DATA_FORMATS:
      raise ValueError(
        f"Hint data 'format' must be one of {DATA_FORMATS}: {val}")

    self._format = val

  #-----------------------------------------------------------------------------
  @property
  def relation( self ):
    return self._relation

  #-----------------------------------------------------------------------------
  @relation.setter
  def relation(self, val):
    if val is None:
      val = DATA_RELATIONS[0]

    if val not in DATA_RELATIONS:
      raise ValueError(
        f"Hint data 'relation' must be one of {DATA_RELATIONS}: {val}")

    self._relation = val

  #-----------------------------------------------------------------------------
  @property
  def loc( self ):
    return self._loc

  #-----------------------------------------------------------------------------
  @loc.setter
  def loc(self, val):
    if not isinstance(val, Loc):
      if isinstance(val, str):
        val = Loc(val)

      elif isinstance(val, Mapping):
        val = Loc(**val)

      elif isinstance(val, Sequence):
        val = Loc(*val)

      elif val is None:
        val = Loc()
      else:
        val = Loc(str(val))

    self._loc = val

  #-----------------------------------------------------------------------------
  @property
  def level( self ):
    return self._level

  #-----------------------------------------------------------------------------
  @level.setter
  def level( self, level ):

    # standardize level name/number
    if isinstance( level, str ):
      level = level.upper()
      # convert to number, standardize name
      level_num = hint_level_num( level )

    else:
      # convert to name
      _level = hint_level_name( level )
      # NOTE: this does not alter the level number even if it is not one of the
      # pre-defined ones, allowing fine-grained numbers.
      # However, the name is still the nearest one less than given number
      # to be user-friendly
      # NOTE: casting after call to level_name, which will raise exception if
      # it couldn't be cast
      level_num = int(level)
      level = _level

    self._level = level
    self._level_num = level_num

  #-----------------------------------------------------------------------------
  @property
  def level_num( self ):
    return self._level_num

  #-----------------------------------------------------------------------------
  @property
  def hints( self ):
    return self._hints

  #-----------------------------------------------------------------------------
  @hints.setter
  def hints( self, hints ):
    cls = type(self)

    if isinstance(hints, str) or not isinstance(hints, (Sequence, Mapping)):
      hints = [hints]

    if isinstance(hints, Mapping):
      hints = ModelHint.cast(
        hints,
        level = self.level ).hints

    else:
      hints = [
        ( hint
          if isinstance(hint, cls) and not isinstance(hint, BaseException)
          else ModelHint.cast(
            hint,
            level = self.level ) )
        for hint in hints
        if hint is not None ]

    self._hints = hints

  #-----------------------------------------------------------------------------
  @property
  def max_level_num( self ):
    """Computes the maximum level of all sub-hints
    """
    return max([ self._level_num, *[h.max_level_num for h in self.hints ]])

  #-----------------------------------------------------------------------------
  def model_hint(self):
    return self

  #-----------------------------------------------------------------------------
  def __rich__( self ):
    try:
      return self.fmt( with_rich = True )
    except Exception:
      # import traceback
      # print(traceback.format_exc())
      # this is a last restort, should only happend during a serious error
      return f"{type(self)} id({id(self)})"

  #-----------------------------------------------------------------------------
  def __str__( self ):
    try:
      return str(self.fmt())
    except Exception:
      # import traceback
      # print(traceback.format_exc())
      # this is a last restort, should only happend during a serious error
      return f"{type(self)} id({id(self)})"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  @staticmethod
  def filter( hint, level, max_level = None ):
    """Filter hint and all sub-hints to the given level or higher

    Parameters
    ----------
    level : str | int
    max_level : None | str | int

    Returns
    -------
    hints : List[ hint ]
      List of hints filtered to the given level. If the root hint is above the `level`,
      it will be the only hint in the list. If it below `level`, but contains sub-hints
      >= `level` then the list will contain a collapse of all hints from the first
      recursive depth they occured. If all are < `level`, then an empy list is returned.
    """

    if isinstance( level, str ):
      level_num = hint_level_num( level )
    else:
      level_num = int( level )

    if max_level is None:
      max_level_num = logging.CRITICAL + 1000

    elif isinstance( max_level, str ):
      max_level_num = hint_level_num( max_level )
    else:
      max_level_num = int( max_level )

    fltr_hints = list()

    for h in hint.hints:
      fltr_hints.extend( ModelHint.filter(
        hint = h,
        level = level_num,
        max_level = max_level_num ) )

    if hint.level_num >= level_num and hint.level_num <= max_level_num:

      return [ type(hint)(
        msg = hint.msg,
        data = hint.data,
        format = hint.format,
        relation = hint.relation,
        loc = hint.loc,
        level = hint.level,
        hints = fltr_hints ), ]

    return fltr_hints

  #-----------------------------------------------------------------------------
  def fmt( self,
    level = 0,
    depth = 0,
    initdepth = None,
    maxdepth = None,
    with_loc = True,
    with_rich = False,
    with_unicode = True,
    checked = None ):
    """Format hint to a string
    """

    if checked is None:
      checked = list()

    elif self in checked:
      return [Text.from_markup(f"[debug]\[circular reference '{self.msg}'\][/]")]

    checked.append(self)

    if maxdepth is not None and maxdepth <= depth:
      return f"max depth reached: {maxdepth}"

    if initdepth is None:
      initdepth = depth

    if isinstance( level, str ):
      level_num = hint_level_num( level )
    else:
      level_num = int( level )

    if with_unicode:
      tree_char = TREE_CHAR_U
    else:
      tree_char = TREE_CHAR_A

    # aaply 'level' style to tree elements
    style = self.level.lower()
    tree_char = { k: Text(v, style = style) for k,v in tree_char.items() }

    next_depth = depth + 1

    lines = list()
    hints = self.hints

    if level_num > 0 and depth == initdepth:
      # filter out all child hints at first level
      hints = [
        _h
        for h in hints
        for _h in ModelHint.filter( hint = h, level = level_num ) ]

    msg_data_joinable = len(self.msg) < 30 and '\n' not in self.msg

    if self.msg:
      msg, sep, _data = self.msg.partition(str(tree_char[self.relation]))
      msg_data_joinable = msg_data_joinable and not bool(_data)

      msg = Text(msg)

      if repr_rec.fullmatch(msg.plain):
        # apply highlighting to message
        # only if the entire message matches a 'well-known' representation
        msg = rich_repr_highlight(msg)

      else:
        # add the default style based on the 'level'
        # NOTE: must insert as span instead of 'style' so it doesn't propagate
        # when joined with other strings
        msg.spans.insert(0, Span(0, len(msg), style))

      if _data:
        # only apply extra highlighting to text after the first colon
        msg += Text(sep) + rich_repr_highlight(Text(_data))

      lines.extend(split_lines(msg))

    if with_loc and self.loc:
      loc = tree_char['loc'] + self.loc.fmt( with_rich = True )

      lines.extend(wrap_lines(loc, 100))

    if self.data:

      if self.format == 'markup':
        data = Text.from_markup(self.data)

      else:
        data = Text(self.data)

        if self.format == 'auto':
          # applying highligting only if there are no styles
          data = rich_repr_highlight(data)

        elif self.format == 'literal':
          data = rich_literal_highlight(data)
          data.spans.insert(0, Span(0, len(data), 'literal'))

        else:
          # add the default style
          data.spans.insert(0, Span(0, len(data), self.format))

      _lines = wrap_lines(data, 100)

      if msg_data_joinable and len(_lines) == 1 and len(_lines[0]) <= 100:
        # add data to the same line as message, if it will fit
        if self.msg:
          lines[0] += tree_char[self.relation] + _lines[0]
        else:
          lines.insert(0, _lines[0])

      else:
        lines.extend( _lines )

    if len(hints) > 0:
      # NOTE: if there are more sub-hints, the current hint needs to be marked
      # with the 'more' symbol (not handled by the parent), and add 'skip'
      # past any loc/data of this hint to get to the sub-hint branches

      if len(lines) == 0:
        # NOTE: if no lines were added above (e.g. no msg, loc, or data), then
        # the branching will be missing a node.
        # Insert a blank line to properly mark the branch
        lines.append(Text())

      lines = indent_lines(
        n = 2,
        lines = lines,
        mark = tree_char['more'],
        ind = tree_char['skip'] )

    for i, hint in enumerate(hints):
      is_last = i == (len(hints) - 1)

      mark = 'end' if is_last else 'branch'

      if len(hint.hints) > 0:
        # NOTE: different marker used to connect to the 'more' symbol added by
        # the sub-hint when it has sub-sub-hints
        mark += '_more'

      line = hint.fmt(
        depth = next_depth,
        initdepth = initdepth,
        maxdepth = maxdepth,
        with_loc = with_loc,
        with_rich = True,
        checked = checked )

      line = indent_lines(
        n = 2,
        lines = line,
        mark = tree_char[mark],
        ind = '' if is_last else tree_char['skip'] )

      if isinstance( line, (str, Text) ):
        if line:
          lines.append( line )
      else:
        lines.extend( line )

    if depth == initdepth:
      lines = Text("\n").join( lines )

      if not with_rich:
        lines = str(lines)

      return lines
    else:
      return lines

  #-----------------------------------------------------------------------------
  @classmethod
  def cast( cls,
    obj,
    width = None,
    height = None,
    with_stack = True,
    level = None ):
    """Converts an object into an application model hint

    Will call 'model_hint' on the object if present. If not, it will use 'hinters'
    registered via 'ModelHint.register'.
    If no specific method is found, general fallbacks are used.
    Exceptions are inspected, tracebacks extracted and sanitized.

    Parameters
    ----------
    obj : object
      Object to convert into a hint
    width : None | int
      Maximum length of automatically formatted strings
    height : None | int
      Maximum height of automatically formatted strings
    with_stack : bool
      Include stack-trace of exceptions
    level : None | str | int
      If given, the level to cast top-level hint.

    Returns
    -------
    ModelHint
    """

    # NOTE: This must always check that the obj is not also an instance of
    # an exception, like ModelError, so that the stack information can be
    # sanitized

    level_num = None

    if level is not None:
      if isinstance( level, str ):
        level_num = hint_level_num( level )
      else:
        level_num = int( level )

    if isinstance( obj, ModelError ) or isinstance( obj, ModelHint ):
      if level_num is None:
        level_num = obj.level_num

    hint = None

    if hasattr(obj, 'model_hint'):
      try:
        hint = obj.model_hint()
      except Exception:
        log.exception(
          f"Call to model_hint failed: {fmt_obj(obj)}",
          exc_info = True)

    if hint is None:
      for bases, hinter in cls.registry[::-1]:
        try:
          if isinstance(obj, bases):
            _hint = hinter(obj)

            if _hint is NotImplemented:
              continue

            if not isinstance(_hint, ModelHint):
              log.error(
                f"Hinter did not return ModelHint: {hinter}"
                f" -> {type(_hint).__name__}")
              continue

            hint = _hint

        except Exception:
          # traceback.print_exc()
          log.exception(
            f"Failed to cast object to hint: {obj}",
            exc_info = True )

    if hint is None:
      hint = ModelHint(
        data = fmt_obj(obj),
        level = level_num )

    if with_stack and isinstance(obj, BaseException):
      hint = prepend_traceback(obj, hint)

    return hint

  #-----------------------------------------------------------------------------
  @classmethod
  def register(cls, bases, hinter = NotSet):
    """Register method for casting objects to a ModelHint

    Parameters
    ----------
    bases: type|tuple[type]
      Type(s) for which the hinter will be considered.
    hinter: Callable[[object], ModelHint|NotImplemented], optional
      A method that will be called with an instance of `bases`.
      It may return NotImplemented to defer to another method.

    """
    if hinter is NotSet:
      return lambda _hinter: cls.register(bases, hinter = _hinter)

    if not isinstance(bases, Sequence):
      bases = (bases,)
    else:
      bases = tuple(bases)

    if not (bases and all(isinstance(b, type) for b in bases)):
      raise TypeError(f"bases must be tuple of types: {fmt_obj(bases)}")

    if not callable(hinter):
      raise TypeError(f"hinter must be callable: {fmt_obj(hinter)}")

    cls.registry.append((bases, hinter))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ModelError( ModelHint, Exception ):
  """General Model Error

  Parameters
  ----------
  msg : str
    A message for the hint.
    The call will not happen until the message is required.
  loc : None | str
    Information on the location to which the hint corresponds.
  level : None | str
    Level of the model hint.
    Must be a value in :py:data:`HINT_LEVELS <partis.utils.HINT_LEVELS>`.
    default: 'info'.
  ignore_frame : None | bool
    Indicates that the stack frame from which the error was raised may be ignored
    without losing relevent information, such as a re-raise in the '__exit__' of
    a context manager.

  **kwargs :
    See ModelHint
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    msg,
    loc = None,
    level = None,
    ignore_frame = None,
    *args, **kwargs ):

    if level is None:
      level = 'error'

    ModelHint.__init__( self,
      msg = msg,
      loc = loc,
      level = level,
      *args, **kwargs )

    self.ignore_frame = bool(ignore_frame)

    Exception.__init__( self, self.msg )

  #-----------------------------------------------------------------------------
  def model_hint(self):
    # NOTE: should not return self to avoid all the data attached to exceptions
    return ModelHint(
      msg = self.msg,
      data = self.data,
      format = self.format,
      relation = self.relation,
      loc = self.loc,
      level = self.level,
      hints = self.hints )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Loc:
  """Location information of source data from a parsed document

  Parameters
  ----------
  filename : str | None
    Filename/path of source document
  line : int | None
    Line number of source data in the document
  col : int | None
    Column number of source data in the document
  path : list[str] | None
    Path of source data within a structured document
  owner : str | None
    Representation of a class or object that is issuing this location.
  time : float | None
    Unix timestamp associated with this location.
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    filename = None,
    line = None,
    col = None,
    path = None,
    owner = None,
    time = None ):

    self.filename = filename
    self.line = line
    self.col = col
    self.path = path
    self.owner = owner
    self.time = time

  #-----------------------------------------------------------------------------
  @property
  def filename(self):
    return self._p_filename

  #-----------------------------------------------------------------------------
  @filename.setter
  def filename(self, val):

    if val is not None:
      val = os.fspath(val)

    self._p_filename = val

  #-----------------------------------------------------------------------------
  @property
  def line(self):
    return self._p_line

  #-----------------------------------------------------------------------------
  @line.setter
  def line(self, val):

    if val is not None:
      val = int(val)

    self._p_line = val

  #-----------------------------------------------------------------------------
  @property
  def col(self):
    return self._p_col

  #-----------------------------------------------------------------------------
  @col.setter
  def col(self, val):

    if val is not None:
      val = int(val)

    self._p_col = val

  #-----------------------------------------------------------------------------
  @property
  def path(self):
    return self._p_path

  #-----------------------------------------------------------------------------
  @path.setter
  def path(self, val):

    if val is None:
      val = []

    if not (
      isinstance( val, list )
      and all( isinstance( s, str ) or isinstance( s, int ) for s in val ) ):

      raise ValueError(
        f"`path` must be a list of strings or ints: {val}")

    self._p_path = val

  #-----------------------------------------------------------------------------
  @property
  def owner(self):
    return self._p_owner

  #-----------------------------------------------------------------------------
  @owner.setter
  def owner(self, val):

    if val is not None:
      val = str(val)

    self._p_owner = val

  #-----------------------------------------------------------------------------
  @property
  def time(self):
    return self._p_time

  #-----------------------------------------------------------------------------
  @time.setter
  def time(self, val):

    if val is not None:
      val = float(val)

    self._p_time = val

  #-----------------------------------------------------------------------------
  @classmethod
  def from_dict(cls, d):
    if isinstance(d, Mapping):
      d = {
        k:v
        for k,v in d.items()
        if k in inspect.getfullargspec(cls.__init__)[0][1:] }

      return Loc(**d)

    return Loc(d)

  #-----------------------------------------------------------------------------
  def to_dict(self):
    loc = dict()

    for k in inspect.getfullargspec(self.__init__)[0][1:]:

      v = getattr(self, k)

      if v is not None and v != []:
        loc[k] = v

    return loc

  #-----------------------------------------------------------------------------
  def replace(self, **kwargs):
    return Loc(**{**self.to_dict(), **kwargs})

  #-----------------------------------------------------------------------------
  def __bool__(self):
    return (
      bool(self.filename)
      or bool(self.line)
      or bool(self.col)
      or bool(self.owner)
      or bool(self.path) )

  #-----------------------------------------------------------------------------
  def fmt( self,
    with_rich = False ):

    parts = list()

    if self.time:
      parts.append(rich_time(self.time))

    if self.owner:
      parts.extend([
        Text("by"),
        Text(self.owner, 'inspect.class' )])

    if self.path:
      parts.extend([
        Text("at"),
        Text(join_attr_path(self.path), 'repr.attrib_name' )])

    if self.filename:
      path, base = osp.split(self.filename)

      if path:
        filename = Text(os.path.sep).join([
          Text(path, 'repr.path'),
          Text(base, 'repr.filename') ])
      else:
        filename = Text(base, 'repr.filename')

      parts.extend([
        Text("in"),
        Text('"') + filename + Text('"') ])

    if self.line is not None:
      parts.extend([
        Text("line"),
        Text(str(self.line), 'repr.number' )])

    if self.col is not None:
      parts.extend([
        Text("col"),
        Text(str(self.col), 'repr.number' )])

    msg = Text(" ").join(parts)
    msg.spans.insert(0, Span(0, len(msg), 'qualifier'))

    if not with_rich:
      msg = str(msg)

    return msg

  #-----------------------------------------------------------------------------
  def __rich__( self ):
    return self.fmt( with_rich = True )

  #-----------------------------------------------------------------------------
  def __str__( self ):

    return str(self.fmt())

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  def __call__( self,
    obj = None,
    key = None ):
    """Creates a new location in the same document

    Parameters
    ----------
    obj : CommentedBase | object | None
      Source data object.
    key : int | str | None
      Key/index for a mapping or sequence source data

    Returns
    -------
    loc : :class:`Loc <partis.schema_meta.base.Loc>`
    """

    path = list(self.path)

    if key is not None:
      path.append( key )

    line = self.line
    col = self.col

    if isinstance( obj, CommentedBase ):
      # NOTE: ruamel appears to store line/col in zero-based indexing
      if (
        key is None
        or not ( isinstance(obj, CommentedMap) or isinstance(obj, CommentedSeq) )
        or obj.lc.data is None
        or (isinstance(obj, CommentedMap) and key not in obj)
        or (isinstance(obj, CommentedSeq) and ( key < 0 or key >= len(obj) ) ) ):

        line = obj.lc.line + 1
        col = obj.lc.col + 1

      else:
        line = obj.lc.data[key][0] + 1
        col = obj.lc.data[key][1] + 1

    return self.replace(
      line = line,
      col = col,
      path = path )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_frame_source_line(frame, lineno):
  """Get filename and source-line from a frame object, also handles Cython modules
  if the associated *.pyx files are installed along side the compiled extension.
  """

  filename = frame.f_code.co_filename
  try:
    filename = Path(filename)
  except (TypeError, ValueError):
    pass
  else:
    if not (filename.exists() or filename.is_absolute()):
      module_file = frame.f_globals.get('__file__', None)
      if module_file:
        src_file = Path(module_file).parent / filename
        if src_file.exists():
          filename = src_file

    # cast Path back to string so its always the same type after this point
    filename = str(filename)

  module_name = (
    frame.f_locals.get('__module__', '')
    or frame.f_globals.get('__name__', ''))

  module = None

  if module_name:
    try:
      module = importlib.import_module(module_name)
    except ImportError:
      pass

  module_vars = vars(module) if module else None

  return filename, linecache.getline(filename, lineno, module_vars).strip()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def prepend_traceback(obj, hint):
  tb = getattr(obj, '__traceback__')

  # chained_hints = list()
  # cause = None
  # context = None
  # if hasattr(obj, '__cause__') and obj.__cause__ is not None:
  #   cause = obj.__cause__
  #   chained_hints.append( ModelHint(
  #     f"Direct Cause",
  #     level = 'debug',
  #     hints = [obj.__cause__] ))
  #
  # if hasattr(obj, '__context__') and obj.__context__ is not cause:
  #   context = obj.__context__
  #   chained_hints.append( ModelHint(
  #     f"Unhandled",
  #     level = 'debug',
  #     hints = [obj.__context__] ))

  if tb is not None:
    # extract traceback information, if available
    for frame, lineno in list(traceback.walk_tb(tb))[::-1]:
      code = frame.f_code
      local_hints = list()
      sub_hints = list()

      if code.co_name != '<module>' and isinstance( frame.f_locals, dict ):
        # add local variable values, if not module level code
        for k, v in frame.f_locals.items():
          if v is not obj:
            local_hints.append(ModelHint(
              msg = k,
              data = fmt_obj(v, width = 100, height = 1 ),
              format = 'literal',
              level = 'trace' ))

      if len(local_hints) > 0:
        sub_hints.append(ModelHint(
          "With local variables",
          level = 'trace',
          hints = local_hints))

      sub_hints.append(hint)

      filename, line_src = get_frame_source_line(frame, lineno)
      if line_src.startswith('raise '):
        line_src = ''

      hint = ModelHint(
        f"During: `{code.co_name}`",
        data = f'`{line_src}`' if line_src else None,
        format = 'block',
        loc = Loc(
          filename = filename,
          line = lineno),
        level = 'debug',
        hints = sub_hints)

  return hint

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@ModelHint.register(BaseException)
def exception_hinter(obj):
  return ModelHint(
    msg = type(obj).__name__,
    data = fmt_obj(obj, width = 100, height = 1 ),
    format = 'literal',
    level = 'error')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@ModelHint.register((Mapping, Sequence))
def sequence_mapping_hinter(obj):
  if isinstance(obj, (str, bytes)):
    return NotImplemented

  hints = list()

  if isinstance(obj, Mapping):
    viter = obj.items()
  else:
    viter = enumerate(obj)

  for k,v in viter:
    _data = None
    _hints = None

    if isinstance(v, (Mapping, Sequence)) and not isinstance(v, (str, bytes)):
      _hints = [v]
    else:
      _data = v

    hints.append(ModelHint(
      msg = k,
      data = _data,
      hints = _hints ))

  return ModelHint(
    data = f"<{type(obj).__name__}>",
    hints = hints )
