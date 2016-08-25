# coding: utf-8


def test():
    n = 1
    while 1:
        yield n 
        n += 1


if __name__ == "__main__":

    my_func = test()
    print type(my_func)
    print my_func.next()
    print my_func.next()
    print my_func.next()
    print dir(my_func)
    print my_func.gi_code
    print my_func.gi_frame
    print my_func.gi_running