# coding: utf-8
# 素材管理
import json
from ..urls import ApiUrl

class MediaType(object):
    image = "image"
    voice = "voice"
    video = "video"
    thumb = "thumb"


class MediaBaseManager(object):

    upload_url = None
    download_url = None

    def __init__(self, wechat):
        self.wechat = wechat

    def upload(self, type=MediaType.image, media=None):
        # 默认是上传图片，所有临时素材只能保存三天，三天后media_id失效
        # media可以是StringIO对象也可以是一个被打开的文件对象open(filepath, 'rb')
        # TODO 增加对路径的支持，目前请不要传路径
        # TODO 上传视频素材时还要增加一个表单
        url = self.upload_url % type
        return self.wechat.upload(url, media=media)

    def download(self, media_id):
        # 未下载成功会返回None,需要debug时wechat=Wechat(debug=True)
        # 成功下载后返回的是一个文件流，需要自行处理
        url = self.download_url % media_id
        return self.wechat.download(url)


class TemporaryMedia(MediaBaseManager):

    upload_url = ApiUrl.media_upload
    download_url = ApiUrl.media_download


class PermanentMedia(MediaBaseManager):

    upload_url = ApiUrl._media_upload
    download_url = ApiUrl._media_download

    def download(self, media_id):
        url = self.download_url
        return self.wechat.download(url, data=dict(media_id=media_id))

    def add_news(self, data):
        return self.wechat.post(ApiUrl.add_news, data=data)

    def add_news_image(self, media):
        return self.wechat.upload(ApiUrl.add_news_image, media=media)

    def delete(self, media_id):
        return self.wechat.post(ApiUrl._media_delete, data={"media_id": media_id})

    def update_news(self, data):
        return self.wechat.post(ApiUrl.update_news, data=data)

    def count(self):
        return self.wechat.get(ApiUrl._media_count)

    def get_list(self, type=MediaType.image, offset=0, count=20):
        return self.wechat.post(ApiUrl._media_list, data={"type": type, "offset": offset, "count": count})