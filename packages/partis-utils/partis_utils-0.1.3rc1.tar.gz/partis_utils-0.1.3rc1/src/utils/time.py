import time
import decimal

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TimerMono:
  """A monotonic time that uses the system set time as the reference point,
  including time elapsed during sleep.
  """

  #-----------------------------------------------------------------------------
  def __init__( self, timer = None, prec = None ):

    if timer is None:
      timer = time.perf_counter

    self._timer = timer

    self._time_abs = time.time()
    self._time_rel = self._timer()
    self._ctx = decimal.Context( prec = prec )
    self._prev_ctx = None

  #-----------------------------------------------------------------------------
  def __call__( self ):
    with self as ctx:
      return (
        ctx.create_decimal(self._time_abs)
        + ctx.create_decimal(self._timer() - self._time_rel) )

  #-----------------------------------------------------------------------------
  def create( self, *args ):
    with self as ctx:
      return sum([
        ctx.create_decimal(x)
        for x in args ])

  #-----------------------------------------------------------------------------
  def __enter__(self):
    self._prev_ctx = decimal.getcontext()
    decimal.setcontext(self._ctx)

    return self._ctx

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):

    decimal.setcontext(self._prev_ctx)
    self._prev_ctx = None

    # do not handle any other exceptions here
    return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
timer = TimerMono( prec = 32 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TimeEncode:
  digits = '0123456789abcdefghijklmnopqrstuvwxyz'

  def __init__(self,
    resolution = 1,
    rollover = 2**32,
    width = 0,
    base = 36 ):
    """Encode unix timestamp

    Parameters
    ----------
    resolution : int
      Number of seconds that are resolved
    rollover : int
      Number of seconds upper bound before wrapping.
      The number of distinct values is ``rollover // resolution``
    width : int
      Minimal witdth of encoded number
    base : int
      Numeric base used to encode number
    """

    assert base <= len(self.digits)

    self.resolution = resolution
    self.rollover = rollover
    self.modulus = rollover // resolution
    self.width = width
    self.base = base

  #-----------------------------------------------------------------------------
  @property
  def max(self):
    return self.encode( self.resolution * (self.modulus-1) )

  #-----------------------------------------------------------------------------
  def encode(self, num):
    num = ( int(num) // self.resolution ) % self.modulus
    res = []
    base = self.base
    digits = self.digits

    while num:
      num, i = divmod(num, base)
      res.append(digits[i])

    ts = ''.join(reversed(res))

    return f'{ts:0>{self.width}}'
