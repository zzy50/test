import threading
import time

shared_number = 0
lock = threading.Lock() # threading에서 Lock 함수 가져오기

def thread_1(number):
    global shared_number
    print("number = ",end=""), print(number)
    
    lock.acquire() # 작업이 끝나기 전까지 다른 쓰레드가 공유데이터 접근을 금지
    for i in range(number):
        shared_number += 1
    lock.release() # lock 해제

def thread_2(number):
    global shared_number
    print("number = ",end=""), print(number)

    lock.acquire() # thread_2 잠금
    for i in range(number):
        shared_number += 1
    lock.release() # thread_2 해제

if __name__ == "__main__":

    threads = [ ]

    start_time = time.time()
    t1 = threading.Thread( target= thread_1, args=(50000000,) )
    t1.start()
    threads.append(t1)

    t2 = threading.Thread( target= thread_2, args=(50000000,) )
    t2.start()
    threads.append(t2)

    for t in threads:
        t.join()

    print("--- %s seconds ---" % (time.time() - start_time))

    print("shared_number=",end=""), print(shared_number)
    print("end of main")