# -*- coding: utf-8 -*-
# 用户管理


from ..urls import ApiUrl


class UserManager(object):

    def __init__(self, wp):
        self.wp = wp

    def create_group(self, name):
        """创建分组
        @param name: 分组的名称
        """
        data = {"group": {"name": name}}
        return self.wp.post(ApiUrl.create_group, data=data)
	
    def get_groups(self):
        """查询所有分组
        """
        return self.wp.get(ApiUrl.get_groups)

    def get_user_groupid(self, openid):
        """查询用户所在分组
        @param openid: 用户的opendid
        """
        return self.wp.post(ApiUrl.get_id, dict(openid=openid))

    def update_group(self, groupid, name):
        """修改分组名
        @param groupid：分组id
        @param name: 分组名字 30个字符以内
        """
        data = {"group": {"id": groupid, "name": name}}
        return self.wp.post(ApiUrl.update_group, data=data)

    def move_user_to_group(self, openid, to_groupid):
        """移动用户分组
        @param openid: 用户的openid
        @param to_groupid: 分组id
        """
        data = dict(openid=openid, to_groupid=to_groupid)
        return self.wp.post(ApiUrl.to_group, data=data)

    def batch_move_to_group(self, openid_list, to_groupid):
        """批量移动用户分组
        @param openid_list: 用户的openid组成的列表
        @param to_groupid: 分组id
        """
        data = dict(openid_list=openid_list, to_groupid=to_groupid)
        return self.wp.post(ApiUrl.batch_to_group, data=data)

    def delete_group(self, groupid):
        """删除分组
        @param groupid: 分组id 
        """
        data = {"group": {"id": groupid}}
        return self.wp.post(ApiUrl.delete_group, data=data)

    def update_user_remark(self, openid, remark):
        """设置用户备注名
        @param openid: 用户的openid
        @parma remark: 用户备注
        """
        return self.wp.post(ApiUrl.update_remark, dict(openid=openid, remark=remark))

    def get_userinfo(self, openid):
        """获取用户基本信息（包括UnionID机制）
        @param openid: 用户的openid
        """
        url = ApiUrl.get_userinfo % openid
        return self.wp.get(url)

    def batch_get_userinfo(self, user_list):
        """批量获取用户基本信息,最多支持一次拉取100条
        @param user_list: 用户openid和语言组成的字典列表
        """
        return self.wp.post(ApiUrl.batch_get_userinfo, dict(user_list=user_list))

    def get_userlist(self, next_openid=""):
        """获取用户列表,一次拉取调用最多拉取10000个关注者的OpenID
        @param next_openid: 第一个拉取的OPENID，不填默认从头开始拉取
        """
        url = ApiUrl.get_userlist % next_openid
        return self.wp.get(url)
