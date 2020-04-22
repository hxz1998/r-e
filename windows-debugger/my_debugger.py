from my_debugger_defines import *

kernel32 = windll.kernel32


class debugger():
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False
        self.h_thread = None
        self.context = None
        self.exception = None
        self.exception_address = 0

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

            # 保存一个指向新建进程的有效句柄，以供后续使用
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print("[*] 错误惹！＞﹏＜：0x%08x." % kernel32.GetLastError())

    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)

        # 尝试附加到目标进程，如果失败则输出提示信息
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            # self.run()
            print("[*] 附加 %d 进程成功" % pid)
        else:
            print("[*] 附加进程失败惹！")

    def run(self):
        # 静静等待发生在 debugger 进程中的调试事件
        while self.debugger_active == True:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # 先简单恢复目标进程的执行，下面注释掉的这两行程序能把目标程序挂起（点不动了）
            # input("按任意键继续……")
            # self.debugger_active = False

            # 获取到线程的句柄并且
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(self.h_thread)
            print("事件码：%d 线程码：%d" % (debug_event.dwDebugEventCode, debug_event.dwThreadId))

            # 如果事件码显示这是一个异常事件，那么进一步检测确切的类型
            exception = None
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                # 获取异常代码
                exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress
            if exception == EXCEPTION_ACCESS_VIOLATION:
                print("权限非法检测到了~")
            elif exception == EXCEPTION_BREAKPOINT:
                continue_status = self.exception_handler_breakpoint()
            elif exception == EXCEPTION_GUARD_PAGE:
                print("注意！页权限检测到了~")
            elif exception == EXCEPTION_SINGLE_STEP:
                print("单步运行中...")
            kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status)

    def exception_handler_breakpoint(self):
        print("[*] 进来了断点处理器")
        print("[*] 异常地址：0x%08x" % self.exception_address)
        return DBG_CONTINUE

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] 终止调试，正在退出...")
            return True
        else:
            print("这里有一些问题粗乃惹！")
            return False

    def open_thread(self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)
        if h_thread is not None:
            return h_thread
        else:
            print("[*] 好像并不能获取到线程句柄哎~＞︿＜")

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:
            # 首先需要正确设置结构体大小，否则会调用失败
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                    success = kernel32.Thread32Next(snapshot, byref(thread_entry))
                    kernel32.CloseHandle(snapshot)
                    return thread_list
                else:
                    print("[*] 所属的进程ID为: %d" % thread_entry.th32OwnerProcessID)
                    return False

    def get_thread_context(self, thread_id=None, h_thread=None):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        h_thread = self.open_thread(thread_id=thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False
