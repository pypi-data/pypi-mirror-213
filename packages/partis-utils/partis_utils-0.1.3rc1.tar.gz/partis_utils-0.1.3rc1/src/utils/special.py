
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NoType:
  """Class indicating a type which no class is a sub-class
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SpecialType:
  """Base class for special values
  """
  _instance = None

  #-----------------------------------------------------------------------------
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)

    return cls._instance

  #-----------------------------------------------------------------------------
  def __bool__( self ):
    return False

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return self.__class__.__name__[:-4]

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    return hash(str(self))

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):
    return self is other

  #-----------------------------------------------------------------------------
  def __ne__( self, other ):
    return self is not other

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NotSetType( SpecialType ):
  """Marks a value that is not set, or otherwise undefined.

  Note
  ----
  This is intended as an alternative to using ``None`` to distinguish parameter
  values that where never specified from ones that have a specified value of ``None``,
  but may often be set by methods that assume that ``None`` is intended to be
  used as the 'Not Set' value.
  """

notset = NotSetType()
NOTSET = notset
NotSet = notset

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RequiredType( SpecialType ):
  """Marks a parameter that is required, without a default value, and must not
  be None or otherwise undefined.
  """
  pass

required = RequiredType()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OptionalType( SpecialType ):
  """Marks a parameter that is optional, without a default value, but may be None.
  """
  pass

optional = OptionalType()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DerivedType( SpecialType ):
  """Marks a parameter that is derived, without a default value, but will be
  constructed from other value(s).
  """
  pass

derived = DerivedType()
