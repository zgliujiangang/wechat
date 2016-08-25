# coding: utf-8


def child_set(input_set):
	# 返回的是一个列表
	if len(input_set) == 1:
		return [set(), set([input_set.pop()])]
	else:
		n = input_set.pop()
		_child_set = child_set(input_set)
		_de_set = [set([n]) | i for i in _child_set]
		return _child_set + _de_set


if __name__ == '__main__':

	my_set = set([1,2,3,4,5])
	my_child_set = child_set(my_set)
	print my_child_set
	print len(my_child_set)