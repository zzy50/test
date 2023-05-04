import threading
import time

def before_work():
    evt.set() # flag 를 1로 설정합니다.
    print('* before work, done')

def after_work():
    print('** after work, waiting')
    evt.wait() # flag 가 1로 설정되기 전까지 대기합니다.
    print('** after work, done')

if __name__ == '__main__':
    evt = threading.Event() # Event 객체를 생성합니다. (default flag=0)
    t1 = threading.Thread(target=after_work)
    t2 = threading.Thread(target=before_work)
    evt.wait()
    t1.start()
    t2.start()