import threading
import time


def consumer(cd: threading.Condition):
    print("consumer thread started")
    with cd:
        print("consumer waiting ...")
        cd.wait() # cd.notifyAll()을 기다림
        print("consumer consumed the resource")


def producer(cd: threading.Condition):
    print("producer thread started ...")
    with cd:
        for _ in range(5):
            print("making resource ...")
            time.sleep(1)
        print("notifying to all consumers")
        cd.notifyAll() # 이 부분이 호출되면 cd.wait()로 기다리고 있는 모든 스레드가 cd.wait() 라인 이하의 코드를 실행한다.


if __name__ == '__main__':
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    cs2.start()
    pd.start()


"""
Condition은 다른 스레드의 신호를 기다리는 동기화(sync) 프리미티브다. 
예컨대, 해당 스레드가 실행을 마쳐야지만 현재 스레드가 나머지 계산을 수행할 수 있다.
Condition을 이용하면 다수의 다른 스레드에게 노티를 주어서 같은 컨디션으로 기다리고 있는 모든 스레드를 제어할 수 있다.

Condition.wait()는 Condition.notifyAll()을 기다린다는 의미이다.
producer 스레드에서 Condition.notifyAll()가 호출되면 기다리고 있는 모든 스레드가 wait() 함수 이하 코드를 실행하게 된다. 
event 와 명확한 차이점에 대해서 생각한다면, 노티(Condition.notifyAll())가 될 때 까지 공유된 자원에 엑세스하는 것이 배제되어야 할 될때 컨디션을 쓰는게 일반적일 것이다.
반면에 event 는 스레드들이 단지 무엇이 true 되기만을 기다리는 것 이외에는 돈케어(don't care)다.
"""