# coding: utf-8


class ApiUrl(object):
    # access_token获取接口
	token = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"

    # 微信公众号菜单自定义接口
    create_menu = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}"
    get_menu = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token={access_token}" 
    delete_menu = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={access_token}"