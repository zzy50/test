from queue import Queue
import threading
import time

def before_work():
    time.sleep(1)
    evt.set() # flag 를 1로 설정합니다.
    print('* before work, done')

def after_work():
    print('** after work, waiting')
    evt.wait() # flag 가 1로 설정되기 전까지 대기합니다.
    
    print('** after work, done')

def check_state():
    print('*** check state,', evt.isSet()) # isSet(): 현재 플래그 상태를 반환합니다.
    evt.wait() 

    print('*** check state,', evt.isSet())
    
if __name__ == '__main__':
    evt = threading.Event()  # Event 객체를 생성합니다. (default flag=0)
    after_thr = threading.Thread(target=after_work)
    before_thr = threading.Thread(target=before_work)
    state_thr = threading.Thread(target=check_state)

    after_thr.start()
    time.sleep(1)
    state_thr.start()
    
    before_thr.start()