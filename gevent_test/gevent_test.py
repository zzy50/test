import gevent
import requests
from gevent import monkey, socket

monkey.patch_all()

def arbitrary_socket_call():
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect(('www.google.com', 80))
    _socket.send(b"GET / HTTP/1.1\r\nHost:www.google.com\r\n\r\n")
    response = _socket.recv(4096)
    print(response)

def run_many_socket_calls():
    jobs = [gevent.spawn(arbitrary_socket_call) for _ in range(1000)]
    gevent.joinall(jobs)

TARGET_URL_LIST = [
    'http://www.google.com',
    'http://www.youtube.com',
    'http://www.facebook.com',
    'http://www.twitter.com',
    'http://www.instagram.com',
    'http://www.wikipedia.com',
    'http://www.yahoo.com',
    'http://www.live.com',
    'http://www.reddit.com',
    'http://www.netflix.com',
    'http://www.linkedin.com',
    'http://www.office.com',
    'http://www.bing.com',
    'http://www.quora.com',
    'http://www.ebay.com',
]

def send_request(url: str):
    content = requests.get(url).content
    print(content)

def run_concurrent():
    jobs = [gevent.spawn(send_request, url) for url in TARGET_URL_LIST]
    gevent.joinall(jobs)

# gevent.socket 을 사용함으로써 동일한 결과를 내는 코드가 더 빠르게 실행된다 
# gevent.socket 은 blocking I/O가 발생하면 그것을 기다리는 동안 다른 작업을 처리할 수 있게 해준다.