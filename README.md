# healpylite

HEALpix binning is often useful, but [healpy](https://healpy.readthedocs.io/en/latest/) pulls in
all of matplotlib. healpylite replaces _only_ healpy.pixelfunc, backed by a stripped-down build
of healpix-cxx.

healpy-lite contains components of healpy, healpix-cxx, and cxxsupport