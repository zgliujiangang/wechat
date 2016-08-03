# coding: utf-8
import time

def search(number, numbers):
    length = len(numbers)
    start = 1 - 0
    end = length - 0
    while True:
        mid = start + (end - start) / 2
        num = numbers[mid]
        # print start
        # print end
        # print num
        # print "aaaaa"
        if num == number:
            return mid
        else:
            if start != end:
                if num > number:
                    start = start
                    end = mid + 1
                else:
                    start = mid + 1
                    end = end
            else: 
                raise ValueError("does not exist")

numbers = [i for i in range(1000000)]

number = 359872

try:
    t0 = time.clock()
    print t0
    numbers.sort()
    print search(number, numbers)
    t1 = time.clock() - t0
    print numbers.index(number)
    t2 = time.clock() - t0
    print (t2 - t1), t1
    print (t2 - t1) / t1
    print t1 / (t2 - t1)
except Exception as e:
    print e
