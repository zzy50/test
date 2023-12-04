import threading
import time


# https://coding-groot.tistory.com/103

# TimerThread
class TimerThread(threading.Thread):
    def __init__(self):
        self.currentTime = 0
        threading.Thread.__init__(self, name='Timer Thread')
 
    # TimerThread가 실행하는 함수
    def run(self):
        # 10초마다 
        while True:
            # 10초 기다린다
            time.sleep(10)
            # 시간을 10초 더한다
            self.currentTime += 10
            print("프로그램을 실행한 시간(초): " + str(self.currentTime))
 
if __name__ == '__main__':
    timer = TimerThread()
    # Daemon Thread로 설정하지 않음, 기본값임
    timer.setDaemon(False)
    # 타이머용 Thread 실행
    timer.start()
 
    # 허술한 덧셈 프로그램
    while True:
        a = int(input("a = "))
        b = int(input("b = "))
        print("a + b = " + str(a + b))