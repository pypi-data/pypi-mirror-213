
import re

from .fmt import (
  fmt_obj,
  split_lines,
  indent_lines )

from .special import NOTSET

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _fmt_class_name( cls ):
  if cls.__module__ == 'builtins':
    return cls.__name__

  return f"~{cls.__module__}.{cls.__name__}"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_class_name( cls ):
  return f":class:`{cls.__name__} <{cls.__module__}.{cls.__name__}>`"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_attr_doc( *,
  name,
  typename,
  obj = NOTSET,
  val = NOTSET,
  prefix = NOTSET,
  doc = NOTSET,
  noindex = False ):
  """Formats an attribute docstring using the custom 'partis_attr' directive.

  This is used to include an optional `prefix` that appears before the attribute
  name, and to do more consistent formatting of the typename and value to allow
  sphinx to generate cross-references, and to handle 'large' values that are
  better represented in the body as a code-block.

  .. code-block::

    .. partis_attr:: {name}
      :type: {typename}
      :prefix: {prefix}
      :value: {value}

      {doc}

  Parameters
  ----------
  name : str
    Name of attribute
  typename : str | type
    Type of the attribute
  obj : str | object
    Object to which the attribute belongs
  val : str | object
    A value that the attribute has, or its default value.
  prefix : str
    An optional prefix for the attribute (e.g. 'property')
  doc : str
    Description part of the docstring

    .. note::

      The text may be modified to remove certain reStructuredText syntax that
      is not compatible with nesting in the sphinx documentation generator.
      For example, section titles will be replaced with simple bold markup.

  noindex : bool
    Flag for whether to mark the attribute with :noindex:, in case the generated
    docstring is being used in more than one location, such as part of the
    docstring of another object.

  """

  if isinstance( typename, type ):
    typename = _fmt_class_name( typename )

    if typename == 'NoneType':
      typename = 'None'

  lines = [
    '',
    f'.. partis_attr:: {name}',
    f'  :type: {typename}' ]

  if noindex:
    lines.append(f'  :noindex:')

  if prefix is not NOTSET:
    lines.append(f'  :prefix: {prefix}')

  # if obj is not NOTSET:
  #   if isinstance( obj, type ):
  #     obj = _fmt_class_name( obj )
  #
  #   lines.append(f'  :canonical: {obj}')

  if val is not NOTSET:

    if val == '...' or val == ...:
      val_str = '...'

    else:
      val_str = fmt_obj( val,  multiline = True )

    val_lines = split_lines( val_str )

    if len(val_lines) > 1 or len(val_str) > 20:
      # insert the value as a block literal below the attribute

      lines.extend([
        '  :value: ...',
        '',
        '  ::',
        '',
        *indent_lines( 4, val_lines ),
        '' ])

    else:
      lines.append(f'  :value: {val_str}')

  if doc is not NOTSET:
    # remove section markings, replaced by simply using bold font to indicate titles
    doc_lines = split_lines(doc)

    ignore_lines = False

    out_lines = list()

    for line in doc_lines:
      m = re.fullmatch(r'^([ ])*[\=\-\^\#]+$', line)

      if m:
        # a line of all section characters
        if len(out_lines):
          # section title is the previous line
          title = out_lines[-1].strip()

          if title in ['Parameters', 'Returns', 'Raises']:
            # completely ignore these sections, since they need to be processed
            # by sphinx at the docstring level
            ignore_lines = True
          else:
            # format into bold font
            # current indentation taken from the first match group

            out_lines[-1] = f"{m.group(1)}**{title}**"
            ignore_lines = False

      else:
        if ignore_lines and len(out_lines):
          out_lines.pop()

        out_lines.append(line)

    lines.extend([''] + indent_lines(2, out_lines) )

  return '\n'.join(lines)
