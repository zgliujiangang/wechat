# coding: utf-8
from .urls import ApiUrl

class MediaType(object):
    image = "image"
    voice = "voice"
    video = "video"
    thumb = "thumb"


class MediaBaseManager(object):

    def __init__(self, wechat):
        self.wechat = wechat


class TemporaryMedia(MediaBaseManager):

    def upload(self, type=MediaType.image, media=media):
        # 默认是上传图片，所有临时素材只能保存三天，三天后media_id失效
        # media可以是stringIO也可以是一个被打开的文件open(filepath, 'rb')
        # TODO 增加对路径的支持，目前请不要传路径
        url = ApiUrl.media_upload % type
        return self.wechat.upload(url, media=media)

    def download(self, media_id):
        url = ApiUrl.media_download % media_id
        return self.wechat.download(url)


class PermanentMedia(MediaBaseManager):

    def upload(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def count(self):
        pass

    def get_list(self):
        pass