# coding: utf-8
import sys
sys.path.append("..")

from examples_test.sqlutil import SqlSearch, SqlInsert, SqlUpdate, SqlCount


if __name__ == '__main__':
    user_id = 10098
    status = 1
    position_id = 1092
    sql = SqlSearch("hr_candidate").filter(to_member_id=user_id).count()
    if status:
        sql = sql.filter(status=status)
    resume_fields = ["name as resume_name", "gender", "age", "email", 
    "experience", "expect_location", "price", "review", "interview_time", "resume_code"]
    sql = sql.join("hr_resume", "hr_resume.id=hr_candidate.resume_id").join_get(resume_fields)
    sql = sql.join("hr_individual_info", "hr_individual_info.id=hr_candidate.from_member_id").join_get(["real_name as delivery_id"])
    sql = sql.join("hr_position_delivery", "hr_position_delivery.candidate_id=hr_candidate.id")
    sql = sql.join("hr_position", "hr_position.id=hr_position_delivery.position_id").join_get(["name as position_name"])
    if position_id:
        sql = sql.join_filter(id=position_id)
    sql, params = sql.data()
    print sql
    print params