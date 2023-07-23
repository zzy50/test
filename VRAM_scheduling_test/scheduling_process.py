import time
import logging
import socket
import subprocess
import GPUtil
import re
import argparse
import sys
import threading
from queue import Queue, Empty
from datetime import datetime
from pathlib import Path

from config import MIN_VRAM


HOST = '0.0.0.0'
PORT = 10025

MAX_TRACKING_TIME = 300


CWD = "/home/cityeyelab/2TBHDD/analysis_code"
EXECUTE_FILES_ROOT = "execute_files"

LOG_ROOT = "scheduling_log"
LOG_EXECUTE_HISTORY_NAME = "execute_history"
LOG_GPU_STATUS = "gpu_status"

BACKLOG_BACKUP_NAME = "BACKLOG"


class SchedulingProcess:
    def __init__(self, host: str, port: int, min_vram: int, max_tracking_time: int, cwd: str, log_root: str, log_execute_history_name: str, log_gpu_status: str, backlog_backup_name: str) -> None:

        self.terminate_flag = False
        self.min_vram = min_vram
        self.max_tracking_time = max_tracking_time
        self.cwd = cwd
        self.backlog_file_path = Path(log_root) / backlog_backup_name

        self.BACKLOG = Queue()
        if self.backlog_file_path.exists():
            self.load_backlog()

        self.GPUs = []

        try:
            self.history_logger = WriteLog(log_root, log_name=log_execute_history_name)
            self.gpu_logger = WriteLog(log_root, log_name=log_gpu_status)

            # TCP 소켓 생성
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 주소 재사용 옵션 설정
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 소켓 바인딩
            self.server_socket.bind((host, port))

            # 서버 소켓을 수신 대기 상태로 전환
            # listen(5) 이런 식으로 숫자를 넣으면 숫자만큼의 연결 요청을 backlog에 저장하여 backlog가 꽉차면 연결 요청을 거부함.
            self.server_socket.listen()

        except Exception as e:
            LOGGER.write(f'[ERROR] Exception while starting server!: {e}')
            LOGGER.write(f'[TERMINATED] This process will be terminated.')

    def run(self):
        thread1 = threading.Thread(target=self.update_gpu_status, daemon=True)
        thread2 = threading.Thread(target=self.get_request, daemon=True)
        thread3 = threading.Thread(target=self.execute_process, daemon=True)
        thread4 = threading.Thread(target=self.write_gpu_log, daemon=True)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()

    def save_backlog(self):
        with open(self.backlog_file_path, "w") as f:
            for cmd_line in list(self.BACKLOG.queue):
                f.write(cmd_line + "\n")

    def load_backlog(self):
        with open(self.backlog_file_path, "r") as f:
            for line in f:
                cmd_line = line.strip()
                self.BACKLOG.put(cmd_line)

    def update_gpu_status(self):
        while not self.terminate_flag:
            time.sleep(1)
            self.GPUs = GPUtil.getGPUs()

    def write_gpu_log(self):
        while not self.terminate_flag:
            time.sleep(1)
            gpu_log_message = ""
            for gpu in sorted(self.GPUs, key=lambda gpu: gpu.id):
                gpu_log_message += f"{gpu.id}: {gpu.memoryUsed} / {gpu.memoryTotal}    "
            self.gpu_logger.write(gpu_log_message)

    def get_request(self):
        while not self.terminate_flag:
            try:
                while not self.terminate_flag:
                    # 연결 요청이 발생하면 연결 수립.
                    client_socket, client_addr = self.server_socket.accept()
                    LOGGER.write(f'[REQUEST] [INFO] Connected by {client_addr}')

                    try:
                        # 클라이언트로부터 데이터 수신
                        data = client_socket.recv(1024)
                        decoded_data = data.decode()
                        LOGGER.write(f'Received from client: {data.decode()}')
                    except Exception as e:
                        LOGGER.write(f'[REQUEST] [ERROR] Exception while receiving data from client: {e}')
                        response_message = f"[REQUEST] [ERROR] Exception while receiving data from client: {e}"
                        client_socket.sendall(response_message.encode())
                        client_socket.close()
                        continue

                    # 실행할 sh파일
                    execute_file_path = Path(decoded_data)
                    try:
                        if execute_file_path.exists():
                            cmd = f"dos2unix {decoded_data};chmod 777 {decoded_data};"
                            dos2unix_chmod_process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                            _, error = dos2unix_chmod_process.communicate()

                            if dos2unix_chmod_process.returncode != 0:
                                response_message = f"[REQUEST] [ERROR] {error.decode('utf-8')}"
                            else:
                                response_message = f"[REQUEST] [INFO] Success request: {execute_file_path.name}"
                                                
                            with open(execute_file_path, "r") as rf:
                                total_lines = rf.readlines()
                            for cmd_line in total_lines:
                                if cmd_line.startswith("CUDA_VISIBLE_DEVICES="):
                                    self.BACKLOG.put(cmd_line)
                                    self.save_backlog()
                        else:
                            response_message = f"[REQUEST] [ERROR] {execute_file_path.name} does not exist"
                    except Exception as e:
                        response_message = f"[REQUEST] [ERROR] {e}"

                    # response_message = f"Sucess: {decoded_data}"
                    LOGGER.write(response_message)
                    client_socket.sendall(response_message.encode())
                    client_socket.close()

            except Exception as e:
                LOGGER.write(f'[REQUEST] [ERROR] Exception while processing request: {e}')
                LOGGER.write(f'[REQUEST] [INFO] Restart loop ...')

    def execute_process(self):
        running_processes = []
        while not self.terminate_flag:
            time.sleep(10)
            for gpu in sorted(self.GPUs, key=lambda gpu: gpu.memoryFree, reverse=True): # VRAM 가용량이 가장 적은 GPU 순으로 정렬
                if gpu.memoryFree > self.min_vram:
                    try:
                        cmd_line = self.BACKLOG.get(timeout=5)
                        cmd_line = re.sub(r"CUDA_VISIBLE_DEVICES=\d+", f"CUDA_VISIBLE_DEVICES={gpu.id}", cmd_line)
                        cmd_line = re.sub(r"--device \d+", f"--device {gpu.id}", cmd_line)
                        final_cmd_line = f"cd /home/cityeyelab/2TBHDD/analysis_code; {cmd_line}"
                        match = re.search(r"--path '([^']*)'", final_cmd_line)
                        if match:
                            spot_name = Path(match.group(1)).name
                        else:
                            spot_name = None

                        try:
                            main_process = subprocess.Popen(final_cmd_line, shell=True, stderr=subprocess.PIPE)
                            start_time = time.time()
                            running_processes.append((main_process, spot_name, start_time))
                            LOGGER.write(f"[EXECUTE] [INFO] Process started: {spot_name}")
                        except Exception as e:
                            response_message = f"[EXECUTE] [ERROR] {e}"
                            LOGGER.write(response_message)

                    except Empty:
                        response_message = f"[EXECUTE] [INFO] BACKLOG is empty!"
                        LOGGER.write(response_message)

            # 실행중인 프로세스의 상태를 확인.
            current_time = time.time()
            for process, spot_name, start_time in running_processes:
                # 프로세스가 종료되었다면 if 블럭 내의 코드가 실행됨. 
                # subprocess.Popen.poll: 프로세스가 종료되었으면 종료 코드를 반환하고, 아직 실행 중이면 None을 반환하는 메소드.
                if process.poll() is not None:
                    running_processes.remove((process, spot_name, start_time))
                    if process.returncode != 0:
                        error = process.stderr.read()
                        response_message = f"[EXECUTE] [ERROR] {error.decode('utf-8')}"
                    else:
                        response_message = f"[EXECUTE] [INFO] Success execute: {spot_name}"
                        self.history_logger.write(cmd_line)
                    LOGGER.write(response_message)
                    LOGGER.write(f"[EXECUTE] [INFO] Process finished: {spot_name}")
                elif current_time - start_time > self.max_tracking_time:
                    running_processes.remove((process, spot_name, start_time))
                    response_message = f"[EXECUTE] [INFO] Success execute: {spot_name}"
                    LOGGER.write(response_message)
                    LOGGER.write(f"[EXECUTE] [INFO] Process finished: {spot_name}")

        
class WriteLog(object):
    def __init__(self, log_root: str, log_name: str=None, time: str=None):
        if not log_name:
            log_name = log_root

        if time == "auto":
            self.time = datetime.now().strftime("%Y%m%d_%H%M%S")
        elif time:
            self.time = time
        else:
            self.time = None

        if self.time:
            self.log_root_path = Path(log_root) / self.time
        else:
            self.log_root_path = Path(log_root)
        self.log_root_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger()

        # 로그 출력 기준 설정
        self.logger.setLevel(logging.INFO)

        # 로그 메세지 형식 지정
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # 로그를 저장할 파일 이름 지정
        if self.time:
            log_path = self.log_root_path / f"{log_name}_{self.time}.txt"
        else:
            log_path = self.log_root_path / f"{log_name}.txt"
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def write(self, message: str) -> None:
        self.logger.info(message)

    def handle_exception(self, *args):
        # sys.excepthook: exc_type, exc_value, exc_traceback 정보를 3개의 인수로 전달함.
        if len(args) == 3: 
            self.logger.error("Unexpected exception", exc_info=(args[0], args[1], args[2]), extra={"markup":False, "highlighter": None})
        
        # threading.excepthook은 예외 객체를 1개의 인수로 전달함.
        elif len(args) == 1:
            self.logger.error("Unexpected exception", exc_info=(args[0].exc_type, args[0].exc_value, args[0].exc_traceback), extra={"markup":False, "highlighter": None})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute_files", type=str, default=None, help="Execute files from the specified file")
    args = parser.parse_args()

    scheduling = SchedulingProcess(
        host=HOST, 
        port=PORT,
        cwd=CWD,
        max_tracking_time=MAX_TRACKING_TIME,
        log_root=LOG_ROOT, 
        log_execute_history_name=LOG_EXECUTE_HISTORY_NAME,
        backlog_backup_name=BACKLOG_BACKUP_NAME
        )

    if args.execute_files:
        execute_files_root = Path(CWD) / EXECUTE_FILES_ROOT
        for execute_file in sorted(execute_files_root.glob("*execute_files.sh")):
            if execute_file.name >= args.execute_files:
                scheduling.BACKLOG.put(str(execute_file))
                scheduling.save_backlog()
    
    scheduling.run()


if __name__ == "__main__":
    LOGGER = WriteLog(LOG_ROOT, time="auto")
    sys.excepthook = LOGGER.handle_exception
    threading.excepthook = LOGGER.handle_exception
    main()







# 주소: 소켓의 식별자. IP와 PORT를 조합하여 생성됨.
# socket.AF_INET: 주소 체계(address family)를 지정. IPv4 인터넷 프로토콜을 사용하는 주소 체계를 의미. (IPv6: socket.AF_INET6)
# socket.SOCK_STREAM: 소켓 타입을 지정. 연결 지향형 소켓을 의미.
# socket.SOL_SOCKET: 소켓 레벨 옵션 설정.
# socket.SO_REUSEADDR: 
# TCP 연결의 종료 과정에서 발생할 수 있는 문제를 방지하기 위함. 
# TCP 연결을 종료할 때, 운영 체제는 TIME_WAIT 상태로 전환하여 일정 시간 동안 소켓을 열어둠. (일반적으로 30초~120초) 
# 이 시간 동안 운영 체제에서 네트워크 상에 지연된 패킷을 수신하고 처리함. 이 시간 동안 서버를 다시 시작하려고 하면 "Address already in use" 오류가 발생함.
# TIME_WAIT 상태가 종료되면 소켓이 닫히고, 해당 주소를 다시 사용할 수 있게 됨.
# 이 옵션은 개발중에 주로 사용하고(서버를 자주 껐다 켰다 하므로), 실제 사용할 때는 30초~120초 간격으로 서버를 재시작할 일은 거의 없으므로 사용할 필요 없음.