import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import autodox
from autodox import dox_a_module
from tapescript import functions


options = {'exclude_names': ['VerifyKey', 'BadSignatureError', 'Tape']}
print(dox_a_module(functions, options))
