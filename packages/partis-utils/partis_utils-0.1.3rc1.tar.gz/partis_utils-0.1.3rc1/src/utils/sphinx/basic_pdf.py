# -*- coding: utf-8 -*-
"""
"""

import sys
import os
import os.path as osp
import re
import subprocess
import shutil
from glob import glob
import tempfile
import json

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
CONF_TMPL = """
from partis.utils.sphinx import basic_conf

globals().update( basic_conf(**{} ) )
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def basic_pdf(file, out_dir, **kwargs):

  builder = 'latexpdf'

  with tempfile.TemporaryDirectory() as dir:
    conf_dir = osp.join(dir, 'conf')
    src_dir = conf_dir
    build_dir = osp.join(dir, 'build')

    os.makedirs(conf_dir)
    os.makedirs(build_dir)
    fname = osp.basename(file)
    name, ext = osp.splitext(fname)
    # kwargs.setdefault('root_doc', name)

    if 'package' not in kwargs and 'project_filename' not in kwargs:
      kwargs.setdefault('project_filename', name)

    _file = osp.join(conf_dir, 'index.rst')
    shutil.copyfile(file, _file)

    with open(osp.join(conf_dir, 'conf.py'), 'w') as fp:
      fp.write(CONF_TMPL.format(str(kwargs)))

    subprocess.check_call([
      'python3',
      '-m',
      'sphinx.cmd.build',
      '-M',
      builder,
      src_dir,
      build_dir,
      '-c',
      conf_dir ])

    pattern = osp.join(build_dir, 'latex', '*.pdf')
    print(f"Copying generated file: {pattern}")

    for file in glob(pattern):
      _file = osp.join(out_dir, osp.basename(file))
      print(f"{file} -> {_file}")

      shutil.copyfile(file, _file)

