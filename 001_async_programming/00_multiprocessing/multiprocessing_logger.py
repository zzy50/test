import logging
from multiprocessing import Process, current_process
from pathlib import Path
from datetime import datetime
import os

def process_task(log_path: Path):
    # 로거 설정
    logging.basicConfig(
        filename=str(log_path),
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger("test_logger")
    try:
        # 여기에 프로세스에서 실행할 코드를 작성합니다.
        # 예를 들어, 의도적으로 예외를 발생시킵니다.
        raise ValueError("Some error occurred")
    except Exception as e:
        # 현재 프로세스에서 발생한 예외를 로그에 기록합니다.
        logger.error(f"Exception in process {current_process().name}: {e}", exc_info=True)

if __name__ == "__main__":
    # 로그 파일 경로 설정
    script_dir = Path(__file__).parent
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = script_dir / "log_test" / now
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "test.log"

    # 프로세스 생성 및 시작
    process = Process(target=process_task, args=(log_path,), name="TestProcess")
    process.start()
    process.join()
