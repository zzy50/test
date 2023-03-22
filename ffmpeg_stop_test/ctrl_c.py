import ctypes
import sys

kernel = ctypes.windll.kernel32

pid = int(sys.argv[1])
print(f"Send Ctrl+C to pid: {pid}")
kernel.FreeConsole()
kernel.AttachConsole(pid)
kernel.SetConsoleCtrlHandler(None, 1)
kernel.GenerateConsoleCtrlEvent(0, 0)
sys.exit(0)