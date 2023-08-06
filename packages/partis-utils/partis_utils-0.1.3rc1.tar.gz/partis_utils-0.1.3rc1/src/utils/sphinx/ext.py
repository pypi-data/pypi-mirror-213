from __future__ import annotations
from typing import (
  Optional,
  Union,
  Literal,
  TypeVar)
from collections.abc import (
  Iterable,
  Sequence )
import inspect
import traceback
import re
import json
from copy import copy

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.locale import _, __
from sphinx.domains.python import (
  PythonDomain,
  PyXrefMixin,
  PyObject,
  PyAttribute,
  PyProperty,
  _parse_annotation)
from sphinx.util.inspect import safe_getattr
from sphinx.builders.html import StandaloneHTMLBuilder

from sphinx_autodoc_typehints import (
  get_annotation_module,
  get_annotation_class_name,
  get_annotation_args,
  format_annotation,
  _inject_rtype,
  process_docstring as _process_docstring )


from .. import fmt_obj
from ..typing import NewType

from sphinx.util import logging
log = logging.getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# returns_rec = re.compile(r"^(?P<bullet>( {8,9}|:returns?:) (\* )?)\*\*?(?P<name>\w+)\*\*? *(?P<type>.*(?=--))?(?P<doc>--.*)?")
returns_rec = re.compile(r"^(?P<bullet>( {8,9}|:returns?:) (\* )?)(\*\*?(?P<name>\w+)\*\*? *)?(?P<type>.*(?=--))?(?P<doc>(--)?.*)?")

param_rec = re.compile(r"^:param (?P<qual>(\w+\.)*)(?P<name>\w+):")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PartisAttribute( PyObject ):
  option_spec = PyObject.option_spec.copy()
  option_spec.update({
    'type': directives.unchanged,
    'value': directives.unchanged,
    'prefix': directives.unchanged,
    'subscript': directives.unchanged })

  #-----------------------------------------------------------------------------
  def get_signature_prefix(self, sig):
    prefix = []

    text = self.options.get('prefix')

    if text:
      parts = [ p.strip() for p in text.split(' ') ]

      for p in parts:
        prefix.append(nodes.Text(p))
        prefix.append(addnodes.desc_sig_space())

    return prefix

  #-----------------------------------------------------------------------------
  def handle_signature(self, sig, signode):
      fullname, prefix = super().handle_signature(sig, signode)

      typ = self.options.get('type')
      subscript = self.options.get('subscript')

      if typ:
        annotations = _parse_annotation(typ, self.env)

        if subscript:
          annotations += [
            addnodes.desc_sig_punctuation('', '['),
            nodes.Text(subscript),
            addnodes.desc_sig_punctuation('', ']') ]


        signode += addnodes.desc_annotation(
          typ, '',
          addnodes.desc_sig_punctuation('', ':'),
          addnodes.desc_sig_space(),
          *annotations)

      value = self.options.get('value')
      if value:
        signode += addnodes.desc_annotation(
          value, '',
          addnodes.desc_sig_space(),
          addnodes.desc_sig_punctuation('', '='),
          addnodes.desc_sig_space(),
          nodes.Text(value))

      return fullname, prefix

  #-----------------------------------------------------------------------------
  def get_index_text(self, modname, name_cls):
    name, cls = name_cls
    try:
      clsname, attrname = name.rsplit('.', 1)
      if modname and self.env.config.add_module_names:
        clsname = '.'.join([modname, clsname])
    except ValueError:
      if modname:
        return _('%s (in module %s)') % (name, modname)
      else:
        return name

    return _('%s (%s attribute)') % (attrname, clsname)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_literal(v):
  return str(v).startswith('typing.Literal[')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_union(v):
  return str(v).startswith('typing.Union[')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_tuple_type(v):
  return str(v).startswith(('typing.Tuple[', 'tuple['))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def typehints_formatter(annotation, config, depth = 0):

  try:
    module = get_annotation_module(annotation)
    class_name = get_annotation_class_name(annotation, module)
    full_name = f"{module}.{class_name}" if module != "builtins" else class_name
    args = get_annotation_args(annotation, module, class_name)

  except ValueError:
    # log.warn(f"Failed to get typename: {annotation}", exc_info = True)
    class_name = str(annotation).strip("'")
    full_name = class_name
    args = []

  try:

    # print('  '*depth + f"typehints_formatter({annotation}) -> {full_name}, {args}")
    result = None

    if annotation is None or annotation is type(None):
      result = ":py:obj:`None`"

    elif annotation is Ellipsis:
      # This avoids creating links to the Ellipses doc page, too cluttered
      result = "..."

    elif isinstance(annotation, (int, float, str)):
      result = fmt_obj(annotation)

    elif isinstance(annotation, (tuple, Sequence)):
      result = ', '.join([typehints_formatter(v, config, depth+1) for v in annotation])

      if len(annotation) == 1:
        result = f"({result},)"
      else:
        result = f"({result})"

    elif isinstance(annotation, NewType):
      result = f":class:`~{full_name}`"

      if depth == 0:
        try:
          arg = rf" ⊆ {typehints_formatter(annotation.__supertype__, config, depth+1)}"
          result += arg
        except Exception as e:
          log.warn(f"Failed to format annotation: {annotation}", exc_info = True)

    elif is_literal(annotation):
      result = ' | '.join([fmt_obj(v) for v in args])

    elif full_name in ('typing.Union', 'types.UnionType', 'typing.Optional'):
      optional = full_name == "typing.Optional"

      # by convention, always put None as first
      args = sorted(
        args,
        key = lambda o: not (o is None or o is type(None)))

      if args[0] is None or args[0] is type(None):
        optional = True
        args = args[1:]

      _depth = depth if len(args) == 1 else depth + 1

      result = ' | '.join([typehints_formatter(v, config, _depth) for v in args])

      if optional:
        result = f"{result}, optional"

    else:
      result = f":class:`~{full_name}`"

      if args:
        _args = []
        for v in args:
          try:
            _args.append(typehints_formatter(v, config, depth+1))
          except Exception as e:
            log.warn(f"Failed to format annotation: {v}", exc_info = True)
            _args.append(str(v).strip("'"))

        _args = ', '.join(_args)


        result += rf"\[{_args}]"

  except:
    log.error(f"Failed to format: {annotation}", exc_info = True)
    raise

  # print('  '*depth + f"-> {result}")
  return result

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_signature(app, what, name, obj, options, signature, return_annotation):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def process_docstring(
  app: Sphinx,
  what: str,
  name: str,
  obj: Any,
  options: Options | None,
  lines: list[str] ) -> None:


  if hasattr(obj, '__get__') and hasattr(obj, 'fget'):
    # NOTE: This is a hack to get sphinx_autodoc_typehints to inject property return
    # typehints into the docstring.
    obj = obj.fget

    _process_docstring(app, what, name, obj, options, lines)
    return

  if isinstance(obj, NewType):
    if hasattr(obj, '__supertype__'):
      type_hints = obj.__supertype__

      try:
        formatted_annotation = typehints_formatter(type_hints, app.config)
        lines.insert(0, '')
        lines.insert(0, formatted_annotation)

      except Exception as e:
        log.warn(f"Failed to format annotation: {type_hints}", exc_info = True)

    return

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def inject_types(
  type_hints,
  signature,
  original_obj,
  app,
  what,
  name,
  lines):

  _lines = copy(lines)

  try:

    rtype = type_hints.pop('return', None)

    log.debug(f"[inject_type] types= {type_hints}")

    ntypes = len(type_hints)
    count = 0
    started = False
    ended = False
    end_idx = 0

    log.debug(f"[inject_type]{name:-^70}")

    for at, line in enumerate(_lines):
      ended = started and line and not line.startswith((":param", ":type", " "))

      if ended:
        end_idx = at
        # stop when all types are inserted, or on the first non-empty line
        # after params section
        log.debug(f"[inject_type]{'':7} -----BREAK-----")
        break

      started = started or line.startswith((":param", ":type"))

      m = '$' if started else '|'
      log.debug(f"[inject_type]{'':4}{at:>3}{m}{line}")

      if started:
        match = param_rec.match(line)

        if match:
          name = match['name']
          fullname = (match['qual'] or '') + name
          insert_idx = at + count

          if name in type_hints:
            count += 1

            formatted_annotation = typehints_formatter(type_hints[name], app.config)
            change = f":type {fullname}: {formatted_annotation}"

            lines.insert(insert_idx, change)
            log.debug(f"[inject_type]{'':2}>>{at:>3}>{change}")
            log.debug(f"[inject_type]{'':7} ^^^^INSERT {count} / {ntypes}^^^^")

          else:
            log.debug(f"[inject_type]{'':7} ^^^^NO TYPE-HINT^^^^")

    else:
      log.debug(f"[inject_type]{'':7} -----END-----")

    log.debug(f"[inject_type]{'':-^70}")

    log.debug(f"[inject_rtype] rtype= {rtype}")

    if not app.config.typehints_document_rtype:
      log.debug(f"[inject_rtype] typehints_document_rtype == False")
      return

    if rtype is None:
      return

    if inspect.isclass(original_obj) or inspect.isdatadescriptor(original_obj):
      log.debug(f"[inject_rtype] Object not applicable: {type(original_obj).__name__}")
      return

    # avoid adding a return type for data class __init__
    if what == "method" and name.endswith(".__init__"):
      log.debug(f"[inject_rtype] Object not applicable: method __init__()")
      return

    # 1. If there is an existing :rtype: anywhere, don't insert anything.
    if any(line.startswith(":rtype:") for line in lines):
      log.debug(f"[inject_rtype] :rtype: already present")
      return

    if is_tuple_type(rtype):
      # For multiple returns, attempt to zip together the "params-like" formatted
      # :returns: section
      rtypes = rtype.__args__

    elif isinstance(rtype, str) or not isinstance(rtype, Sequence):
      rtypes = [rtype]

    else:
      rtypes = rtype

    nrtypes = len(rtypes)
    count = 0
    started = False

    log.debug(f"[inject_rtype] nrtypes({nrtypes})= {rtypes}")
    log.debug(f"[inject_rtype]{name:-^70}")

    for at, line in enumerate(lines):
      if count == nrtypes or (started and line and line[0] != ' '):
        # stop when all returns are inserted, or on the first non-empty line
        # after returns section
        log.debug(f"[inject_rtype]{'':7} -----BREAK-----")
        break

      started = started or line.startswith((":return:", ":returns:"))
      m = '$' if started else '|'
      log.debug(f"[inject_rtype]{'':4}{at:>3}{m}{line}")

      if started:
        match = returns_rec.match(line)

        if match:
          count += 1

          if match['type']:
            log.debug(f"[inject_rtype]{'':7} ^^^^EXISTING RTYPE {match['type']}^^^^")
            continue

          if match['name']:
            name = f"**{match['name']}** "
          else:
            name = ''

          doc = match['doc'] or ''

          if doc and not doc.startswith('--'):
            doc = '-- ' + doc

          formatted_annotation = typehints_formatter(rtypes[count-1], app.config)
          change = f"{match['bullet']}{name}({formatted_annotation}) {doc}"
          lines[at] = change

          log.debug(f"[inject_rtype]{'':2}>>{at:>3}>{change}")
          log.debug(f"[inject_rtype]{'':7} ^^^^INSERT RTYPE {count} / {nrtypes}^^^^")
    else:
      log.debug(f"[inject_rtype]{'':7} -----END-----")

    log.debug(f"[inject_rtype]{'':-^70}")

    if count == 0:

      # don't allow mixing the two insertion methods,
      # but if nothing was counted then allow the default insertion
      formatted_annotation = typehints_formatter(rtype, app.config)
      change = f":rtype: {formatted_annotation}"

      lines.insert(end_idx, "")
      lines.insert(end_idx, change)
      lines.insert(end_idx, "")

      log.debug(f"[inject_rtype]{'':2}>>{end_idx:>3}|{lines[end_idx]}")
      log.debug(f"[inject_rtype]{'':2}>>{end_idx:>3}|{change}")
      log.debug(f"[inject_rtype]{'':7} ^^^^INSERT RTYPE^^^^")

  except Exception as e:
    log.warn(f"Failed to inject type(s) into docstring of {what} {name}", exc_info = True)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _builder_inited(app: sphinx.application.Sphinx) -> None:

  if app.builder.format == 'html':
    if app.config.mathjax3_config:
      # replace inlined js with the 'mathjax_config.js_t' template
      app.config.html_context['mathjax3_config_json'] = f'window.MathJax = {json.dumps(app.config.mathjax3_config)}'
      app.config.mathjax3_config = ''


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def setup(app):
  import partis.utils
  partis.utils.TYPING = True

  import sphinx_autodoc_typehints
  sphinx_autodoc_typehints._inject_types_to_docstring = inject_types

  app.add_directive('partis_attr', PartisAttribute)

  # app.connect("autodoc-process-signature", process_signature )
  app.connect("autodoc-process-docstring", process_docstring )

  app.connect("builder-inited", _builder_inited)
