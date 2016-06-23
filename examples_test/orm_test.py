# coding: utf-8
import sys
sys.path.append("..")

from examples_test.orm import SqlSearch, SqlInsert, SqlUpdate



if __name__ == '__main__':
    fields = ["name", "age", "sex"]
    _fields = ["year", "month", "date"]
    test1 = SqlSearch('hr_resume').count().get(fields).get(_fields).filter(name__start_with="liu").join("hr_admin", "hr_admin.id=hr_resume.id").join_get(fields).join_filter(id__gt=1000).order_by("id DESC", "name").data()
    test2 = SqlInsert('hr_resume').insert(id=1, name='liu', sex=0, age=26).data()
    test3 = SqlUpdate('hr_admin').update(name=1, age=26).filter(name__gt=25).filter(age__lt=25).data()
    print test1
    print test2
    print test3