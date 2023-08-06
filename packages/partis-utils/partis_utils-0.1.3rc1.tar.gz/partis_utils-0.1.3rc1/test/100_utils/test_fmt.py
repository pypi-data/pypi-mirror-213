import numpy as np
import array

import partis.utils.fmt as fmt

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_fmt_src_line():
  fmt.fmt_src_line(fmt)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_split_lines():
  assert fmt.split_lines("") == ["", ]
  assert fmt.split_lines("a") == ["a", ]
  assert fmt.split_lines("ab") == ["ab", ]
  assert fmt.split_lines("a\nb") == ["a", "b"]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_indent_lines():
  x = "a\nb\nc"

  y = fmt.indent_lines( n = 3, lines = x, mark = "- " )

  assert y == " - a\n   b\n   c"

  y = fmt.indent_lines( n = 0, lines = x, mark = "- " )

  assert y == x

  y = fmt.indent_lines( n = 3, lines = ['a', 'b', 'c'], mark = "++ " )

  assert y == ["++ a", "   b", "   c"]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_fmt_base_or_type():
  assert fmt.fmt_base_or_type( str ) == "`str`"
  assert fmt.fmt_base_or_type( object() ) == "`object`"

  assert fmt.fmt_base_or_type( 'xyz' ) == "'xyz'"

  assert fmt.fmt_base_or_type( True ) == "True"
  assert fmt.fmt_base_or_type( 1 ) == "1"
  assert fmt.fmt_base_or_type( 1.1 ) == "1.1"
  assert fmt.fmt_base_or_type( 1 + 1j ) == "(1+1j)"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DummyGPUArrayFlags:
  def __init__( self, flags ):
    for k in flags:
      setattr( self, k, True )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DummyGPUArray:
  def __init__( self, shape, dtype, flags ):
    self.shape = shape
    self.dtype = dtype
    self.flags = DummyGPUArrayFlags( flags )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_fmt_array():

  arrs = [
    np.zeros( (1, 3, 4), dtype = np.float32 ),
    array.array( 'd', [1, 2, 3, 4]),
    bytes([1, 2, 3, 4]),
    bytearray([1, 2, 3, 4]),
    memoryview(bytearray([1, 2, 3, 4])).cast('B', (2,2)),
    DummyGPUArray( shape = (1, 2, 3), dtype = np.float32, flags = ['c_contiguous', ]),
    "hello world",
    b"hello world",
    # technically not an array, but someone might format a list
    [1, 2, 3, 4] ]

  for arr in arrs:
    x = fmt.fmt_array( obj = arr )
    print(x)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_fmt_limit():
  x = fmt.fmt_limit(
    "hello world\nhello world\nhello world",
    width = 5,
    height = 2 )

  assert x == "hel|...|ld\nhel|...|ld"
