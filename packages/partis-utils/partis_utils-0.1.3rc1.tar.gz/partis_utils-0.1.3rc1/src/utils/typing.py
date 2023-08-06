from __future__ import annotations
import types
import typing

import inspect
from collections import namedtuple
from collections.abc import Sequence, Mapping
import importlib
import sys
import re
import builtins
import typing_extensions

from typing import *
from typing_extensions import *

from .inspect import caller_module

from .hint import ModelHint, ModelError

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if sys.version_info >= (3, 10):
  # added in 3.10
  from types import UnionType
else:
  # can be referenced without further condition
  UnionType = Union

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if sys.version_info >= (3, 10):
  # added in 3.10
  from inspect import get_annotations as _get_annotations
else:
  from get_annotations import get_annotations as _get_annotations

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from . import ast
from .ast import (
  unparse,
  Load,
  Name,
  Subscript,
  Index,
  Tuple)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
try:
  # added 3.8
  from typing import Literal
except ImportError:
  class Literal:
    def __init__(self, *args):
      self.__args__ = args

    def __class_getitem__(cls, *args):
      return cls(*args)

    def __str__(self):
      args = [str(v) for v in self.__args__]
      return f"Literal[{', '.join(args)}]"

    def __repr__(self):
      return str(self)

LITERAL_TYPES = (int, float, str, list, tuple, dict)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TypeHint:
  """Container for information from a parsed type annotation

  Parameters
  ----------
  name:
    Name of un-wrapped/aliased type or class. e.g. `"list"` for the case of `list[int]`.
  args:
    Any arguments of a type alias. e.g. `(TypeHint(name='"int"',...),)` for the case of `list[int]`.
  module:
    A module associated with the un-wrapped type. e.g. `builtins` for the case of `list[int]`
  untyped:
    The original un-evaluated type-hint. e.g. `"list[int]"`
  typed:
    The evaluated un-wrapped type. e.g. `<class 'list'>`
  obj:
    The evaluated typehint object.
  error:
    If the type-hint could not be evaluated, this gives reason, error, and stack-trace.
    This is done instead of directly raising an exception for some use-cases where
    the program should be able to continue running without the type-hint.
  """
  def __init__(self,
    name: str = '',
    args: tuple[TypeHint|Any] = (),
    module: str = '',
    untyped: str = '',
    typed: Any = None,
    obj: Any = None,
    error: ModelHint|None = None ):

    self.name = str(name)
    self.args = args
    self.module = str(module)
    self.untyped = str(untyped)
    self.typed = typed
    self.obj = obj
    self.error = error

  #-----------------------------------------------------------------------------
  def dict(self):
    return {
      k:getattr(self, k)
      for k in ('name', 'args', 'module', 'untyped', 'typed', 'obj', 'error') }

  #-----------------------------------------------------------------------------
  def __str__(self):
    d = self.dict()
    err = d.pop('error')

    args = [
      f"{k}= {v}"
      for k,v in d.items()
      if v]

    if self.error is not None:
      args.append(f"error= {self.error.msg}")

    return f"{type(self).__name__}({', '.join(args)})"

  #-----------------------------------------------------------------------------
  def __repr__(self):
    return str(self)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
BUILTIN_MODULES = [
  'types',
  'typing',
  'typing_extensions']

BUILTINS = {}
DEFAULT_GLOBALS = {}

for module_name in BUILTIN_MODULES:
  module = importlib.import_module(module_name)
  for name in module.__all__:
    v = getattr(module, name)

    # handle module name for back-ported implementations
    _v = DEFAULT_GLOBALS.get(name, None)

    _module_name = module_name if _v is None else BUILTINS[_v][0]

    BUILTINS[v] = (_module_name, name)
    DEFAULT_GLOBALS[name] = v

  DEFAULT_GLOBALS.update({
    name: getattr(module, name) for name in module.__all__ })

# NOTE: this is to combine the various forms of 'Union' into a single type
for cls in [UnionType, Optional]:
  BUILTINS[cls] = ('typing', 'Union')

# override any of the types included above with the builtin equivalents
# E.G. Text -> str
BUILTINS.update({
  v: ('builtins', name)
  for name, v in vars(builtins).items()
  if isinstance(v, type)})

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GENERIC_ALIASES = {}


if sys.version_info < (3, 9):
  GENERIC_ALIASES.update({
    'dict': 'Dict',
    'list': 'List',
    'tuple': 'Tuple',
    'set': 'Set',
    'type': 'Type' })

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if not isinstance(NewType, type):
  # patch in newer Python NewType
  # changed in 3.10 from a function to a class

  def _idfunc(_, x):
      return x

  class NewType:
      """NewType creates simple unique types with almost zero
      runtime overhead. NewType(name, tp) is considered a subtype of tp
      by static type checkers. At runtime, NewType(name, tp) returns
      a dummy callable that simply returns its argument. Usage::
          UserId = NewType('UserId', int)
          def name_by_id(user_id: UserId) -> str:
              ...
          UserId('user')          # Fails type check
          name_by_id(42)          # Fails type check
          name_by_id(UserId(42))  # OK
          num = UserId(5) + 1     # type: int
      """

      __call__ = _idfunc

      def __init__(self, name, tp):
          self.__qualname__ = name
          if '.' in name:
              name = name.rpartition('.')[-1]
          self.__name__ = name
          self.__supertype__ = tp
          def_mod = caller_module().__name__
          if def_mod != 'typing':
              self.__module__ = def_mod

      def __mro_entries__(self, bases):
          # We defined __mro_entries__ to get a better error message
          # if a user attempts to subclass a NewType instance. bpo-46170
          superclass_name = self.__name__

          class Dummy:
              def __init_subclass__(cls):
                  subclass_name = cls.__name__
                  raise TypeError(
                      f"Cannot subclass an instance of NewType. Perhaps you were looking for: "
                      f"`{subclass_name} = NewType({subclass_name!r}, {superclass_name})`"
                  )

          return (Dummy,)

      def __repr__(self):
          return f'{self.__module__}.{self.__qualname__}'

      def __reduce__(self):
          return self.__qualname__

      def __or__(self, other):
          return Union[self, other]

      def __ror__(self, other):
          return Union[other, self]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GenericAlias = getattr(types, 'GenericAlias', None)

if GenericAlias is None:
  # types.GenericAlias added Python 3.9
  # from numpy/_typing/_generic_alias.py
  class GenericAlias:
    """A python-based backport of the `types.GenericAlias` class.

    E.g. for ``t = list[int]``, ``t.__origin__`` is ``list`` and
    ``t.__args__`` is ``(int,)``.

    See Also
    --------
    :pep:`585`
        The PEP responsible for introducing `types.GenericAlias`.

    """

    __slots__ = (
        "__weakref__",
        "_origin",
        "_args",
        "_parameters",
        "_hash",
        "_starred",
    )

    @property
    def __origin__(self) -> type:
        return super().__getattribute__("_origin")

    @property
    def __args__(self) -> tuple[object, ...]:
        return super().__getattribute__("_args")

    @property
    def __parameters__(self) -> tuple[TypeVar, ...]:
        """Type variables in the ``GenericAlias``."""
        return super().__getattribute__("_parameters")

    @property
    def __unpacked__(self) -> bool:
        return super().__getattribute__("_starred")

    @property
    def __typing_unpacked_tuple_args__(self) -> tuple[object, ...] | None:
        # NOTE: This should return `__args__` if `__origin__` is a tuple,
        # which should never be the case with how `_GenericAlias` is used
        # within numpy
        return None

    def __init__(
        self,
        origin: type,
        args: object | tuple[object, ...],
        starred: bool = False,
    ) -> None:
        self._origin = origin
        self._args = args if isinstance(args, tuple) else (args,)
        self._parameters = tuple(_parse_parameters(self.__args__))
        self._starred = starred

    @property
    def __call__(self) -> type[Any]:
        return self.__origin__

    def __reduce__(self: _T) -> tuple[
        type[_T],
        tuple[type[Any], tuple[object, ...], bool],
    ]:
        cls = type(self)
        return cls, (self.__origin__, self.__args__, self.__unpacked__)

    def __mro_entries__(self, bases: Iterable[object]) -> tuple[type[Any]]:
        return (self.__origin__,)

    def __dir__(self) -> list[str]:
        """Implement ``dir(self)``."""
        cls = type(self)
        dir_origin = set(dir(self.__origin__))
        return sorted(cls._ATTR_EXCEPTIONS | dir_origin)

    def __hash__(self) -> int:
        """Return ``hash(self)``."""
        # Attempt to use the cached hash
        try:
            return super().__getattribute__("_hash")
        except AttributeError:
            self._hash: int = (
                hash(self.__origin__) ^
                hash(self.__args__) ^
                hash(self.__unpacked__)
            )
            return super().__getattribute__("_hash")

    def __instancecheck__(self, obj: object) -> NoReturn:
        """Check if an `obj` is an instance."""
        raise TypeError("isinstance() argument 2 cannot be a "
                        "parameterized generic")

    def __subclasscheck__(self, cls: type) -> NoReturn:
        """Check if a `cls` is a subclass."""
        raise TypeError("issubclass() argument 2 cannot be a "
                        "parameterized generic")

    def __repr__(self) -> str:
        """Return ``repr(self)``."""
        args = ", ".join(_to_str(i) for i in self.__args__)
        origin = _to_str(self.__origin__)
        prefix = "*" if self.__unpacked__ else ""
        return f"{prefix}{origin}[{args}]"

    def __getitem__(self: _T, key: object | tuple[object, ...]) -> _T:
        """Return ``self[key]``."""
        key_tup = key if isinstance(key, tuple) else (key,)

        if len(self.__parameters__) == 0:
            raise TypeError(f"There are no type variables left in {self}")
        elif len(key_tup) > len(self.__parameters__):
            raise TypeError(f"Too many arguments for {self}")
        elif len(key_tup) < len(self.__parameters__):
            raise TypeError(f"Too few arguments for {self}")

        key_iter = iter(key_tup)
        return _reconstruct_alias(self, key_iter)

    def __eq__(self, value: object) -> bool:
        """Return ``self == value``."""
        if not isinstance(value, _GENERIC_ALIAS_TYPE):
            return NotImplemented
        return (
            self.__origin__ == value.__origin__ and
            self.__args__ == value.__args__ and
            self.__unpacked__ == getattr(
                value, "__unpacked__", self.__unpacked__
            )
        )

    def __iter__(self: _T) -> Generator[_T, None, None]:
        """Return ``iter(self)``."""
        cls = type(self)
        yield cls(self.__origin__, self.__args__, True)

    _ATTR_EXCEPTIONS: ClassVar[frozenset[str]] = frozenset({
        "__origin__",
        "__args__",
        "__parameters__",
        "__mro_entries__",
        "__reduce__",
        "__reduce_ex__",
        "__copy__",
        "__deepcopy__",
        "__unpacked__",
        "__typing_unpacked_tuple_args__",
        "__class__",
    })

    def __getattribute__(self, name: str) -> Any:
        """Return ``getattr(self, name)``."""
        # Pull the attribute from `__origin__` unless its
        # name is in `_ATTR_EXCEPTIONS`
        cls = type(self)
        if name in cls._ATTR_EXCEPTIONS:
            return super().__getattribute__(name)
        return getattr(self.__origin__, name)

# TODO:
# typing.Annotated: If your software uses annotated types, you might need to back-port typing.Annotated for Python versions <3.9.
# typing.ParamSpec: If you use PEP 612's typing.ParamSpec for higher-order functions with callbacks, consider back-porting it for Python versions <3.10.
# Python 3.10 introduces the typing.TypeAlias decorator to define type aliases. Ensure that your implementation correctly handles type aliases across different Python versions.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FixupBitOrUnion(ast.NodeTransformer):
  """UnionType (bit-wise or) not added until 3.10
  """
  def visit_BinOp(self, node):
    if not isinstance(node.op, ast.BitOr):
      return node

    args = []

    for v in [FixupBitOrUnion().visit(node.left), FixupBitOrUnion().visit(node.right)]:
      if isinstance(v, Subscript) and isinstance(v.value, Name) and v.value.id == 'Union':
        args.extend(v.slice.elts)
      else:
        args.append(v)

    return Subscript(
      value=Name(id='Union', ctx=Load()),
      slice=Tuple(
        elts=args,
        ctx=Load()),
      ctx=Load())

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FixupGenericAlias(ast.NodeTransformer):
  """Builtin types generic alias not added until 3.9
  """
  def visit_Subscript(self, node):
    if not isinstance(node.value, Name):
      return node

    alias = GENERIC_ALIASES.get(node.value.id, None)
    if alias is None:
      return node

    return Subscript(
      value = Name(id=alias, ctx=Load()),
      slice = FixupGenericAlias().visit(node.slice))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fixup_annotation(src: str) -> str:
  if sys.version_info >= (3, 10):
    return src

  tree = ast.parse(src, mode = 'eval')

  if sys.version_info < (3, 10):
    tree = FixupBitOrUnion().visit(tree)

  if GENERIC_ALIASES:
    tree = FixupGenericAlias().visit(tree)

  src = unparse(tree)

  return src

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def typehint_module(ant: Any) -> str|None:
  # print(f"typehint_module({ant})")

  if ant is None or ant is type(None):
    # print(f"  is_builtin (None)")
    return "builtins"

  try:
    if ant in BUILTINS:
      # print(f"  is_builtin")
      return BUILTINS[ant][0]
  except TypeError as e:
    # print(f"  lookup error: {e}")
    pass

  if (( sys.version_info < (3, 10)
        and inspect.isfunction(ant)
        and hasattr(ant, "__supertype__"))
      or isinstance(ant, NewType)
      or type(ant).__name__ == "ParamSpec" ):
    # print(f"  is_typing (NewType or ParamSpec)")
    return 'typing'

  for src, _ant in [
    ('instance', ant),
    ('__origin__', getattr(ant, "__origin__", None)),
    ('type', type(ant))]:

    # print(f"  name ({src}): {_ant}")

    if _ant is not None:
      for field in [
        '__module__']:

        name = getattr(_ant, field, None)

        if name and isinstance(name, str):
          # print(f"    -> field {field} -> {name}")
          break

        # print(f"    -> field {field} not found")

      else:
        continue

      break

  else:
    # Check if the type of `ant` is a built-in function or method
    if isinstance(ant, (types.BuiltinFunctionType, types.BuiltinMethodType)):
      # print("  is_builtin_function_or_method")
      return "builtins"

    # print(f"  parse from string")
    name = str(ant).partition('[')[0].rpartition('.')[0]


  if not name:
    # print(f"  no name!")
    # TODO: what to do with things that don't have a module?
    assert name

  return name

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def typehint_classname(ant: Any) -> Tuple[object, str]:
  # print(f"typehint_classname({ant})")

  if ant is None or ant is type(None):
    return ant, 'None'

  if (( sys.version_info < (3, 10)
        and inspect.isfunction(ant)
        and hasattr(ant, "__supertype__"))
      or isinstance(ant, NewType) ):

    return ant, 'NewType'

  for src, _ant in [
    ('__origin__', getattr(ant, "__origin__", None)),
    ('instance', ant),
    ('type', type(ant))]:

    # print(f"  name ({src}): {_ant}")

    if _ant is None:
      continue

    if _ant in BUILTINS:
      cls = _ant
      name = BUILTINS[_ant][1]
      # print(f"    -> builtin -> {name}")
      break

    for field in [
      '__qualname__',
      '_name',
      'name',
      '__name__']:

      name = getattr(_ant, field, None)

      if isinstance(name, str) and name:
        cls = _ant
        # print(f"    -> field {field} -> {name}")
        break
    else:
      continue

    break

  else:
    cls = ant
    name = repr(ant)

  name = name.partition('[')[0].rpartition('.')[2].lstrip("_")

  return cls, name

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def typehint_args(ant: Any) -> list:
  # TODO: look into typing_extensions.get_args

  for field in [
    '__parameters__',
    '__args__',
    '__values__',
    '__constraints__',
    '__supertype__',
    '__type__',
    'type_var']:

    args = getattr(ant, field, None)

    if isinstance(args, Sequence) and len(args) > 0:
      break

  else:
    args = ()

  if len(args) == 1 and isinstance(args[0], Sequence) and len(args[0]) == 0:
    # normalize ((), ) -> ()
    args = ()

  return tuple([typehint_normalize(v) for v in args])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_literal(value: Any) -> bool:
  if isinstance(value, (type, Callable)):
    return False

  if not isinstance(value, (str, bytes)) and isinstance(value, Sequence):
    return all(is_literal(v) for v in value)

  if isinstance(value, Mapping):
    return all(
      is_literal(k) and is_literal(v)
      for k, v in value.items() )

  return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def typehint_normalize(ant: Any, untyped: str = None) -> TypeHint|Any:
  """
  Parameters
  ----------
  ant:
    The evaluated but "un-parsed" annotation. e.g. `GenericAlias(list, (int,))`
  untyped:
    The un-evaluated typehint. e.g. `"list[int]"`
  """

  module = typehint_module(ant)
  cls, name = typehint_classname(ant)
  args = typehint_args(ant)

  # print(f"typehint_normalize(<{type(ant).__name__}> {ant})")
  # print(f"  module = {module}")
  # print(f"  cls    = {cls}")
  # print(f"  name   = {name}")
  # print(f"  args   = {args}")

  # if this is a literal value/argument and not a type, simply return the value
  # e.g. in NDarray[Shape[3,5], DType['float64']]
  # 3, 5, and 'float64' do not get converted to a TypeHint
  if module not in BUILTIN_MODULES+['builtins'] and is_literal(ant):
    # print(f"  is_literal")
    return ant

  untyped = untyped or name

  return TypeHint(
    name = name,
    args = args,
    module = module,
    untyped = untyped,
    typed = cls,
    obj = ant)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def eval_annotation(ant, globals = None, locals = None):
  if globals is None:
    globals = DEFAULT_GLOBALS
  else:
    globals = {**DEFAULT_GLOBALS, **globals}

  if not isinstance(ant, str):
    return ant

  ant = fixup_annotation(ant)

  ant = eval(ant, globals, locals)

  if isinstance(ant, LITERAL_TYPES):
    return Literal[ant]

  return ant

  # try:
  #   ant = eval(ant, globals, locals)

  #   if isinstance(ant, LITERAL_TYPES):
  #     return Literal[ant]

  #   return ant

  # except Exception as e1:
  #   print(repr(e))
  #   ants = ant.split('|')

  #   if len(ants) == 1:
  #     raise e1
  #   else:
  #     return Union[tuple([
  #       eval_annotation(v, globals = globals, locals = locals)
  #       for v in ants])]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def eval_annotations(ants, globals = None, locals = None):
  if not ants:
    return {}

  _ants = {}

  for k,v in ants.items():
    # print(f"eval '{k}': {v}")
    try:
      _ants[k] = typehint_normalize(eval_annotation(v, globals, locals), v)
    except Exception as e:
      _ants[k] = TypeHint(
        untyped = v,
        error = ModelHint.cast(e))

    # print(f"  -> {_ants[k]}")

  return _ants

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_annotations(obj, globals = None, locals = None):
  ants = _get_annotations(obj)
  return eval_annotations(ants, globals = globals, locals = locals)