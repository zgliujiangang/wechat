# coding: utf-8
import time

def search(number, numbers):
    # 二分法查找
    low = 0
    height = len(numbers) - 1
    while low < height:
        mid = (height + low) / 2
        if numbers[mid] > number:
            height = mid - 1
        elif numbers[mid] < number:
            low = mid + 1
        else:
            return mid
    return -1


def order(array):
    # 冒泡排序
    flag = False
    for i in range(len(array)):
        if not flag:
            for j in range(len(array)-i):
                flag = True 
                if array[j] > array[j+1]:
                    array[j+1], array[j] = array[j], array[j+1]
                    flag = False
        else:
            break
    return array


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
