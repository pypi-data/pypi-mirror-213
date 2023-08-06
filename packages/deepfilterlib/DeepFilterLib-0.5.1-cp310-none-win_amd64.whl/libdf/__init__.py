

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_7():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'DeepFilterLib.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_3_7()
del _delvewheel_init_patch_1_3_7
# end delvewheel patch

from .libdf import *

__doc__ = libdf.__doc__
if hasattr(libdf, "__all__"):
    __all__ = libdf.__all__