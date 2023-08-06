
import sys
import os
import os.path as osp
from pathlib import Path
import shutil
import json
import subprocess

from .log import getLogger

from .mutex_file import MutexBase

from .hint import ModelHint

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def prepend_paths(new, old, sep):
  paths = [p for p in old.split(sep) if p]

  return sep.join([
    *[os.fspath(p) for p in new],
    *paths ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProcessEnv:
  """Base process environment

  Parameters
  ----------
  bin_paths : None | list[str]
    Additional bin paths to make available when running commands.
  logger : None | logging.Logger
    Logger to log messages.

  """

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    bin_paths = None,
    logger = None ):

    if bin_paths is None:
      bin_paths = list()

    logger = logger or getLogger(__name__)

    self._p_bin_paths = [Path(p) for p in bin_paths]
    self._p_logger = logger

    self._p_ctx_bin_paths = None

  #-----------------------------------------------------------------------------
  @property
  def logger(self):
    return self._p_logger

  #-----------------------------------------------------------------------------
  @property
  def bin_paths(self):
    return self._p_bin_paths

  #-----------------------------------------------------------------------------
  def __enter__( self ):
    self._p_ctx_bin_paths = os.environ.get("PATH", None )

    paths = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]

    # prepend new executable paths
    os.environ["PATH"] = prepend_paths(
      new = self._p_bin_paths,
      old = os.environ.get("PATH", ""),
      sep = os.pathsep )

    return self

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):

    if self._p_ctx_bin_paths is None:
      os.environ.pop("PATH")
    else:
      os.environ["PATH"] = self._p_ctx_bin_paths

    self._p_ctx_bin_paths = None

    # do not handle any other exceptions here
    return False

  #-----------------------------------------------------------------------------
  def Popen( self, args, **kwargs ):
    """Runs a process with the environment using ``subprocess.Popen``
    """

    env = kwargs.pop( 'env', os.environ )
    env.update(kwargs.pop('extra_environ', {}))

    PATH = prepend_paths(
      new = self._p_bin_paths,
      old = env.get("PATH", ""),
      sep = os.pathsep )

    return subprocess.Popen(
      args,
      env = {
        **env,
        'PATH' : PATH },
      **kwargs )

  #-----------------------------------------------------------------------------
  def run( self, args, **kwargs ):
    """Runs a process with the environment using ``subprocess.run``
    """

    env = kwargs.pop( 'env', os.environ )

    env.update(kwargs.pop('extra_environ', {}))

    PATH = prepend_paths(
      new = self._p_bin_paths,
      old = env.get("PATH", ""),
      sep = os.pathsep )

    return subprocess.run(
      args,
      env = {
        **env,
        'PATH' : PATH },
      **kwargs )

  #-----------------------------------------------------------------------------
  def run_log( self, args, **kwargs ):

    res = self.run(
      args,
      stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT,
      check = False,
      **kwargs )

    err = res.returncode != 0
    out = res.stdout.decode('utf-8', errors = 'replace')

    self._p_logger.hint(
      ModelHint(
        'Run Command',
        level = 'error' if err else 'debug',
        hints = [
          ModelHint(
            'Arguments',
            level = 'info' if err else 'debug',
            hints = args ),
          ModelHint(
            'Returncode',
            level = 'error' if err else 'debug',
            data = res.returncode),
          ModelHint(
            f"Output",
            level = 'warning' if err else 'debug',
            data = out,
            format = 'block' )]))

    if err:

      raise subprocess.CalledProcessError(
        res.returncode,
        res.args,
        output = res.stdout )

  #-----------------------------------------------------------------------------
  async def trio_run( self, args, **kwargs ):
    """Runs a process with the environment using ``trio.run_process``
    """
    import trio

    env = kwargs.pop( 'env', os.environ )

    PATH = prepend_paths(
      new = self._p_bin_paths,
      old = env.get("PATH", ""),
      sep = os.pathsep )

    return await trio.run_process(
      command = args,
      env = {
        **env,
        'PATH' : PATH },
      **kwargs )

  #-----------------------------------------------------------------------------
  async def trio_run_log( self, args, **kwargs ):

    res = await self.trio_run(
      args,
      capture_stdout = True,
      stderr = subprocess.STDOUT,
      check = False,
      **kwargs )

    out = res.stdout.decode('ascii', errors = 'replace')

    if out:
      self._p_logger.info( out )

    if res.returncode != 0:

      raise subprocess.CalledProcessError(
        res.returncode,
        res.args,
        output = res.stdout )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VirtualEnv( ProcessEnv ):
  """Minimal implementation of a venv process environment manager

  Parameters
  ----------
  path : str
    Path at which to create the virtual environment.
  interpreter : None | str
    The interpreter to use in the venv.
  args : None | list[str]
    Additional arguments passed to create venv.
  bin_paths : None | list[str]
    Additional bin paths to make available when running commands.
  inherit_site_packages : None | list[str]
    Add 'site-packages' search paths to the new venv for the current values in
    ``sys.path``.
    This may be used to chain virtual environments, where packages can use those
    already installed, but new changes will not affect the inherited venv(s).
    If None, the new venv will **not** include any additional paths.
    If a list of paths, the currently running search paths are added in
    addition to any other listed paths.
  reuse_existing : bool
    Attempt to re-use an existing virtual environment at `path`.
    If the specified interpreter does not match, the existing venv will be
    deleted and re-created.
  logger : None | logging.Logger
    Logger to log messages.
  mutex : None | Mutex
    Mutex used to acquire locks on creating or installing to the venv at `path`

  Note
  ----
  Adapted from the nox VirtualEnv: https://github.com/theacodes/nox
  """
  #-----------------------------------------------------------------------------
  def __init__( self, *,
    path,
    interpreter = None,
    args = None,
    bin_paths = None,
    inherit_site_packages = None,
    reuse_existing = False,
    logger = None,
    mutex = None ):

    logger = logger or getLogger(__name__)

    path = Path(path).resolve()

    bin_path = path / 'bin'

    if bin_paths is None:
      bin_paths = list()

    bin_paths = [bin_path] + bin_paths

    if interpreter is None:
      interpreter = Path(sys.executable)

    elif not isinstance(interpreter, Path):
      interpreter = Path(interpreter)

    if not interpreter.is_absolute():
      if len(interpreter.parts) == 1:
        interpreter = Path(shutil.which(interpreter))
      else:
        interpreter = Path.cwd() / interpreter

    if args is None:
      args = list()

    if mutex is None:
      mutex = MutexBase()

    super().__init__(
      bin_paths = bin_paths,
      logger = logger )

    self._p_path = path
    self._p_interpreter = interpreter
    self._p_args = args
    self._p_bin_path = bin_path
    self._p_exec = self.bin_path / 'python'
    self._p_mutex = mutex

    self._p_ctx_sys_path = None

    py_path_cur = Path(sys.executable).parent.parent
    py_path_ori = self.interpreter.parent.parent

    if self.path in [ py_path_cur, py_path_ori]:
      # just set it to re-use the environment
      logger.debug(f"Skipping creation of venv since it points to original interpreter: {self.path}")
      return

    # check that path is not being created inside the current one(s)
    if (
      self.path.is_relative_to(py_path_cur)
      or py_path_cur.is_relative_to(self.path)
      or self.path.is_relative_to(py_path_ori)
      or py_path_ori.is_relative_to(self.path) ):

      raise ValueError(
        f"Cannot create venv within another venv: {self.path}")

    with self._p_mutex:

      if self.path.exists() and any(self.path.iterdir()):

        if not self.exec.exists():
          raise ValueError(
            f"Not removing existing venv because no python was found: {self.exec}")

        valid = False

        if not reuse_existing:
            logger.warning(f"Removing existing venv: {self.path}")
            shutil.rmtree(self.path)

        else:
          logger.info(f"Checking existing venv for re-use: {self.path}")

          try:
            prefix_check_src = "import sys; sys.stdout.write(getattr(sys, 'real_prefix', sys.base_prefix))"

            res_cur = subprocess.check_output([
              os.fspath(self.interpreter),
              '-c',
              prefix_check_src ])

            res_prev = subprocess.check_output([
              os.fspath(self.exec),
              '-c',
              prefix_check_src ])

            res_prev = res_prev.decode('utf-8', errors = 'ignore' )
            res_cur = res_cur.decode('utf-8', errors = 'ignore' )

            if res_cur == res_prev:
              valid = True
            else:
              logger.warning(f"Existing venv uses different interpreter: {res_prev} != {res_cur}")

          except subprocess.SubprocessError as e:
            logger.warning("Interpreter check failed", exc_info = True )

          if not valid:
            logger.warning(f"Removing existing incompatible venv: {self.path}")
            shutil.rmtree(self.path)

      if not (self.path.exists() and any(self.path.iterdir())):
        logger.detail(f"Creating venv: {self.path}")

        subprocess.check_call([
          os.fspath(self.interpreter),
          '-m',
          'venv',
          os.fspath(self.path),
          *args ])

      if bool(inherit_site_packages) or isinstance(inherit_site_packages, list):
        site_paths = dict()
        sys_path = [ Path(p) for p in sys.path ]

        if isinstance(inherit_site_packages, list):
          for dir in inherit_site_packages:
            dir = Path(dir).resolve()
            exec = dir / 'bin' / 'python'

            if not exec.is_file():
              logger.warning(f"ignoring inheritance, python not found: {dir}")
              continue

            sys_path += VirtualEnv.get_sys_path( exec )

        for path in sys_path:
          path = path.resolve()

          if path.name == 'site-packages':
            # get the path relative to existing installation base directory
            # e.g. 'lib/pythonX.Y/site-packages'
            site_dir = path.relative_to(path.parent.parent.parent)

            if not (self.path / site_dir).is_dir():
              # the new venv does not have a corresponding site-packages directory
              # likely due to different versions
              logger.warning(f"ignoring inheritance, incompatible site: {site_dir}")
              continue

            # store the complete path to be added to the sys.path of the venv
            site_paths.setdefault( site_dir, [] ).append(path)

        for site_dir, paths in site_paths.items():
          # create a .pth file in the new venv with all 'site-packages' paths
          inherit_pth = self.path / site_dir / 'venv_inherited.pth'

          with open( inherit_pth, 'w' ) as fp:
            fp.write( '\n'.join([os.fspath(p) for p in paths]) )

  #-----------------------------------------------------------------------------
  @property
  def bin_path(self):
    return self._p_bin_path

  #-----------------------------------------------------------------------------
  @property
  def interpreter(self):
    return self._p_interpreter

  #-----------------------------------------------------------------------------
  @property
  def path(self):
    return self._p_path

  #-----------------------------------------------------------------------------
  @property
  def exec(self):
    return self._p_exec

  #-----------------------------------------------------------------------------
  def __enter__( self ):
    self._p_ctx_sys_path = sys.path

    sys.path = sys.path + [ os.fspath(p) for p in self.sys_path ]

    return super().__enter__()

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):

    sys.path = self._p_ctx_sys_path
    self._p_ctx_sys_path = None

    # do not handle any other exceptions here
    return super().__exit__(type, value, traceback)

  #-----------------------------------------------------------------------------
  @staticmethod
  def get_sys_path( exec ):
    """The sys.path that will be used in the new venv
    """

    sys_path_src = "import sys; import json; sys.stdout.write(json.dumps(sys.path))"

    res = subprocess.run([
        os.fspath(exec),
        '-c',
        sys_path_src ],
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      check = True )

    sys_path = json.loads( res.stdout.decode('utf-8', errors = 'ignore' ) )

    return [ Path(p) for p in sys_path ]

  #-----------------------------------------------------------------------------
  @staticmethod
  def get_pip_version( exec ):
    """Version (major only) of pip currently installed in the virtual environment
    """

    pip_version_src = "import sys; import pip; sys.stdout.write(pip.__version__.split('.')[0])"

    res = subprocess.run([
        os.fspath(exec),
        '-c',
        pip_version_src ],
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      check = True )

    pip_version = int( res.stdout.decode('utf-8', errors = 'ignore' ) )

    return pip_version

  #-----------------------------------------------------------------------------
  @property
  def sys_path(self):
    """The sys.path that will be used in the new venv
    """

    return VirtualEnv.get_sys_path( self.exec )

  #-----------------------------------------------------------------------------
  @property
  def pip_version(self):
    """Version (major only) of pip currently installed in the virtual environment
    """

    return VirtualEnv.get_pip_version( self.exec )

  #-----------------------------------------------------------------------------
  def install( self, args, **kwargs ):
    with self._p_mutex:

      self.run_log([
          os.fspath(self.exec),
          '-m',
          'pip',
          'install',
          *args ],
        **kwargs )

  #-----------------------------------------------------------------------------
  async def trio_install( self, args, **kwargs ):

    async with self._p_mutex:

      await self.trio_run_log([
          os.fspath(self.exec),
          '-m',
          'pip',
          'install',
          *args ],
        **kwargs )
