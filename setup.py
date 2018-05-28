#!/usr/bin/env python

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools import Extension

import numpy

class custom_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)

        # Make sure that Numpy is importable
        # (does the same thing as setup_requires=['numpy'])
        self.distribution.fetch_build_eggs('numpy')
        # Prevent numpy from thinking it is still in its setup process:
        # See http://stackoverflow.com/questions/19919905
        from six.moves import builtins
        builtins.__NUMPY_SETUP__ = False

        # Add Numpy header search path path
        import numpy
        self.include_dirs.append(numpy.get_include())

    def run(self):
        # If we were asked to build any C/C++ libraries, add the directory
        # where we built them to the include path. (It's already on the library
        # path.)
        if self.distribution.has_c_libraries():
            self.run_command('build_clib')
            build_clib = self.get_finalized_command('build_clib')
            for key, value in build_clib.build_args.items():
                for ext in self.extensions:
                    if not hasattr(ext, key) or getattr(ext, key) is None:
                        setattr(ext, key, value)
                    else:
                        getattr(ext, key).extend(value)
        build_ext.run(self)

setup(name='healpylite',
      version="0.1",
      description='Healpix binning for Python',
      packages=['healpylite'],
      ext_modules=[
          Extension('healpylite._healpy_pixel_lib',
                    sources=['healpylite/src/_healpy_pixel_lib.cc'],
                    include_dirs=[numpy.get_include()],
                    language='c++'),
      ],
      install_requires=['numpy', 'six'],
      license='GPLv2',
      )
