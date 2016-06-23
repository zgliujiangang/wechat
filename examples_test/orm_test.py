# coding: utf-8
import sys
sys.path.append("..")

from examples_test.orm import SqlSearch, SqlInsert, SqlUpdate, SqlCount



if __name__ == '__main__':
    fields_1 = ["id", "resume_id", "position_id", "status", "create_time"]
    fields_2 = ["name", "mobile", "gender", "age", "email", "experience", "expect_location", "price", "review", "interview_time", "resume_code"]
    fields_3 = ["real_name"]
    fields_4 = ["name"]
    search = SqlSearch("hr_position_delivery").get(fields_1).filter(to_member_id=10).filter(status__in=[1,2,3]).page().order_by("id")
    search = search.join("hr_resume", "hr_position_delivery.resume_id=hr_resume.id").join_get(fields_2)
    search = search.join("hr_individual_info", "hr_position_delivery.from_member_id=hr_individual_info.id").join_get(fields_3)
    search = search.join("hr_position", "hr_position_delivery.position_id=hr_position.id").join_get(fields_4).join_filter(type=1).join_filter(name__like="liu")
    
    print search.data()
    # data = SqlCount("hr_resume").filter(id=1, name=2, age__in=[23, 24, 25])
    # print data.data()