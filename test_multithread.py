import threading
import time


def show1(arg1, arg2):
    time.sleep(1)
    mystring = str(arg1).join(arg2)
    print("thread {} running....{}".format(arg1, mystring))


def show2(arg1, arg2):
    time.sleep(1)
    mystring = str(arg1).join(arg2)
    print("thread {} running....{}".format(arg1, mystring))


if __name__ == '__main__':
    thread_list = []
    for i in range(10):
        t = threading.Thread(target=show1, args=(i, 'show1'))
        thread_list.append(t)
    for t in thread_list:
        t.start()
        # string = str(i).join(" thread(s)")
        # if i%2:
        #     t = threading.Thread(target=show1, args=(i, "show1"))
        #     t.start()
        # else:
        #     t = threading.Thread(target=show2, args=(i, "show2"))
        #     t.start()


