from ctypes import *
import time

msvcrt = cdll.msvcrt

counter = 0

while True:
    msvcrt.printf(b"Testing: %d\n", counter)
    counter += 1