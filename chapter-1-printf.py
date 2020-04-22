from ctypes import *

msvcrt = cdll.msvcrt
message = b"Hello, world!"
msvcrt.printf(b"Testing: %s\n", message)