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

_mono_1 = "#1c1d1f"
_mono_2 = "#3b3d41"
_mono_3 = "#5c626c"

_cyan = "#246c75"
_cyan_2 = "#005d69"

_blue = "#005298"
_blue_2 = "#005298"

_magenta = "#691982"
_magenta_2 = "#691982"

_green = "#39601f"
_green_2 = "#39601f"

_red = "#791e25"
_red_2 = "#5c140f"

_orange = "#ac5f14"
_orange_2 = "#a27106"

_syntax_fg = _mono_1
_syntax_bg = "#d2dae8"
_syntax_accent = "#bccdee"

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
    Keyword.Type : f'bold {_orange_2}',
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
    Name.Class : f'bold {_orange_2}',
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
