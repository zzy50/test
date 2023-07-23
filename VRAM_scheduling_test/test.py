import time
import logging
from queue import Queue, Empty
from threading import Thread
from datetime import datetime
from pathlib import Path


FILENAME = "2023_07_12_16_58_26_execute_file.sh"
LOG_ROOT = "log"

LIMIT_QSIZE = 5
BACKLOG = Queue()
RUNNING = Queue()
DONE = Queue()


class Test:
    def __init__(self) -> None:
        self.logger = WriteLog(LOG_ROOT)
        self.running_zero_time = None
        self.exit_flag = False

    def main(self):
        thread1 = Thread(target=self.get_request, daemon=True)
        thread2 = Thread(target=self.execute_process, daemon=True)
        thread3 = Thread(target=self.process_in_running, daemon=True)
        thread4 = Thread(target=self.write_num_of_process_in_running, daemon=True)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()

        self.logger.write("Test is Done!")

    def get_request(self):
        with open(FILENAME, "r", encoding="utf-8") as rf:
            total_lines = rf.readlines()
            for cmd_line in total_lines:
                if cmd_line.startswith("CUDA_VISIBLE_DEVICES"):
                    BACKLOG.put(cmd_line)
                    # self.logger.write(f"BACKLOG's length: {BACKLOG.qsize()}")
 
    def execute_process(self):
        while not self.exit_flag:
            if RUNNING.qsize() < LIMIT_QSIZE:
                time.sleep(0.2)
                try:
                    # get 메소드의 옵션
                    # block: True일 경우 Queue가 비어있어도 queue.Empty exception를 발생시키지 않고 Queue에 요소가 채워질 때까지 대기함. 기본값 True. 
                    # timeout: 지정된 시간 동안 대기한 후에도 Queue가 비어있으면 queue.Empty exception을 발생시킴. 
                    cmd_line = BACKLOG.get(timeout=5)
                except Empty:
                    self.logger.write("BACKLOG is empty!")   
                    self.exit_flag = True
                RUNNING.put(cmd_line)

    def process_in_running(self):
        while not self.exit_flag:
            time.sleep(1)
            done_task = RUNNING.get()
            DONE.put(done_task)
            self.logger.write(f"DONE's length: {DONE.qsize()}")

    def write_num_of_process_in_running(self):
        while not self.exit_flag:
            time.sleep(0.2)
            self.logger.write(f"RUNNING's length: {RUNNING.qsize()}")


class WriteLog(object):
    def __init__(self, log_root: str, log_name: str=None):
        if not log_name: 
            log_name = log_root
        self.now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_root_path = Path(log_root) / self.now
        self.log_root_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger()

        # 로그 출력 기준 설정
        self.logger.setLevel(logging.INFO)

        # 로그 메세지 형식 지정
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # 로그를 저장할 파일 이름 지정
        log_path = self.log_root_path / f"{log_name}_{self.now}.txt"
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def write(self, message: str) -> None:
        self.logger.info(message)


if __name__ == "__main__":
    test = Test()
    test.main()
