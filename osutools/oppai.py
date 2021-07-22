import sys
import pkg_resources
import tempfile
import urllib.request
import os
import platform
import pathlib
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
    dll = CDLL(pkg_resources.resource_filename("osutools", f"oppai_files/{filename}"))
    dll.ezpp_new.restype = c_void_p
    dll.ezpp_set_mods.argtypes = (c_void_p, c_int)
    dll.ezpp_set_combo.argtypes = (c_void_p, c_int)
    dll.ezpp_set_nmiss.argtypes = (c_void_p, c_int)
    dll.ezpp_set_accuracy.argtypes = (c_void_p, c_int, c_int)
    dll.ezpp_set_accuracy_percent.argtypes = (c_void_p, c_float)
    dll.ezpp.argtypes = (c_void_p, c_char_p)
    dll.ezpp_pp.argtypes = (c_void_p,)
    dll.ezpp_pp.restype = c_float

    @classmethod
    def calculate_pp_from_url(
        cls,
        url,
        mods=0,
        max_combo=None,
        misses=None,
        num_100=None,
        num_50=None,
        accuracy=None,
    ):
        temp_map = tempfile.NamedTemporaryFile(delete=False)
        temp_map.write(urllib.request.urlopen(url).read())
        temp_map.close()
        pp = cls.calculate_pp(
            temp_map.name,
            mods=mods,
            max_combo=max_combo,
            misses=misses,
            num_100=num_100,
            num_50=num_50,
            accuracy=accuracy,
        )
        os.remove(temp_map.name)
        return pp

    @classmethod
    def calculate_pp(
        cls,
        filename,
        mods=0,
        max_combo=None,
        misses=None,
        num_100=None,
        num_50=None,
        accuracy=None,
    ):
        ez = Oppai.dll.ezpp_new()
        cls.dll.ezpp_set_mods(ez, mods)
        if max_combo is not None:
            cls.dll.ezpp_set_combo(ez, max_combo)
        if misses is not None:
            cls.dll.ezpp_set_nmiss(ez, misses)
        if accuracy is not None:
            cls.dll.ezpp_set_accuracy_percent(ez, accuracy)
        elif num_100 is not None and num_50 is not None:
            cls.dll.ezpp_set_accuracy(ez, num_100, num_50)
        cls.dll.ezpp(ez, str(filename).encode())
        pp_out = cls.dll.ezpp_pp(ez)
        return pp_out
