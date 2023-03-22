import sys
import os
import subprocess
import time

base_dir = os.path.dirname(os.path.realpath(__file__))
# flag to kill ffmpeg process
stop_ffmpeg = False

# first, create a .bat file to start ffmpeg
# note: some params is not available in old ffmpeg version
command = f'ffmpeg -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_on_network_error 1 -reconnect_on_http_error 1 -reconnect_delay_max 3 -i https://some-stream-url -t 3600 -c copy -bsf:a aac_adtstoasc "stream-output.mp4"'
cmd_command = f"@echo OFF\ntitle FFMPEG Task: Demo\n{command}"
cmd_file = f"{base_dir}/ffmpeg_demo.bat"
with open(cmd_file, 'w+') as f:
        f.write(cmd_command)

# execute bat file, get process id (PID)
p = subprocess.Popen(cmd_file, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE)
while not stop_ffmpeg:
        time.sleep(1)
...
# when we want stop recording, set stop_ffmpeg = True
if stop_ffmpeg:
        subprocess.check_call([sys.executable, 'ctrl_c.py', str(self.sub_p.pid)])
        time.sleep(5)
        p.communicate(input=b"y\n")  # ffmpeg is asking `y` to confirm stop process