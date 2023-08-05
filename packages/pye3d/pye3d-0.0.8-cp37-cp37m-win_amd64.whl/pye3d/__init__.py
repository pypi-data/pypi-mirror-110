

""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_12():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pye3d.libs'))
    if sys.version_info[:2] >= (3, 8):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-pye3d-0.0.8')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_12()
del _delvewheel_init_patch_0_0_12
# end delvewheel patch

__version__ = "0.0.8"
