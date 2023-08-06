import inspect
from collections.abc import (
  Mapping,
  Sequence )

import trio

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def aval( val, *args, **kwargs ):
  """Returns a value from plain data, callable, or coroutine
  """

  if callable( val ):
    val = val( *args, **kwargs )

  if inspect.isawaitable( val ):
    val = await val

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AsyncTarget:
  """Provides an asynchronous return value using an event driven callback
  """

  #-----------------------------------------------------------------------------
  def __init__( self, t = 0.25 ):
    self._t = t
    self._noval = object()
    self._result = self._noval
    self._error = self._noval

  #-----------------------------------------------------------------------------
  def on_result( self, result = None ):
    self._result = result

  #-----------------------------------------------------------------------------
  def on_error( self, error = None ):
    self._error = error

  #-----------------------------------------------------------------------------
  async def wait( self ):
    while self._result is self._noval and self._error is self._noval:
      await trio.sleep( self._t )

    if self._result is self._noval:
      self._result = None

    if self._error is self._noval:
      self._error = None

    return self._result, self._error

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TrioFuture:
  """Wrapping class to store the result of running an awaitable
  """

  #-----------------------------------------------------------------------------
  def __init__( self, f ):
    self._f = f
    self._res = None
    self._exc = None
    self._nursery = None

  #-----------------------------------------------------------------------------
  async def run( self,
    nursery,
    re_raise = True,
    cancel_on_complete = False ):
    """Runs the awaitable within a given nursery
    """
    self._nursery = nursery

    try:
      self._res = await self._f

      if cancel_on_complete:
        nursery.cancel()

    except Exception as e:
      self._exc = e

      if re_raise:
        raise

  #-----------------------------------------------------------------------------
  @property
  def result( self ):
    if self._exc is not None:
      raise self._exc

    return self._res

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def wait_all( awaitables ):
  """Runs and waits for all awaitables to complete, returning the result

  An exception is raised if any awaitable raises an exception.

  Parameters
  ----------
  awaitables : Sequence[ awaitable ] | Mapping[ object, awaitable ]
    Sequence or mapping of awaitables to run.

  Returns
  -------
  results : Sequece | Mapping
    Result of each awaitable in the original sequence or mapping
  """

  if isinstance( awaitables, Mapping ):
    futures = [ ( k, TrioFuture(f) ) for k, f in awaitables.items() ]

    async with trio.open_nursery() as nursery:

      for k, f in futures:
        nursery.start_soon( f.run, nursery )

    return type(awaitables)( [ ( k, f.result ) for k, f in futures ] )

  if isinstance( awaitables, Sequence ):
    futures = [ TrioFuture(f) for f in awaitables ]

    async with trio.open_nursery() as nursery:

      for f in futures:
        nursery.start_soon( f.run, nursery )

    return [ f.result for f in futures ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ResourceReq:
  #-----------------------------------------------------------------------------
  def __init__(self, limiter, resources):
    if not isinstance(limiter, ResourceLimiter):
      raise ValueError(f"'limiter' must be ResourceLimiter: {limiter}")

    for k, v in resources.items():
      if k not in limiter._limits:
        raise ValueError(f"Resource not defined: {k}")

      limit = limiter._limits[k]

      if v > limit:
        raise ValueError(f"Resource limited to {limit} <= {k}: {v}")

    self.limiter = limiter
    self.resources = resources

  #-----------------------------------------------------------------------------
  async def __aenter__(self):
    return await self.limiter.acquire(self)

  #-----------------------------------------------------------------------------
  async def __aexit__(self, type, value, traceback):
    await self.limiter.release(self)

    return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ResourceLimiter:
  """More general implementation of trio.CapacityLimiter

  Allows each acquisition to be a variable amount of one or more resources.
  """
  def __init__(self, **limits):
    if not (
      len(limits) > 0
      and all(isinstance(v, int) and v >= 0 for v in limits.values()) ):

      raise ValueError(f"'limits' must be integers >= 0: {limits}")

    self._lot = trio.lowlevel.ParkingLot()
    self._limits = dict(limits)
    self._avail = dict(limits)

  #-----------------------------------------------------------------------------
  def require(self, **resources):
    return ResourceReq(self, resources)

  #-----------------------------------------------------------------------------
  def _acquire(self, req):
    for k, v in req.resources.items():
      if self._avail[k] < v:
        raise trio.WouldBlock


    for k, v in req.resources.items():
      self._avail[k] -= v

    return req

  #-----------------------------------------------------------------------------
  async def acquire(self, req):
    assert isinstance(req, ResourceReq) and req.limiter is self

    await trio.lowlevel.checkpoint_if_cancelled()
    try:
      return self._acquire(req)

    except trio.WouldBlock:

      while True:
        await self._lot.park()

        try:
          return self._acquire(req)
        except trio.WouldBlock:
          pass

    else:
      await trio.lowlevel.cancel_shielded_checkpoint()

  #-----------------------------------------------------------------------------
  async def release(self, req):
    assert isinstance(req, ResourceReq) and req.limiter is self

    await trio.lowlevel.checkpoint_if_cancelled()

    for k, v in req.resources.items():
      self._avail[k] += v

    self._lot.unpark()

    await trio.lowlevel.cancel_shielded_checkpoint()
