import os
import os.path as osp
import time
import tempfile
import re
import psutil
import platform
from .time import timer

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MutexFileError( Exception ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MutexFileTimeout( MutexFileError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MutexBase:
  """Base mutex class that does nothing
  """

  #-----------------------------------------------------------------------------
  def __init__(self,
    period = None ):

    if period is None:
      period = 0.5

    period = float(period)

    self._period = period

  #-----------------------------------------------------------------------------
  def __enter__(self):

    for i in self.acquire():

      time.sleep(self._period)

    return self

  #-----------------------------------------------------------------------------
  async def __aenter__(self):
    import trio

    for i in self.acquire():
      await trio.sleep(self._period)

    return self

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):

    try:
      if not self.is_acquired():
        raise MutexFileError(f"mutex violated before release: {self}") from value

    finally:
      self.release()

    # do not handle any other exceptions here
    return False

  #-----------------------------------------------------------------------------
  async def __aexit__(self, type, value, traceback):

    try:
      if not self.is_acquired():
        raise MutexFileError(f"mutex violated before release: {self}") from value

    finally:
      self.release()

    # do not handle any exceptions here
    return False

  #-----------------------------------------------------------------------------
  def acquire( self ):
    for i in range(0):
      yield i

  #-----------------------------------------------------------------------------
  def release( self ):
    pass

  #-----------------------------------------------------------------------------
  def is_acquired( self ):
    return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MutexFile( MutexBase ):
  """Creates a multiprocessing mutex (mutually exclusive) using files

  .. note::

    MutexFile will also work on a shared filesystem as long as the
    fully-qualified domain name of each host is unique.
    However, orphaned mutex files from processes that ended before releasing the
    mutex can only be cleaned by another process running on the same host.

  Parameters
  ----------
  prefix : str
    Unique name which will be tied to the mutex.
    Only one MutexFile (in any process) with the same 'prefix' and 'dir' will be
    able to aqcuire the mutex and enter the context.
  dir : str | None
    Directory in which to create the mutex files
    default: ``osp.join( tempfile.gettempdir(),  prefix + '_mutex')``
  period : float | None
    Period in seconds between attempts to aqcuire the mutex
    default: 0.5
  hostname : str | None
    Name uniquely identifying this host.
    default: ``platform.node()``

    .. note::

      The name will be sanitized to contain only word characters.
      If the hostname is no longer unique after sanitization, relative to other
      hosts attempting a mutex lock, the behaviour is undefined.

  timeout : float | None
    Maximum time in seconds which attempts will be retried.
    Will raise exception if this is exceeded.
    default: inf
  expiration: float | None
    Maximum time that a mutex file will remain valid, whether or not a lock
    has been acquired.
    default: inf


  See Also
  --------
  * https://man7.org/linux/man-pages/man2/open.2.html

    On NFS, O_EXCL is supported only when using NFSv3 or later
    on kernel 2.6 or later.  In NFS environments where O_EXCL
    support is not provided, programs that rely on it for
    performing locking tasks will contain a race condition.
    Portable programs that want to perform atomic file locking
    using a lockfile, and need to avoid reliance on NFS
    support for O_EXCL, **can create a unique file on the same
    filesystem (e.g., incorporating hostname and PID), and use
    link(2) to make a link to the lockfile**.  If link(2)
    returns 0, the lock is successful.  Otherwise, use stat(2)
    on the unique file to check if its link count has
    increased to 2, in which case the lock is also successful.

  """

  #-----------------------------------------------------------------------------
  def __init__(self,
    prefix,
    dir = None,
    period = None,
    hostname = None,
    timeout = None,
    expiration = None ):

    super().__init__(
      period = period )

    if not prefix:
      raise ValueError(f"prefix must be a non-empty string")

    prefix = str(prefix)

    if not re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9_\-]*$', prefix ):
      raise ValueError(
        f"prefix must contain only letters, digits, '_', '-', and start with a letter: {prefix}")

    if dir is None:
      dir = osp.join(
        tempfile.gettempdir(),
        prefix + '_mutex')

    dir = osp.abspath(dir)

    if hostname is None:
      hostname = platform.node()

    hostname = re.sub(r'[^a-zA-Z0-9]+', '_', str(hostname) )

    if timeout is None:
      timeout = 0.0

    timeout = timer.create(timeout)

    if expiration is None:
      expiration = 0.0

    expiration = timer.create(expiration)

    self._prefix = prefix
    self._dir = dir
    self._timeout = timeout
    self._expiration = expiration

    self._pid = os.getpid()
    self._mrec = re.compile(rf'mutex\.{prefix}\.([a-zA-Z0-9_]+)\.(\d+)$')

    # replace any runs of non alpha-numeric characters with an underscore
    self._hostname = hostname

    self._lname = f"mutex.{prefix}.lock"
    self._mname = f"mutex.{prefix}.{self._hostname}.{self._pid}"

    self._lfile = osp.join( dir, self._lname )
    self._mfile = osp.join( dir, self._mname )
    self._tmpfile = self._mfile + ".tmp"

    self._idx = None
    self._reftime = None
    self._mutex = None

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return f"{type(self).__name__}( {self._mfile} )"

  #-----------------------------------------------------------------------------
  def acquire( self ):

    if self._mutex:
      raise MutexError(f"mutex already created: {self}")

    if not osp.exists(self._dir):
      os.makedirs(self._dir)

    self.release()

    mutexes = self.get_mutexes()

    if mutexes:
      self._idx = mutexes[-1][0] + 1
    else:
      self._idx = 0

    # time used as a reference (must be global clock)
    self._reftime = timer()

    self._mutex = ( self._idx, self._reftime, self._hostname, self._pid )

    # write to temporary file and then move to prevent another process from
    # seeing a partially created mutex file

    content = f"{self._idx}, {self._reftime}, {self._expiration}"

    with open( self._tmpfile, 'w' ) as fp:
      fp.write(content)

    os.replace( self._tmpfile, self._mfile )

    # TODO: it is still possible that a race condition happens where the
    # filesystem is not viewed in time to see the complete ordering of mutex files.

    num = 0

    # time used for timeout
    ftime = self._timeout + self._reftime if self._timeout else 0.0
    ctime = self._reftime

    try:
      while not ftime or ctime < ftime:

        if self.is_acquired():
          return

        # generator yields after a failed attempt to aqcuire
        yield num

        ctime = timer()
        num += 1

      raise MutexFileTimeout(f"mutex acquisition timeout exceeded: {self._timeout}, {self}")

    except:
      self.release()
      raise

  #-----------------------------------------------------------------------------
  def release( self ):
    self.remove_mfile( self._mfile )

    try:
      os.remove(self._tmpfile)
    except:
      pass

    self._idx = None
    self._reftime = None
    self._mutex = None

  #-----------------------------------------------------------------------------
  def is_acquired( self ):

    mutexes = self.get_mutexes()

    if self._mutex not in mutexes:
      raise MutexFileError(f"mutex no longer exists: {self}")

    # NOTE: there must be at least one if self._mutex is in the list
    idx, reftime, hostname, pid = mutexes[0]

    # this process now has the top mutex
    if hostname == self._hostname and pid == self._pid:

      try:
        # attempt to link the lockfile to the mutex file
        os.symlink(self._mfile, self._lfile)
        return True

      except FileExistsError:
        pass

      try:
        # verify that the link points to the mutex
        mfile = os.readlink(self._lfile)
        return mfile == self._mfile
      except:
        pass

    return False

  #-----------------------------------------------------------------------------
  def get_lfile( self ):
    try:

      mfile = os.readlink(self._lfile)

      mutex = self.get_mfile( mfile )

      return mutex

    except FileNotFoundError:
      pass

    except OSError:
      try:
        os.remove(self._lfile)
      except:
        pass

    return None

  #-----------------------------------------------------------------------------
  def get_mfile( self, mfile ):

    mname = osp.basename(mfile)

    m = self._mrec.fullmatch(mname)

    if not m:
      return None

    try:

      hostname = str(m.group(1))
      pid = int(m.group(2))

      with open( mfile, 'r' ) as fp:
        idx, reftime, expiration = fp.read().split(',')

      idx = int(idx.strip())
      reftime = timer.create(reftime.strip())
      expiration = timer.create(expiration.strip())

      if (
        # remove mutex of process that is known to not be running
        hostname == self._hostname
        and not psutil.pid_exists(pid) ):

        self.remove_mfile(mfile)
        return None

      elif expiration:
        curtime = timer()

        with timer as ctx:
          if (curtime - reftime) > expiration:

            self.remove_mfile(mfile)
            return None

      mutex = ( idx, reftime, hostname, pid )

      return mutex

    except:
      pass

    return None


  #-----------------------------------------------------------------------------
  def remove_mfile( self, mfile ):
    try:
      _mfile = os.readlink(self._lfile)

    except FileNotFoundError:
      pass

    except OSError:
      # remove the lock file if it cannot be read
      os.remove(self._lfile)

    else:
      if _mfile == mfile:
        # remove the lock file if it points to the mfile being removed
        os.remove( self._lfile )

    try:
      os.remove( mfile )
    except:
      pass

  #-----------------------------------------------------------------------------
  def get_mutexes( self ):

    mutexes = list()

    if not osp.exists(self._dir):
      return mutexes

    locked_mutex = self.get_lfile()

    for mname in os.listdir(self._dir):

      mfile = osp.join( self._dir, mname )

      mutex = self.get_mfile(mfile)

      if mutex and mutex != locked_mutex:
        mutexes.append( mutex )

    # all mutex ordered by idx, then reference time, then by hostname, then by pid
    mutexes = sorted( mutexes )

    if locked_mutex:
      # ensures current mutex is always listed first
      mutexes.insert(0, locked_mutex)

    return mutexes
