
import sys
import os
import os.path as osp
import pytest

from partis.utils.hint import (
  HINT_LEVELS_TO_NUM,
  hint_level_name,
  hint_level_num,
  DEBUG,
  ModelHint,
  ModelError,
  Loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# unicode
HU = """
● abc
│ def
│ ◹ 1969-12-31 21:25:45 by asd at f[3].g in "1" line 2 col 3
│   xyz
├╸'a'
├╸'b'
╰╸'c'"""

# ascii
HA = """
* abc
| def
| > 1969-12-31 21:25:45 by asd at f[3].g in "1" line 2 col 3
|   xyz
- 'a'
- 'b'
- 'c'"""

HF = """
● abc
│ def
│ ◹ 1969-12-31 21:25:45 by asd at f[3].g in "1" line 2 col 3
│   xyz
├╸'a'
├╸'b'
╰╸'c'
"""


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HLISTU = """
● <list>
├╸0: 1
├╸1: 2
╰╸2: 3"""

HLISTA = """
* <list>
- 0: 1
- 1: 2
- 2: 3"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint():

  h = ModelHint(
    msg = """abc
      def
      """,
    data = '  xyz',
    format = 'literal',
    loc = Loc(
      filename = '1',
      line = 2,
      col = 3,
      path = ['f', 3, 'g'],
      owner = 'asd',
      time = 12345.0 ),
    level = 'debug',
    hints = ['a', 'b', 'c'] )

  h_u = h.fmt()
  print(h_u)

  assert h.msg == "abc\ndef"
  assert h.data == '  xyz'
  assert h.format == 'literal'
  assert h.loc.filename == '1'
  assert h.loc.line == 2
  assert h.loc.col == 3
  assert h.loc.path == ['f', 3, 'g']
  assert h.loc.owner == 'asd'
  assert h.loc.time == 12345.0
  assert h.level == 'DEBUG'
  assert h.level_num == DEBUG
  assert h.hints[0].data == "'a'"
  assert h.hints[0].level == 'DEBUG'
  assert h.hints[1].data == "'b'"
  assert h.hints[1].level == 'DEBUG'
  assert h.hints[2].data == "'c'"
  assert h.hints[2].level == 'DEBUG'



  h_a = h.fmt(with_unicode = False)
  print(h_a)
  assert h_u == HU[1:]
  assert h_a == HA[1:]

  d1 = h.to_dict()
  print('d1', d1)

  d2 = dict(
    msg = "abc\ndef",
    data = '  xyz',
    format = 'literal',
    relation = 'related',
    loc = dict(
      filename = '1',
      line = 2,
      col = 3,
      path = ['f', 3, 'g'],
      owner = 'asd',
      time = 12345.0 ),
    level = 'DEBUG',
    hints = [
      dict(
        data = "'a'",
        msg = '',
        format = 'auto',
        relation = 'related',
        loc = dict(),
        level = 'DEBUG',
        hints = list() ),
      dict(
        data = "'b'",
        msg = '',
        format = 'auto',
        relation = 'related',
        loc = dict(),
        level = 'DEBUG',
        hints = list() ),
      dict(
        data = "'c'",
        msg = '',
        format = 'auto',
        relation = 'related',
        loc = dict(),
        level = 'DEBUG',
        hints = list() ) ] )

  print('d2', d2)


  assert d1 == d2

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint_error():

  try:

    raise ModelError('abc', data = 'xyz')

  except ModelError as e:

    h = ModelHint.cast(e)

  print(h)

  assert h.msg == 'During: `test_hint_error`'
  # assert h.data == "`raise ModelError('abc', data = 'xyz')`"
  assert h.data == ''
  assert h.format == 'block'
  assert h.level == 'DEBUG'
  assert h.loc.filename.endswith('test_hint.py')

  assert not isinstance(h, (ModelError, Exception))
  assert type(h) is ModelHint
  assert h.hints[0].msg == 'abc'
  assert h.hints[0].data == 'xyz'
  assert h.hints[0].format == 'auto'
  assert h.hints[0].level == 'ERROR'


  d1 = h.to_dict()

  print('d1', d1)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint_cast_list():
  h = ModelHint.cast([1, 2, 3])
  p = ModelHint.cast("123")

  h_u = h.fmt()
  print(h_u)

  assert h.data == '<list>'
  assert h.hints[0].msg == '0'
  assert h.hints[0].data == '1'
  assert h.hints[1].msg == '1'
  assert h.hints[1].data == '2'
  assert h.hints[2].msg == '2'
  assert h.hints[2].data == '3'

  assert p.data == '123'

  h_a = h.fmt(with_unicode = False)
  print(h_a)

  assert h_u == HLISTU[1:]
  assert h_a == HLISTA[1:]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint_cast_dict():
  h = ModelHint.cast({'a': 1, 'b': 2, 'c': 3})

  print(h)


  assert h.data == '<dict>'
  assert h.hints[0].msg == 'a'
  assert h.hints[0].data == '1'
  assert h.hints[1].msg == 'b'
  assert h.hints[1].data == '2'
  assert h.hints[2].msg == 'c'
  assert h.hints[2].data == '3'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint_cast_error():

  try:

    raise ValueError('abc')

  except ValueError as e:

    h = ModelHint.cast(e)

  #h_f = h.filter(h, '0', None)
  #print(h_f)

  assert h.msg == 'During: `test_hint_cast_error`'
  # assert h.data == "`raise ValueError('abc')`"
  assert h.data == ''
  assert h.format == 'block'
  assert h.level == 'DEBUG'
  assert h.loc.filename.endswith('test_hint.py')

  assert not isinstance(h, (ModelError, Exception))
  assert type(h) is ModelHint
  assert h.hints[0].msg == 'ValueError'
  assert h.hints[0].data == 'abc'
  assert h.hints[0].format == 'literal'
  assert h.hints[0].level == 'ERROR'

  d1 = h.to_dict()
  print('d1', d1)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def test_hint_functions():
    h = ModelHint(
    msg = """abc
      def
      """,
    data = '  xyz',
    format = 'literal',
    loc = Loc(
      filename = '1',
      line = 2,
      col = 3,
      path = ['f', 3, 'g'],
      owner = 'asd',
      time = 12345.0 ),
    level = 'debug',
    hints = ['a', 'b', 'c'] )


    h_f = h.filter(h,3,None)
    h.fmt(level = 5, initdepth = None)

    assert h_f[0].msg == "abc\ndef"
    assert h_f[0].data == '  xyz'
    assert h_f[0].format == 'literal'
    assert h_f[0].loc.filename == '1'
    assert h_f[0].loc.line == 2
    assert h_f[0].loc.col == 3
    assert h_f[0].loc.path == ['f', 3, 'g']
    assert h_f[0].loc.owner == 'asd'
    assert h_f[0].loc.time == 12345.0
    assert h_f[0].level == 'DEBUG'
    assert h_f[0].level_num == DEBUG
    assert h_f[0].hints[0].data == "'a'"
    assert h_f[0].hints[0].level == 'DEBUG'
    assert h_f[0].hints[1].data == "'b'"
    assert h_f[0].hints[1].level == 'DEBUG'
    assert h_f[0].hints[2].data == "'c'"
    assert h_f[0].hints[2].level == 'DEBUG'

    fmt_m = h.fmt(maxdepth = -1)
    assert fmt_m == "max depth reached: -1"
    with pytest.raises(ValueError):
      h.fmt(level = "5")

    with pytest.raises(TypeError):
      h.loc = [1,2,3,4]

    with pytest.raises(TypeError):
      h.loc = {'test_key': 'test_value', '1': '5', '7': '2', '4': '0'}

    with pytest.raises(ValueError):
      h.format = 1



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_hint_levels():
  h = hint_level_num(15)
  assert h == 15
  with pytest.raises(ValueError):
    n_s = hint_level_num([1,2,5])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':
  test_hint_cast_list()
  test_hint_levels()
  test_hint_functions()
  test_hint()
  test_hint_error()
