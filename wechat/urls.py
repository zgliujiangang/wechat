# coding: utf-8


class ApiUrl(object):
    # 微信ip地址列表
    wechat_ip = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token={access_token}"
    # access_token获取接口
    token = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"

    # 微信公众号菜单自定义接口
    create_menu = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}"
    get_menu = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token={access_token}" 
    delete_menu = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={access_token}"

    # 微信网页授权
    # code换取access_token
    oauth2_token = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={appsecret}&code=%s&grant_type=authorization_code"
    oauth2_userinfo = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"
    oauth2_refresh = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={appid}&grant_type=refresh_token&refresh_token=%s"