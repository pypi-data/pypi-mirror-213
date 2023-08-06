import sys

from .fmt import (
  indent_lines,
  line_segment )

from .hint import (
  Loc,
  ModelHint )

from pyflakes import (
  checker )

Checker = checker.Checker

if sys.version_info >= (3, 8):
  import ast

else:
  from typed_ast import ast3 as ast
  checker.ast = ast
  checker.FOR_TYPES = tuple([getattr(ast, k.__name__) for k in checker.FOR_TYPES])

  Checker._ast_node_scope = {
    getattr(ast, k.__name__) : v
    for k,v in Checker._ast_node_scope.items() }

from pyflakes.messages import (
  Message,
  UndefinedName,
  UnusedImport,
  UnusedVariable )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def check_attrs( obj, name ):
  attrs = name.split('.')

  _obj = obj

  for i, attr in enumerate(attrs):
    try:
      _obj = getattr( _obj, attr )

    except AttributeError as e:
      return '.'.join(attrs[:i]), '.'.join(attrs[i:])

  return name, ''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lint_python(
  src,
  locals,
  mode,
  loc = None,
  restricted = False ):

  if loc is None:
    loc = Loc()

  hints = list()

  src_lines = src.splitlines()

  assert mode in ['func', 'expr', 'exec']

  if mode == 'func':
    fsrc = "def func():\n  __noop__ = 0\n{}".format(indent_lines(2, src))
    ix = 2
    iy = 2

  elif mode == 'expr':
    _r = '__result__ = '
    fsrc = _r + src
    ix = len(_r)
    iy = 0

  else:
    fsrc = src
    ix = 0
    iy = 0

  filename = ''

  try:

    tree = ast.parse(fsrc, filename = filename)

  except SyntaxError as e:

    lineno = e.lineno - iy
    col = e.offset - ix

    idx = lineno - 1
    offset = col - 1

    _loc = Loc(
      filename = 'compiled source',
      line = lineno,
      col = col )

    line = src_lines[idx]

    hints.append( ModelHint(
      e.msg,
      loc = _loc,
      level = 'error',
      data = '\n'.join([
        line,
        ' '*offset + '^' + ' '*(len(line) - offset - 1 ) ]),
      format = 'block' ) )

  else:

    file_tokens = checker.make_tokens(fsrc)

    if restricted:
      w = RestrictedChecker(tree, file_tokens=file_tokens, filename=filename)

    else:
      w = Checker(tree, file_tokens=file_tokens, filename=filename)

    w.messages.sort(key=lambda m: m.lineno)

    for m in w.messages:
      if m.lineno - iy <= 0:
        # likely disliked '__noop__' in wrapping code being un-used
        continue

      message = m.message
      message_args = m.message_args

      lineno = m.lineno - iy
      col = m.col - ix

      idx = lineno - 1
      offset = col

      line = src_lines[idx]

      if type(m) in [ UnusedImport, UnusedVariable ]:
        level = 'warning'
      else:
        level = 'error'

      if isinstance( m, UndefinedName ) and locals:

        name = m.message_args[0]

        _, _name = line_segment(
          text = line,
          sep = r"[^a-zA-Z0-9_\.]",
          offset = offset )

        contains, missing = check_attrs( locals, _name )

        if not missing:
          continue

        if contains:
          offset += len(contains)
          level = 'warning'
          message = "Unknown attribute '%s' of name '%s'"
          message_args = (missing, contains)

      msg = message % message_args

      _loc = Loc(
        filename = 'compiled source',
        line = lineno,
        col = offset + 1 )

      hints.append( ModelHint(
        msg,
        loc = _loc,
        level = level,
        data = '\n'.join([
          line,
          ' '*offset + '^' + ' '*(len(line) - offset - 1 ) ]),
        format = 'block' ) )

  if len(hints) > 0:
    max_num = max([hint.level_num for hint in hints])

    hints = [
      ModelHint(
        loc = loc,
        level = max_num,
        hints = hints ) ]

  return hints


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Restricted(Message):
  message = 'Use of %r not allowed in restricted evaluation'

  def __init__(self, filename, loc, name):
      Message.__init__(self, filename, loc)
      self.message_args = (name,)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RestrictedChecker( Checker ):

  restricted_nodes = [
    # 'Add', 'And',
    # 'AssAttr', 'AssList', 'AssName', 'AssTuple',
    # 'Assert', 'Assign', 'AugAssign',
    'Backquote',
    # 'Bitand', 'Bitor', 'Bitxor', 'Break',
    # 'CallFunc', 'Class', 'Compare', 'Const', 'Continue',
    # 'Decorators', 'Dict', 'Discard', 'Div',
    # 'Ellipsis', 'EmptyNode',
    'Exec',
    # 'Expression', 'FloorDiv',
    # 'For',
    'From',
    # 'Function',
    # 'GenExpr', 'GenExprFor', 'GenExprIf', 'GenExprInner',
    # 'Getattr', 'Global', 'If',
    'Import',
    # 'Invert',
    # 'Keyword', 'Lambda', 'LeftShift',
    # 'List', 'ListComp', 'ListCompFor', 'ListCompIf', 'Mod',
    # 'Module',
    # 'Mul', 'Name', 'Node', 'Not', 'Or', 'Pass', 'Power',
    # 'Print', 'Printnl',
    'Raise',
    #  'Return', 'RightShift', 'Slice', 'Sliceobj',
    # 'Stmt', 'Sub', 'Subscript',
    'TryExcept', 'TryFinally',
    # 'Tuple', 'UnaryAdd', 'UnarySub',
    # 'While','Yield'
    ]

  restricted_builtins = [
    '__import__',
    # 'abs', 'apply', 'basestring', 'bool', 'buffer',
    # 'callable', 'chr', 'classmethod', 'cmp', 'coerce',
    'compile',
    # 'complex',
    'delattr',
    # 'dict',
    'dir',
    # 'divmod', 'enumerate',
    'eval', 'execfile', 'file',
    # 'filter', 'float', 'frozenset',
    'getattr', 'globals', 'hasattr',
    #  'hash', 'hex', 'id',
    'input',
    # 'int', 'intern', 'isinstance', 'issubclass', 'iter',
    # 'len', 'list',
    'locals',
    # 'long', 'map', 'max', 'min', 'object', 'oct',
    'open',
    # 'ord', 'pow', 'property', 'range',
    'raw_input',
    # 'reduce',
    'reload',
    # 'repr', 'reversed', 'round', 'set',
    'setattr',
    # 'slice', 'sorted', 'staticmethod',  'str', 'sum', 'super',
    # 'tuple', 'type', 'unichr', 'unicode',
    'vars',
    #  'xrange', 'zip'
    ]


  #-----------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):

    self.builtIns = set([
      name
      for name in self.builtIns
      if name not in self.restricted_builtins ])

    super().__init__(*args, **kwargs)


  #-----------------------------------------------------------------------------
  def getNodeHandler(self, node_class):
    if node_class.__name__ in self.restricted_nodes:
      return self._restricted_handler

    return super().getNodeHandler(node_class)

  #-----------------------------------------------------------------------------
  def _restricted_handler(self, node):

    self.report(
      Restricted,
      node,
      type(node).__name__ )

    self.handleChildren(node)
