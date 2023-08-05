"""Installation file for ansys-mapdl-reader"""
import os
import sys
from io import open as io_open

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

try:
    import numpy as np
except ImportError:
    raise Exception('Please install numpy first with "pip install numpy"')


def check_cython():
    """Check if binaries exist and if not check if Cython is installed"""
    has_binary_reader = False
    for filename in os.listdir('ansys/mapdl/reader'):
        if '_binary_reader' in filename:
            has_binary_reader = True

    if not has_binary_reader:
        # ensure cython is installed before trying to build
        try:
            import cython
        except ImportError:
            raise ImportError('\n\n\nTo build pyansys please install Cython with:\n\n'
                              'pip install cython\n\n') from None


check_cython()


class build_ext(_build_ext):
    """ build class that includes numpy directory """
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


def compilerName():
    """ Check compiler and assign compile arguments accordingly """
    import re
    import distutils.ccompiler
    comp = distutils.ccompiler.get_default_compiler()
    getnext = False

    for a in sys.argv[2:]:
        if getnext:
            comp = a
            getnext = False
            continue
        # separated by space
        if a == '--compiler' or re.search('^-[a-z]*c$', a):
            getnext = True
            continue
        # without space
        m = re.search('^--compiler=(.+)', a)
        if m is None:
            m = re.search('^-[a-z]*c(.+)', a)
            if m:
                comp = m.group(1)

    return comp


# Assign arguments based on compiler
compiler = compilerName()
if compiler == 'unix':
    cmp_arg = ['-O3', '-w']
else:
    cmp_arg = ['/Ox', '-w']


# Get version from version info
__version__ = None
this_file = os.path.dirname(__file__)
version_file = os.path.join(this_file, 'ansys', 'mapdl', 'reader', '_version.py')
with io_open(version_file, mode='r') as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = ['numpy>=1.14.0',
                    'pyvista>=0.30.1',
                    'appdirs>=1.4.0',
                    'matplotlib>=3.0.0',
                    'tqdm>=4.45.0']


# Actual setup
setup(
    name='ansys-mapdl-reader',
    packages=['ansys.mapdl.reader', 'ansys.mapdl.reader.examples'],
    version=__version__,
    description='Pythonic interface to files generated by MAPDL',
    long_description=open('README.rst').read(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    url='https://github.com/pyansys/pymapdl-reader',

    # Build cython modules
    cmdclass={'build_ext': build_ext},
    ext_modules=[
                 Extension('ansys.mapdl.reader._archive',
                           ['ansys/mapdl/reader/cython/_archive.pyx',
                            'ansys/mapdl/reader/cython/archive.c'],
                           extra_compile_args=cmp_arg,
                           language='c',),

                 Extension('ansys.mapdl.reader._reader',
                           ['ansys/mapdl/reader/cython/_reader.pyx',
                            'ansys/mapdl/reader/cython/reader.c',
                            'ansys/mapdl/reader/cython/vtk_support.c'],
                           extra_compile_args=cmp_arg,
                           language='c',),

                 Extension("ansys.mapdl.reader._relaxmidside",
                           ["ansys/mapdl/reader/cython/_relaxmidside.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension("ansys.mapdl.reader._cellqual",
                           ["ansys/mapdl/reader/cython/_cellqual.pyx"],
                           extra_compile_args=cmp_arg,
                           language='c'),

                 Extension("ansys.mapdl.reader._binary_reader",
                           ["ansys/mapdl/reader/cython/_binary_reader.pyx",
                            "ansys/mapdl/reader/cython/binary_reader.cpp"],
                           extra_compile_args=cmp_arg,
                           language='c++'),
                 ],

    python_requires='>=3.6.*',
    keywords='vtk MAPDL ANSYS cdb full rst',
    package_data={'ansys.mapdl.reader.examples': ['TetBeam.cdb',
                                                  'HexBeam.cdb',
                                                  'file.rst',
                                                  'file.full',
                                                  'sector.rst',
                                                  'sector.cdb']},
    install_requires=install_requires,
)
