# -*- coding: utf-8 -*-
"""CLI for running sphinx-build

.. code-block:: bash

  python -m doc -b html latexpdf

"""

import sys
import os
from pathlib import Path
import shutil
import re
import subprocess
import argparse
from argparse import RawTextHelpFormatter

from partis.pyproj import (
  norm_dist_name,
  join_dist_filename,
  dist_targz )

from partis.utils import caller_module

try:
  from importlib.metadata import metadata

except ImportError:
  from importlib_metadata import metadata

from .basic_conf import get_meta


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def basic_main(
  conf_dir,
  src_dir,
  root_dir,
  package = None,
  project = None,
  project_normed = None,
  project_filename = None,
  version = None ):
  """Convenience implementation of the ``__main__`` to build documentation and
  distribution file.


  Parameters
  ----------
  package : str
    Name of installed package to build documentation
  conf_dir : Path
    Directory where conf.py is located
  src_dir : Path
    Directory where 'index' document is located
  root_dir : Path
    Directory for root project

  Returns
  -------
  int
    returncode

  Example
  -------

  .. code-block:: python

  from partis.utils.sphinx import basic_main

  if __name__ == "__main__":

    src_dir = Path(__file__).parent
    root_dir = src_dir.parent

    basic_main(
      package = '...',
      conf_dir = src_dir,
      src_dir = src_dir,
      root_dir = root_dir)

  """

  if package:
    ( _project,
      _project_normed,
      _version,
      _description,
      _author,
      _email ) = get_meta(package)

    project = project or _project
    project_normed = project_normed or _project_normed
    version = version or _version

  project = project or root_doc
  project_normed = project_normed or project
  version = version or ''

  # for filenames etc., replace all non-word characters with underscores
  project_normed = re.sub(r'[^\w]+', '_', project_normed.strip() ).lstrip('_')

  if not project_filename:
    if version:
      project_filename = join_dist_filename( [project_normed, version] )
    else:
      project_filename = project_normed

  dist_name = project_filename
  doc_dist_name = dist_name + '-doc'
  doc_dist_file = doc_dist_name + '.tar.gz'
  pdf_name = dist_name + '.pdf'

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "-b", "--builder",
    type = str,
    nargs = '+',
    default = [ 'html' ],
    help = "builder to use passed to sphinx-build `-b` option. "
      "May give multiple builders to run in series." )

  parser.add_argument( "-o", "--outdir",
    type = Path,
    default = None,
    help = "Output directory" )

  parser.add_argument( "--no-dist",
    action = 'store_true',
    help = f"Do not create a documentation distribution: {doc_dist_file}" )

  args = parser.parse_args()

  root_dir = Path(root_dir)
  conf_dir = Path(conf_dir)
  src_dir = Path(src_dir)

  outdir = args.outdir or root_dir/'dist'
  outdir.mkdir(exist_ok = True)

  build_dir = root_dir/'build'
  build_dir.mkdir(exist_ok = True)

  doctrees = build_dir/'.doctrees'

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  builds = list()

  for builder in args.builder:
    post_cmd = None

    if builder == 'latexpdf':
      if shutil.which("pdflatex") is None:
        raise RuntimeError(f"Command not found 'pdflatex' needed for {builder}")

      elif os.name != 'nt' and shutil.which("latexmk") is None:
        # required to build on non-windows OS
        raise RuntimeError(f"Command not found 'latexmk' needed for {builder}")

      builder = 'latex'

      if sys.platform == 'win32':
        makecmd = os.environ.get('MAKE', 'make.bat')
      else:
        makecmd = os.environ.get('MAKE', 'make')

      post_cmd = [makecmd, 'all-pdf']

    print(f"Running sphinx-doc builder: {builder}\n")

    builder_dir = build_dir/builder
    builds.append((builder, builder_dir))

    cmd = [
      'python3',
      '-m',
      'sphinx.cmd.build',
      '-T',
      '-b',
      builder,
      str(src_dir),
      str(builder_dir),
      '-c',
      str(conf_dir) ]

    print('> ', ' '.join(cmd))
    subprocess.check_call(cmd)

    if post_cmd:
      print('> ', ' '.join(post_cmd))
      subprocess.check_call(post_cmd, cwd = builder_dir)

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  if not args.no_dist:

    print(f'Packaging documentation: {doc_dist_file}\n')

    with dist_targz(
      outname = doc_dist_file,
      outdir = outdir) as dist:

      for builder, builder_dir in builds:
        if builder == 'latexpdf':
          # only copy in the generated pdf
          dist.copyfile(
            src = build_dir/'latex'/pdf_name,
            dst = '/'.join([doc_dist_name, pdf_name]) )

          shutil.copyfile(
            build_dir/'latex'/pdf_name,
            outdir/pdf_name)

        else:
          dist.copytree(
            src = builder_dir,
            dst = '/'.join([doc_dist_name, builder]))

  return 0
