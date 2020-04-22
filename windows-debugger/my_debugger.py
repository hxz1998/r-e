from my_debugger_defines import *

kernel32 = windll.kernel32


class debugger():
    def __init__(self):
        pass

    def load(self, path_to_exec):
        """参数 dwCreationFlags 中的标志位控制着进程的创建方式
        如果希望新创建的进程独占一格控制台窗口，那么可加上标志位 CREATE_NEW_CONSOLE
        """
        creation_flags = DEBUG_PROCESS

        # 实例化结构体
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        # 在以下两个成员变量的共同作用下，新建进程将在一个单独的窗体中显示
        # 通过改变结构体 STARTUPINFO 中的成员变量来控制 debugger 的行为
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        # 设置结构体 STARTUPINFO 中的成员变量 cb 的值，用以表示结构体本身大小
        startupinfo.cb = sizeof(startupinfo)

        # fixed：0x000003e6 错误
        # https://stackoverflow.com/questions/53139186/why-python-kernel32-createprocessa-get-error-0x000003e6
        # LPSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)
        # LPSTARTUPINFOW = POINTER(STARTUPINFO)
        # LPPROCESS_INFORMATION = POINTER(PROCESS_INFORMATION)
        # kernel32 = WinDLL('kernel32', use_last_error=True)
        # kernel32.CreateProcessW.argtypes = (LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES,
        #                                     BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION)
        # kernel32.restype = BOOL

        if kernel32.CreateProcessW(path_to_exec, None, None, None, False, creation_flags, None, None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print('[*] Process launched')
            print('[*] 创建成功了进程（process），系统分配的进程号 PID: {}'.format(process_information.dwProcessId))
        else:
            print("[*] 错误惹！＞﹏＜：0x%08x." % kernel32.GetLastError())
