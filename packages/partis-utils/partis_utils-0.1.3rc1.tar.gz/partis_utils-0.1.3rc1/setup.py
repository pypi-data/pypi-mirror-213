"""Usage of `setup.py` is deprecated, and is supplied only for legacy installation.
"""
import sys
import os
import os.path as osp
from pathlib import (
  Path,
  PurePath,
  PurePosixPath)
import importlib
import logging
import argparse
import subprocess
import tempfile
from argparse import RawTextHelpFormatter
logger = logging.getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def egg_info( args ):

  logger.warning(
    "running legacy 'setup.py egg_info'" )

  dir = Path(args.egg_base).joinpath(EGG_INFO_NAME)

  if not dir.exists():
    dir.mkdir(parents=True, exist_ok = True)

  with open(dir.joinpath('PKG-INFO'), 'wb' ) as fp:  
    fp.write( PKG_INFO )

  with open( dir.joinpath('setup_requires.txt'), 'wb' ) as fp: 
    fp.write( b'' )

  with open( dir.joinpath('requires.txt'), 'wb' ) as fp: 
    fp.write( REQUIRES )

  with open( dir.joinpath('SOURCES.txt'), 'wb' ) as fp:
    fp.write( SOURCES )

  with open( dir.joinpath('top_level.txt'), 'wb' ) as fp:
    fp.write( TOP_LEVEL )

  with open( dir.joinpath('entry_points.txt'), 'wb' ) as fp:
    fp.write( ENTRY_POINTS )

  with open(dir.joinpath('dependency_links.txt'), 'wb' ) as fp:
    fp.write( b'' )

  with open( dir.joinpath('not-zip-safe'), 'wb' ) as fp:
    fp.write( b'' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bdist_wheel( args ):

  logger.warning(
    "running legacy 'setup.py bdist_wheel'" )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  backend.build_wheel(
    wheel_directory = args.dist_dir or args.bdist_dir or '.' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def install( args ):

  logger.warning(
    "running legacy 'setup.py install'" )

  reqs = [ f"{r}" for r in build_requires ]

  subprocess.check_call([
    sys.executable,
    '-m',
    'pip',
    'install',
    *reqs ] )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  with tempfile.TemporaryDirectory() as tmpdir:
    wheel_name = backend.build_wheel(
      wheel_directory = tmpdir )

    subprocess.check_call([
      sys.executable,
      '-m',
      'pip',
      'install',
      tmpdir.joinpath(wheel_name) ]) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dummy( args ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  logging.basicConfig(
    level = logging.INFO,
    format = "{name}:{levelname}: {message}",
    style = "{" )


  logger.warning(
    "'setup.py' is deprecated, limited support for legacy installs. Upgrade pip." )

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  subparsers = parser.add_subparsers()

  #.............................................................................
  egg_info_parser = subparsers.add_parser( 'egg_info' )

  egg_info_parser.set_defaults( func = egg_info )

  egg_info_parser.add_argument( "-e", "--egg-base",
    type = str,
    default = '.' )

  #.............................................................................
  bdist_wheel_parser = subparsers.add_parser( 'bdist_wheel' )

  bdist_wheel_parser.set_defaults( func = bdist_wheel )

  bdist_wheel_parser.add_argument( "-b", "--bdist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "-d", "--dist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "--python-tag",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--plat-name",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--py-limited-api",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--build-number",
    type = str,
    default = None )

  #.............................................................................
  install_parser = subparsers.add_parser( 'install' )

  install_parser.set_defaults( func = install )

  install_parser.add_argument( "--record",
    type = str,
    default = None )

  install_parser.add_argument( "--install-headers",
    type = str,
    default = None )

  install_parser.add_argument( "--compile",
    action='store_true' )

  install_parser.add_argument( "--single-version-externally-managed",
    action='store_true' )

  #.............................................................................
  clean_parser = subparsers.add_parser( 'clean' )

  clean_parser.set_defaults( func = dummy )

  clean_parser.add_argument( "-a", "--all",
    action='store_true' )

  args = parser.parse_args( )

  args.func( args )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE: these are templated literal values substituded by the backend when
# building the source distribution

build_backend = 'partis.pyproj.backend'
backend_path = None
build_requires = ['wheel', 'partis-pyproj>=0.1.3rc1']

EGG_INFO_NAME = 'partis-utils.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-utils\nVersion: 0.1.3rc1\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Collection of text and functional utilities\nLicense-File: LICENSE.txt\nClassifier: Programming Language :: Python :: 3\nClassifier: Operating System :: POSIX :: Linux\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Development Status :: 4 - Beta\nClassifier: Operating System :: Microsoft :: Windows\nClassifier: Programming Language :: Python\nClassifier: Topic :: Utilities\nClassifier: Intended Audience :: Developers\nProvides-Extra: doc\nProvides-Extra: lint\nProvides-Extra: asy\nProvides-Extra: theme\nProvides-Extra: sphinx\nRequires-Dist: psutil>=5.9.0\nRequires-Dist: typing_extensions~=4.4.0\nRequires-Dist: astunparse>=1.6.3; python_version < "3.9"\nRequires-Dist: get-annotations>=0.1.2; python_version < "3.10"\nRequires-Dist: rich==12.0.1; python_version < "3.6.3"\nRequires-Dist: importlib_metadata; python_version < "3.8"\nRequires-Dist: partis-pyproj>=0.1.3rc1\nRequires-Dist: rich>=12.5.1; python_version >= "3.6.3"\nRequires-Dist: typed-ast~=1.5.4; python_version < "3.8"\nRequires-Dist: wheel\nRequires-Dist: partis-utils[sphinx]>=0.1.3rc1; extra == "doc"\nRequires-Dist: typed-ast~=1.5.4; extra == "lint" and python_version < "3.8"\nRequires-Dist: pyflakes~=2.4.0; extra == "lint"\nRequires-Dist: trio==0.19.0; extra == "asy" and python_version < "3.7"\nRequires-Dist: trio==0.20.0; extra == "asy" and python_version >= "3.7"\nRequires-Dist: pygments~=2.14.0; extra == "theme"\nRequires-Dist: sphinxcontrib-bibtex~=2.5.0; extra == "sphinx"\nRequires-Dist: furo~=2022.12.7; extra == "sphinx"\nRequires-Dist: sphinx-paramlinks~=0.5.4; extra == "sphinx"\nRequires-Dist: sphinx~=5.3.0; extra == "sphinx"\nRequires-Dist: sphinx-design~=0.3.0; extra == "sphinx"\nRequires-Dist: sphinx-subfigure~=0.2.4; extra == "sphinx"\nRequires-Dist: partis-pyproj~=0.1.0; extra == "sphinx"\nRequires-Dist: sphinx_autodoc_typehints~=1.21.4; extra == "sphinx"\nRequires-Dist: pygments~=2.14.0; extra == "sphinx"\nRequires-Dist: sphinx-copybutton~=0.5.1; extra == "sphinx"\nRequires-Dist: sphinxcontrib-svg2pdfconverter[CairoSVG]~=1.2.2; extra == "sphinx"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.utils`` package contains a collection of text and functional utilities.\n\nhttps://nanohmics.bitbucket.io/doc/partis/utils'

REQUIRES = b'psutil>=5.9.0\ntyping_extensions~=4.4.0\nastunparse>=1.6.3; python_version < "3.9"\nget-annotations>=0.1.2; python_version < "3.10"\nrich==12.0.1; python_version < "3.6.3"\nimportlib_metadata; python_version < "3.8"\npartis-pyproj>=0.1.3rc1\nrich>=12.5.1; python_version >= "3.6.3"\ntyped-ast~=1.5.4; python_version < "3.8"\nwheel\npartis-utils[sphinx]>=0.1.3rc1; extra == "doc"\ntyped-ast~=1.5.4; extra == "lint" and python_version < "3.8"\npyflakes~=2.4.0; extra == "lint"\ntrio==0.19.0; extra == "asy" and python_version < "3.7"\ntrio==0.20.0; extra == "asy" and python_version >= "3.7"\npygments~=2.14.0; extra == "theme"\nsphinxcontrib-bibtex~=2.5.0; extra == "sphinx"\nfuro~=2022.12.7; extra == "sphinx"\nsphinx-paramlinks~=0.5.4; extra == "sphinx"\nsphinx~=5.3.0; extra == "sphinx"\nsphinx-design~=0.3.0; extra == "sphinx"\nsphinx-subfigure~=0.2.4; extra == "sphinx"\npartis-pyproj~=0.1.0; extra == "sphinx"\nsphinx_autodoc_typehints~=1.21.4; extra == "sphinx"\npygments~=2.14.0; extra == "sphinx"\nsphinx-copybutton~=0.5.1; extra == "sphinx"\nsphinxcontrib-svg2pdfconverter[CairoSVG]~=1.2.2; extra == "sphinx"'

SOURCES = b'partis_utils-0.1.3rc1/src/utils/__init__.py\npartis_utils-0.1.3rc1/src/utils/lint.py\npartis_utils-0.1.3rc1/src/utils/valid.py\npartis_utils-0.1.3rc1/src/utils/mem.py\npartis_utils-0.1.3rc1/src/utils/module.py\npartis_utils-0.1.3rc1/src/utils/file.py\npartis_utils-0.1.3rc1/src/utils/hint.py\npartis_utils-0.1.3rc1/src/utils/mutex_file.py\npartis_utils-0.1.3rc1/src/utils/property.py\npartis_utils-0.1.3rc1/src/utils/similarity.py\npartis_utils-0.1.3rc1/src/utils/log.py\npartis_utils-0.1.3rc1/src/utils/sphinx/__init__.py\npartis_utils-0.1.3rc1/src/utils/sphinx/basic_main.py\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/theme_patch.js\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/tex-chtml-full-min.js\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/tex-chtml-full-min.js.LICENSE.txt\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/3.2.2\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Zero.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Typewriter-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_SansSerif-Bold.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Size1-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_AMS-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Math-Italic.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Vector-Bold.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Main-Bold.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Size2-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Vector-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Main-Italic.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Math-BoldItalic.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Math-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_SansSerif-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Calligraphic-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Calligraphic-Bold.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_SansSerif-Italic.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Script-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Fraktur-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Main-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Size3-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Fraktur-Bold.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax/output/chtml/fonts/woff-v2/MathJax_Size4-Regular.woff\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/tables.css\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/app_icon.svg\npartis_utils-0.1.3rc1/src/utils/sphinx/_static/mathjax_config.js_t\npartis_utils-0.1.3rc1/src/utils/sphinx/_templates/base.html\npartis_utils-0.1.3rc1/src/utils/sphinx/basic_pdf.py\npartis_utils-0.1.3rc1/src/utils/sphinx/ext.py\npartis_utils-0.1.3rc1/src/utils/sphinx/basic_conf.py\npartis_utils-0.1.3rc1/src/utils/fmt_doc.py\npartis_utils-0.1.3rc1/src/utils/sig.py\npartis_utils-0.1.3rc1/src/utils/plugin.py\npartis_utils-0.1.3rc1/src/utils/fmt.py\npartis_utils-0.1.3rc1/src/utils/typing.py\npartis_utils-0.1.3rc1/src/utils/data.py\npartis_utils-0.1.3rc1/src/utils/time.py\npartis_utils-0.1.3rc1/src/utils/async_trio/__init__.py\npartis_utils-0.1.3rc1/src/utils/async_trio/async_trio.py\npartis_utils-0.1.3rc1/src/utils/venv.py\npartis_utils-0.1.3rc1/src/utils/ast.py\npartis_utils-0.1.3rc1/src/utils/theme/pygments_light.py\npartis_utils-0.1.3rc1/src/utils/theme/pygments_dark.py\npartis_utils-0.1.3rc1/src/utils/special.py\npartis_utils-0.1.3rc1/src/utils/inspect.py\npartis_utils-0.1.3rc1/doc/conf.py\npartis_utils-0.1.3rc1/doc/__init__.py\npartis_utils-0.1.3rc1/doc/index.rst\npartis_utils-0.1.3rc1/doc/src/mem.rst\npartis_utils-0.1.3rc1/doc/src/module.rst\npartis_utils-0.1.3rc1/doc/src/index.rst\npartis_utils-0.1.3rc1/doc/src/inspect.rst\npartis_utils-0.1.3rc1/doc/src/hint.rst\npartis_utils-0.1.3rc1/doc/src/data.rst\npartis_utils-0.1.3rc1/doc/src/fmt.rst\npartis_utils-0.1.3rc1/doc/src/valid.rst\npartis_utils-0.1.3rc1/doc/src/special.rst\npartis_utils-0.1.3rc1/doc/src/log.rst\npartis_utils-0.1.3rc1/doc/src/mutex_file.rst\npartis_utils-0.1.3rc1/doc/src/venv.rst\npartis_utils-0.1.3rc1/doc/src/plugin.rst\npartis_utils-0.1.3rc1/doc/__main__.py\npartis_utils-0.1.3rc1/doc/sphinx.rst\npartis_utils-0.1.3rc1/doc/img/C.png\npartis_utils-0.1.3rc1/doc/img/A.png\npartis_utils-0.1.3rc1/doc/img/B.png\npartis_utils-0.1.3rc1/test/100_utils/__init__.py\npartis_utils-0.1.3rc1/test/100_utils/test_venv.py\npartis_utils-0.1.3rc1/test/100_utils/test_hint.py\npartis_utils-0.1.3rc1/test/100_utils/test_fmt.py\npartis_utils-0.1.3rc1/pyproject.toml\npartis_utils-0.1.3rc1/LICENSE.txt\npartis_utils-0.1.3rc1/README.rst'

TOP_LEVEL = b''

ENTRY_POINTS = b''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
