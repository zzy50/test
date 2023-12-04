def ex1():
    import threading, queue, time
    
    SHARE_DATA = 0
    def generator(start, end):
        global SHARE_DATA
        for i in range(start, end, 1):
            buf = SHARE_DATA
            time.sleep(0.01)
            # data 값을 1씩 증가
            SHARE_DATA = buf + 1
    
    # generator함수를 두개의 쓰레드로 실행했다.
    t1 = threading.Thread(target=generator, args = (1,10))
    t2 = threading.Thread(target=generator, args = (1,10))
    # 쓰레드 시작
    t1.start()
    t2.start()
    # 쓰레드가 종료할 때까지 대기
    t1.join()
    t2.join()
    
    print(SHARE_DATA)



def ex2():
    import threading, queue, time
    data = 0
    # 쓰레드의 Lock를 가져온다.
    lock = threading.Lock()
    def generator(start, end):
        global data
        for i in range(start, end, 1):
            # lock이 설정된 이상 다음 이 lock를 호출할 때 쓰레드는 대기를 한다.
            lock.acquire()
            buf = data
            time.sleep(0.01)
            # data 값을 1씩 증가
            data = buf + 1
            # 사용이 끝나면 lock 해제한다.
            lock.release()
    
    # generator함수를 두개의 쓰레드로 실행했다.
    t1 = threading.Thread(target=generator, args = (1,10))
    t2 = threading.Thread(target=generator, args = (1,10))
    # 쓰레드 시작
    t1.start()
    t2.start()
    # 쓰레드가 종료할 때까지 대기
    t1.join()
    t2.join()
    
    print(data)


def ex3():
    import threading, queue, time
    
    data = 0
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    def generator1(start, end):
        global data
        for i in range(start, end, 1):
            # lock1로 lock 걸었다. (여기 이후를 실행하려면 lock1이 release상태여야한다.)
            lock1.acquire()
            # lock2로 lock 걸었다. (여기 이후를 실행하려면 lock2이 release상태여야한다.)
            lock2.acquire()
            print(i)
            time.sleep(0.1)
            lock2.release()
            lock1.release()
        
    def generator2(start, end):
        global data
        for i in range(start, end, 1):
            # lock2로 lock 걸었다. (여기 이후를 실행하려면 lock2이 release상태여야한다.)
            lock2.acquire()
            # lock1로 lock 걸었다. (여기 이후를 실행하려면 lock1이 release상태여야한다.)
            lock1.acquire()
            print(i)
            time.sleep(0.1)
            lock1.release()
            lock2.release()
    
    # generator1함수를 쓰레드로 실행
    t1 = threading.Thread(target=generator1, args = (1,10))
    # generator2함수를 쓰레드로 실행
    t2 = threading.Thread(target=generator2, args = (1,10))
    # 쓰레드 시작
    t1.start()
    t2.start()
    # 쓰레드가 종료할 때까지 대기
    t1.join()
    t2.join()
    
    print(data)


# ex1()
"""
ex1

분명히 generator 함수를 두번 호출했고 9번씩 두번이 돌아야 하는데 결과는 9라는 값이 나왔습니다.
이유는 제가 일부러 에러를 만들기 위해서 만든 것입니다만, 첫번째 쓰레드에서 buf에 SHARE_DATA를 담고 두번째 쓰레드에서 또 buf에 SHARE_DATA를 담습니다.
그런수 SHARE_DATA에는 다시 buf의 1 증가 값을 넣기 때문에 이런 현상이 나옵니다.

이걸 해결하기 위해서는 lock을 사용해서 동기화를 해야 합니다.
"""


# ex2()
"""
ex2

원하는 결과값이 나왔습니다.

lock 사용할 때는 항상 데드 락을 조심해야 합니다. 데드 락이란 서로 간의 락이 묶여있는 상태를 말합니다.
"""


ex3()
"""
ex3

위가 데드락의 상황인데 쓰레드는 generator1과 generator2에서는 서로 역으로 lock 걸려있는 상황입니다.
즉, generator1에서 lock1과 lock2를 걸고 들어갑니다. generator2에서 lock2와 lock1를 걸고 들어갑니다.
generator1에서 lock1에 락을 걸고 lock2를 걸고 들어가려니 이미 lock2이 generator2에서 걸린 상태입니다.
generator2에서 lock2에 락을 걸고 lock1로 걸고 들어가려니 이미 lock1이 generator1에서 걸린 상태입니다.

즉, generator1과 generator2가 서로 lock이 풀리기를 기다리는 상태가 되어 버렸습니다.
이게 데드락입니다. 위 예제는 제가 데드락을 표현하기 위해서 억지로 만든 예제입니다만, 
실무에서는 함수 안에 함수 안에서 lock을 걸고 다른 곳에서 또 lock이 걸린 상태가 되어 버리면 이런 데드락 상태가 되어버립니다.
해결 방법은 개발시에 되도록 lock을 하나로 통일하고 중첩 lock이 되지 않도록 하는 방법 밖에 없네요.

"""