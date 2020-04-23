import my_debugger

debugger = my_debugger.debugger()

# debugger.load("C:\\Windows\\System32\\calc.exe")

pid = input("输入进程号\n> ")
debugger.attach(int(pid))

printf_address = debugger.func_resolve("msvcrt.dll", "printf")
print("[*] 地址在：0x%08x" % printf_address)
debugger.bp_set(printf_address)
debugger.run()

# list = debugger.enumerate_threads()
#
# if list is not False:
#     for thread in list:
#         thread_context = debugger.get_thread_context(thread)
#
#         # 输出一些并不重要的信息
#         print("[*] 从线程号为 %0x%08x 的线程中取出来的寄存器值为" % thread)
#         print("[*] EIP: 0x%08x" % thread_context.Eip)
#         print("[*] ESP: 0x%08x" % thread_context.Esp)
#         print("[*] EBP: 0x%08x" % thread_context.Ebp)
#         print("[*] EAX: 0x%08x" % thread_context.Eax)
#         print("[*] EBX: 0x%08x" % thread_context.Ebx)
#         print("[*] ECX: 0x%08x" % thread_context.Ecx)
#         print("[*] EDX: 0x%08x" % thread_context.Edx)
#         print("[*] 结素惹~")

debugger.detach()
