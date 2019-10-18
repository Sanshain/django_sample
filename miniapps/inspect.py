
import inspect
import traceback


def func():
    a=7
    print globals()

def main():
    r = 5
    func()

if __name__ == '__main__':
    main()
