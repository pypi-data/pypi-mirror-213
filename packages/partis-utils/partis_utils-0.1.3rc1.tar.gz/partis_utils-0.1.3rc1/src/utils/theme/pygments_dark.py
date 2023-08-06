from pygments.style import Style
from pygments.token import (
  Keyword,
  Name,
  Punctuation,
  Comment,
  String,
  Literal,
  Text,
  Error,
  Number,
  Operator,
  Generic )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_mono_1 = "#c9cdd1"
_mono_2 = "#9b9fa2"
_mono_3 = "#757a7d"

_cyan = "#56b6c2"
_cyan_2 = "#79bac2"

_blue = "#61aeee"
_blue_2 = "#61aeee"

_magenta = "#c678dd"
_magenta_2 = "#cc8fde"

_green = "#98c379"
_green_2 = "#82af61"

_red = "#e06c75"
_red_2 = "#be5046"

_orange = "#d19a66"
_orange_2 = "#e6c07b"

_syntax_fg = _mono_1
_syntax_bg = "#282c34"
_syntax_accent = "#2a3345"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PygmentsStyle(Style):
  background_color = _syntax_bg
  highlight_color = _syntax_accent

  default_style = ''

  styles = {
    Text : _mono_1,
    Text.Whitespace : _mono_3,
    Punctuation : _cyan_2,
    Comment : f'italic {_mono_3}',
    Comment.Hashbang : f'italic {_mono_3}',
    Comment.Multiline : f'italic {_mono_3}',
    Comment.Preproc : _orange,
    Comment.PreprocFile : f'italic {_mono_3}',
    Comment.Single : f'italic {_mono_3}',
    Comment.Special : f'italic {_mono_3}',
    Generic : _orange,
    Generic.Deleted : _red_2,
    Generic.Emph : 'italic',
    Generic.Error : f'border:{_red_2}',
    Generic.Heading : f'bold {_blue}',
    Generic.Inserted : _green,
    Generic.Output : _mono_1,
    Generic.Prompt : f'{_blue}',
    Generic.Strong : 'bold',
    Generic.Subheading : f'{_magenta}',
    Generic.Traceback : _green_2,
    Keyword : _magenta,
    Keyword.Constant : f'{_orange}',
    Keyword.Declaration : f'{_orange}',
    Keyword.Namespace : f'{_magenta}',
    Keyword.Pseudo : f'{_orange}',
    Keyword.Reserved : f'{_orange}',
    Keyword.Type : _orange_2,
    Operator : _mono_2,
    Operator.Word : _magenta_2,
    Name : _mono_1,
    Name.Namespace : _mono_1,
    Name.Tag : f'{_red}',
    Name.Label : _orange,
    Name.Other : _orange,
    Name.Attribute : _orange,
    Name.Property : _orange,
    Name.Builtin : _blue,
    Name.Builtin.Pseudo : _orange,
    Name.Constant : _orange,
    Name.Class : f'{_orange_2}',
    Name.Decorator : _magenta,
    Name.Entity : f'{_magenta}',
    Name.Exception : f'{_red}',
    Name.Function : _blue,
    Name.Function.Magic : _blue,
    Name.Variable : _magenta,
    Name.Variable.Class : _red,
    Name.Variable.Global : _red,
    Name.Variable.Instance : _red,
    Name.Variable.Magic : _red,
    # NOTE: custom name token
    Name.External : f'{_blue_2} underline',
    Literal : _orange,
    Literal.Number : _orange,
    Literal.Number.Bin : _orange,
    Literal.Number.Float : _orange,
    Literal.Number.Hex : _orange,
    Literal.Number.Integer : _orange,
    Literal.Number.Integer.Long : _orange,
    Literal.Number.Oct : _orange,
    Literal.String : _green,
    Literal.String.Affix : _green,
    Literal.String.Backtick : _green,
    Literal.String.Char : _green,
    Literal.String.Delimiter : _green,
    Literal.String.Doc : _green,
    Literal.String.Double : _green,
    Literal.String.Escape : _cyan,
    Literal.String.Heredoc : _green,
    Literal.String.Interpol : _red_2,
    Literal.String.Other : _green,
    Literal.String.Regex : _cyan,
    Literal.String.Single : _green,
    Literal.String.Symbol : _green,
    Literal.Scalar : _green,
    Literal.Scalar.Plain : _green }
