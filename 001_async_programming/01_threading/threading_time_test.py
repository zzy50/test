import threading

class MyClass:
    def __init__(self):
        self.count = 0

    def my_method(self):
        # 여기에 실행할 코드 작성
        print(self.count)
        t = threading.Timer(5, self.my_method)
        t.daemon = True
        t.start()

    def add_count(self):
        self.count += 1

    

my_instance = MyClass()
my_instance.my_method()

# 다른 코드들
while True:
    my_instance.add_count()
