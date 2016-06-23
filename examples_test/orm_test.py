# coding: utf-8
import sys
sys.path.append("..")

from examples_test.orm import SqlSearch, SqlInsert, SqlUpdate


if __name__ == '__main__':
    fields = ["name", "age", "sex"]
    test = SqlSearch('hr_resume').get(fields).filter(name__like="liu").data()
    print test