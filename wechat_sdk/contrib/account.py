# -*- coding: utf-8 -*-


from urllib import quote
from ..urls import ApiUrl


class ActionName:
    qr_scene = "QR_SCENE"
    qr_limit_scene = "QR_LIMIT_SCENE"
    qr_limit_str_scene = "QR_LIMIT_STR_SCENE"


class AccountManager(object):

    def __init__(self , wp):
        self.wp = wp

    def create_qrcode(self, action_name, scene_id, expire_seconds=None):
        """生成带参数的二维码
        @param action_name: 二维码类型 QR_SCENE为临时,QR_LIMIT_SCENE为永久,
                            QR_LIMIT_STR_SCENE为永久的字符串参数值
        @param scene_id: 场景id, scene_str也通过此参数传递
        @param expire_seconds: 二维码有效期（默认30秒），当action_name为QR_SCENE有效
        """
        action_info = {}
        if action_name == ActionName.qr_limit_str_scene:
            scene = {"scene_id": scene_id}
        else:
            scene = {"scene_str": scene_id}
        data = {"action_name": action_name, "action_info": {"scene": scene}}
        if expire_seconds and action_name == ActionName.qr_scene:
            data["expire_seconds"] = expire_seconds
        return self.wp.post(ApiUrl.create_qrcode, data=data)

    def download_qrcode(self, ticket):
        """通过ticket换取二维码
        @param ticket: 获取的二维码ticket
        """
        url = ApiUrl.download_qrcode % quote(ticket)
        return self.wp.download(url)

    def get_shorturl(self, long_url):
        """长链接转短链接接口
        @param long_url: 长链接
        """
        return self.wp.post(ApiUrl.get_shorturl, dict(action="long2short", long_url=long_url))
