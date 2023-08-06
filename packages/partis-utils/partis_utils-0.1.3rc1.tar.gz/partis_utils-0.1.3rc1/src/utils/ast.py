import sys

if sys.version_info >= (3, 8):
  from ast import *
else:
  from typed_ast.ast import *

if sys.version_info >= (3, 9):
  # added in 3.9
  # from ast import unparse
  pass
else:
  from astunparse import unparse