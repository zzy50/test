import atexit

def exit_func():
    print("Have a nice day.")

def main():
    print("hello")

atexit.register(exit_func)
main()