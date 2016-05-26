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
    oauth2_token = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={appsecret}&code=%s&grant_type=authorization_code"
    oauth2_userinfo = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"
    oauth2_refresh = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={appid}&grant_type=refresh_token&refresh_token=%s"
    oauth2_check = "https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s"

    # 素材管理模块
    # 临时素材
    media_upload = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=%s"
    media_download = "https://api.weixin.qq.com/cgi-bin/media/get?access_token={access_token}&media_id=%s"
    # 永久素材
    _media_upload = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=%s"
    _media_download = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token={access_token}"
    add_news = "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token={access_token}"
    add_news_image = "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    _media_delete = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token={access_token}"
    update_news = "https://api.weixin.qq.com/cgi-bin/material/update_news?access_token={access_token}"
    _media_count = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token={access_token}"
    _media_list = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}"