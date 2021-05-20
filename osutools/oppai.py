import sys
import pathlib
import platform
from ctypes import *


# If you're using this on its own make sure it has oppai_files dir in the same directory
class Oppai:
    is_64bits = sys.maxsize > 2 ** 32
    is_windows = platform.system() == "Windows"
    if is_64bits and is_windows:
        filename = "oppai.dll"
    elif not is_64bits and is_windows:
        filename = "oppai32.dll"
    elif is_64bits and not is_windows:
        filename = "liboppai.so"
    else:
        filename = "liboppaii686.so"
    path = pathlib.Path(__file__).parent / "oppai_files" / filename
    dll = CDLL(str(path))
    dll.ezpp_new.restype = c_void_p
    dll.ezpp_set_mods.argtypes = (c_void_p, c_int)
    dll.ezpp_set_combo.argtypes = (c_void_p, c_int)
    dll.ezpp_set_nmiss.argtypes = (c_void_p, c_int)
    dll.ezpp_set_accuracy.argtypes = (c_void_p, c_int, c_int)
    dll.ezpp.argtypes = (c_void_p, c_char_p)
    dll.ezpp_pp.argtypes = (c_void_p,)
    dll.ezpp_pp.restype = c_float

    @classmethod
    def calculate_pp(cls, filename, mods=0, max_combo=None, misses=None, num_100=None, num_50=None):
        ez = Oppai.dll.ezpp_new()
        cls.dll.ezpp_set_mods(ez, mods)
        if max_combo is not None:
            cls.dll.ezpp_set_combo(ez, max_combo)
        if misses is not None:
            cls.dll.ezpp_set_nmiss(ez, misses)
        if num_100 is not None and num_50 is not None:
            cls.dll.ezpp_set_accuracy(ez, num_100, num_50)
        cls.dll.ezpp(ez, filename.encode())
        pp_out = cls.dll.ezpp_pp(ez)
        return pp_out


