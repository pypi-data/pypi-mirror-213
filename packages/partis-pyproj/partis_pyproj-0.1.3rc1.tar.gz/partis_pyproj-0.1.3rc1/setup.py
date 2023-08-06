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

build_backend = 'pyproj.backend'
backend_path = ['src']
build_requires = ['wheel', 'tomli>=1.2.3', 'packaging==21.3', 'importlib_metadata; python_version < "3.8"']

EGG_INFO_NAME = 'partis-pyproj.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-pyproj\nVersion: 0.1.3rc1\nRequires-Python: >=3.6.2\nAuthor-email: "Nanohmics Inc." <software.support@nanohmics.com>\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Minimal set of Python project utilities (PEP-517/621)\nLicense-File: LICENSE.txt\nClassifier: Topic :: Software Development :: Build Tools\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Programming Language :: Python\nClassifier: Operating System :: POSIX :: Linux\nClassifier: Development Status :: 4 - Beta\nClassifier: Intended Audience :: Developers\nClassifier: Programming Language :: Python :: 3\nClassifier: Operating System :: Microsoft :: Windows\nProvides-Extra: meson\nProvides-Extra: cmake\nProvides-Extra: doc\nProvides-Extra: test\nProvides-Extra: cov\nProvides-Extra: lint\nRequires-Dist: tomli>=1.2.3\nRequires-Dist: packaging==21.3\nRequires-Dist: importlib_metadata; python_version < "3.8"\nRequires-Dist: wheel\nRequires-Dist: meson>=0.61.3; extra == "meson"\nRequires-Dist: ninja>=1.10.2.3; extra == "meson"\nRequires-Dist: ninja>=1.10.2.3; extra == "cmake"\nRequires-Dist: cmake>=3.24.3; extra == "cmake"\nRequires-Dist: partis-utils[sphinx]>=0.1.3rc1; extra == "doc"\nRequires-Dist: meson>=0.61.3; extra == "test"\nRequires-Dist: numpy; extra == "test"\nRequires-Dist: pip>=18.1; extra == "test"\nRequires-Dist: coverage[toml]>=6.2; extra == "test"\nRequires-Dist: nox>=2021.10.1; extra == "test"\nRequires-Dist: tomli>=1.2.3; extra == "test"\nRequires-Dist: cmake>=3.24.3; extra == "test"\nRequires-Dist: Cython>=0.29.18; extra == "test"\nRequires-Dist: ninja>=1.10.2.3; extra == "test"\nRequires-Dist: pytest_mock>=3.6.1; extra == "test"\nRequires-Dist: build>=0.7.0; extra == "test"\nRequires-Dist: pytest>=6.2.5; extra == "test"\nRequires-Dist: pytest-cov>=3.0.0; extra == "test"\nRequires-Dist: coverage[toml]>=6.2; extra == "cov"\nRequires-Dist: pyflakes==2.4.0; extra == "lint"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.pyproj`` package aims to be very simple and\ntransparent implementation of a PEP-517 build back-end.\n\nhttps://nanohmics.bitbucket.io/doc/partis/pyproj'

REQUIRES = b'tomli>=1.2.3\npackaging==21.3\nimportlib_metadata; python_version < "3.8"\nwheel\nmeson>=0.61.3; extra == "meson"\nninja>=1.10.2.3; extra == "meson"\nninja>=1.10.2.3; extra == "cmake"\ncmake>=3.24.3; extra == "cmake"\npartis-utils[sphinx]>=0.1.3rc1; extra == "doc"\nmeson>=0.61.3; extra == "test"\nnumpy; extra == "test"\npip>=18.1; extra == "test"\ncoverage[toml]>=6.2; extra == "test"\nnox>=2021.10.1; extra == "test"\ntomli>=1.2.3; extra == "test"\ncmake>=3.24.3; extra == "test"\nCython>=0.29.18; extra == "test"\nninja>=1.10.2.3; extra == "test"\npytest_mock>=3.6.1; extra == "test"\nbuild>=0.7.0; extra == "test"\npytest>=6.2.5; extra == "test"\npytest-cov>=3.0.0; extra == "test"\ncoverage[toml]>=6.2; extra == "cov"\npyflakes==2.4.0; extra == "lint"'

SOURCES = b'partis_pyproj-0.1.3rc1/src/pyproj/__init__.py\npartis_pyproj-0.1.3rc1/src/pyproj/norms.py\npartis_pyproj-0.1.3rc1/src/pyproj/pep.py\npartis_pyproj-0.1.3rc1/src/pyproj/builder/__init__.py\npartis_pyproj-0.1.3rc1/src/pyproj/builder/builder.py\npartis_pyproj-0.1.3rc1/src/pyproj/builder/cargo.py\npartis_pyproj-0.1.3rc1/src/pyproj/builder/cmake.py\npartis_pyproj-0.1.3rc1/src/pyproj/builder/meson.py\npartis_pyproj-0.1.3rc1/src/pyproj/builder/process.py\npartis_pyproj-0.1.3rc1/src/pyproj/load_module.py\npartis_pyproj-0.1.3rc1/src/pyproj/_legacy_setup.py\npartis_pyproj-0.1.3rc1/src/pyproj/_nonprintable.py\npartis_pyproj-0.1.3rc1/src/pyproj/path/__init__.py\npartis_pyproj-0.1.3rc1/src/pyproj/path/match.py\npartis_pyproj-0.1.3rc1/src/pyproj/path/pattern.py\npartis_pyproj-0.1.3rc1/src/pyproj/path/utils.py\npartis_pyproj-0.1.3rc1/src/pyproj/validate.py\npartis_pyproj-0.1.3rc1/src/pyproj/pkginfo.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/dist_targz.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/__init__.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/dist_zip.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/dist_binary.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/dist_base.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/dist_source.py\npartis_pyproj-0.1.3rc1/src/pyproj/dist_file/dist_copy.py\npartis_pyproj-0.1.3rc1/src/pyproj/legacy.py\npartis_pyproj-0.1.3rc1/src/pyproj/backend.py\npartis_pyproj-0.1.3rc1/src/pyproj/pyproj.py\npartis_pyproj-0.1.3rc1/src/pyproj/pptoml.py\npartis_pyproj-0.1.3rc1/doc/conf.py\npartis_pyproj-0.1.3rc1/doc/__init__.py\npartis_pyproj-0.1.3rc1/doc/index.rst\npartis_pyproj-0.1.3rc1/doc/src/pptoml.rst\npartis_pyproj-0.1.3rc1/doc/src/index.rst\npartis_pyproj-0.1.3rc1/doc/src/backend.rst\npartis_pyproj-0.1.3rc1/doc/src/builder.rst\npartis_pyproj-0.1.3rc1/doc/src/validate.rst\npartis_pyproj-0.1.3rc1/doc/src/pkginfo.rst\npartis_pyproj-0.1.3rc1/doc/src/pyproj.rst\npartis_pyproj-0.1.3rc1/doc/src/path.rst\npartis_pyproj-0.1.3rc1/doc/src/pep.rst\npartis_pyproj-0.1.3rc1/doc/src/load_module.rst\npartis_pyproj-0.1.3rc1/doc/src/norms.rst\npartis_pyproj-0.1.3rc1/doc/src/dist_file.rst\npartis_pyproj-0.1.3rc1/doc/__main__.py\npartis_pyproj-0.1.3rc1/doc/glossary.rst\npartis_pyproj-0.1.3rc1/test/pkg_bad_5/src/test_pkg/sub_mod/sub_sub_mod/good_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_5/src/test_pkg/sub_mod/sub_sub_mod/bad_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_5/src/test_pkg/pure_mod/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_5/pkgaux/__init__.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_5/pyproject.toml\npartis_pyproj-0.1.3rc1/test/__init__.py\npartis_pyproj-0.1.3rc1/test/pkg_meson_2/src/test_pkg/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_meson_2/src/test_pkg/plat_mod.pyx\npartis_pyproj-0.1.3rc1/test/pkg_meson_2/meson.build\npartis_pyproj-0.1.3rc1/test/pkg_meson_2/meson_options.txt\npartis_pyproj-0.1.3rc1/test/pkg_meson_2/pyproject.toml\npartis_pyproj-0.1.3rc1/test/pkg_bad_2/src/test_pkg/sub_mod/sub_sub_mod/good_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_2/src/test_pkg/sub_mod/sub_sub_mod/bad_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_2/src/test_pkg/pure_mod/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_2/pkgaux/__init__.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_2/pyproject.toml\npartis_pyproj-0.1.3rc1/test/__main__.py\npartis_pyproj-0.1.3rc1/test/test_03_dist.py\npartis_pyproj-0.1.3rc1/test/sitecustom/partis-sitecustom.pth\npartis_pyproj-0.1.3rc1/test/sitecustom/pyproject.toml\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/bad_link/src/test_pkg/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/bad_link/src/test_pkg/plat_mod.pyx\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/bad_link/meson.build\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/bad_link/meson_options.txt\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/bad_link/pyproject.toml\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/src/test_pkg/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/src/test_pkg/plat_mod.pyx\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/meson.build\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/meson_options.txt\npartis_pyproj-0.1.3rc1/test/pkg_meson_bad_1/pyproject.toml\npartis_pyproj-0.1.3rc1/test/pkg_min/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_min/pyproject.toml\npartis_pyproj-0.1.3rc1/test/noxfile.py\npartis_pyproj-0.1.3rc1/test/test_00_validate.py\npartis_pyproj-0.1.3rc1/test/test_04_load_module.py\npartis_pyproj-0.1.3rc1/test/pkg_cmake_1/src/test_pkg/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_cmake_1/src/test_pkg/plat_mod.pyx\npartis_pyproj-0.1.3rc1/test/pkg_cmake_1/src/test_pkg/CMakeLists.txt\npartis_pyproj-0.1.3rc1/test/pkg_cmake_1/CMakeLists.txt\npartis_pyproj-0.1.3rc1/test/pkg_cmake_1/pyproject.toml\npartis_pyproj-0.1.3rc1/test/test_01_norms.py\npartis_pyproj-0.1.3rc1/test/test_05_pkginfo.py\npartis_pyproj-0.1.3rc1/test/pkg_base/src/test_pkg/sub_mod/sub_sub_mod/good_file.py\npartis_pyproj-0.1.3rc1/test/pkg_base/src/test_pkg/sub_mod/sub_sub_mod/bad_file.py\npartis_pyproj-0.1.3rc1/test/pkg_base/src/test_pkg/sub_mod/good_file.py\npartis_pyproj-0.1.3rc1/test/pkg_base/src/test_pkg/sub_mod/bad_file.py\npartis_pyproj-0.1.3rc1/test/pkg_base/src/test_pkg/pure_mod/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_base/pkgaux/__init__.py\npartis_pyproj-0.1.3rc1/test/pkg_base/pyproject.toml\npartis_pyproj-0.1.3rc1/test/test_06_pyproj.py\npartis_pyproj-0.1.3rc1/test/test_02_path.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_3/pyproject.toml\npartis_pyproj-0.1.3rc1/test/pkg_meson_1/src/test_pkg/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_meson_1/src/test_pkg/plat_mod.pyx\npartis_pyproj-0.1.3rc1/test/pkg_meson_1/meson.build\npartis_pyproj-0.1.3rc1/test/pkg_meson_1/meson_options.txt\npartis_pyproj-0.1.3rc1/test/pkg_meson_1/pyproject.toml\npartis_pyproj-0.1.3rc1/test/test_07_backend.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_4/src/test_pkg/sub_mod/sub_sub_mod/good_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_4/src/test_pkg/sub_mod/sub_sub_mod/bad_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_4/src/test_pkg/pure_mod/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_4/pkgaux/__init__.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_4/pyproject.toml\npartis_pyproj-0.1.3rc1/test/pkg_bad_1/src/test_pkg/sub_mod/sub_sub_mod/good_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_1/src/test_pkg/sub_mod/sub_sub_mod/bad_file.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_1/src/test_pkg/pure_mod/pure_mod.py\npartis_pyproj-0.1.3rc1/test/pkg_bad_1/pyproject.toml\npartis_pyproj-0.1.3rc1/pyproject.toml\npartis_pyproj-0.1.3rc1/LICENSE.txt\npartis_pyproj-0.1.3rc1/README.rst'

TOP_LEVEL = b''

ENTRY_POINTS = b''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
