# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

# This file can be modified by setup.py when building a manylinux2010 wheel
# When modified, it will preload some libraries needed for the python C extension
from ctypes import CDLL, RTLD_GLOBAL
_libascendcl = CDLL("libascendcl.so", mode=RTLD_GLOBAL)
_libacl_op_compiler = CDLL("libacl_op_compiler.so", mode=RTLD_GLOBAL)
_libfmk_onnx_parser = CDLL("libfmk_onnx_parser.so", mode=RTLD_GLOBAL)
