from ctypes import *

from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR, LPCWSTR, HANDLE, LPVOID, BOOL

LPBYTE = POINTER(BYTE)

# 为 ctype 变量创建符合匈牙利命名风格的匿名，这样可以使得代码更接近于Win32风格，
# 不过事后验证并不需要这样做，直接使用ctypes.wintypes里面定义好的就行惹

# WORD = c_ushort
# DWORD = c_long
# LPBYTE = POINTER(c_ubyte)
# LPTSTR = POINTER(c_char)
# HANDLE = c_void_p

# 常值定义
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010


# 定义函数CreateProcessW()所用到的结构体
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPWSTR),
        ("lpDesktop", LPWSTR),
        ("lpTitle", LPWSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFilgs", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE)
    ]


class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD)
    ]


class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [('nLength', DWORD),
                ('lpSecurityDescriptor', LPVOID),
                ('bInheritHandle', BOOL)]
