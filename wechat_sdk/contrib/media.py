# -*- coding: utf-8 -*-
# 素材管理


import json
from ..urls import ApiUrl


class MediaType:
    image = "image"
    voice = "voice"
    video = "video"
    thumb = "thumb"


class MediaManager(object):

    def __init__(self, wp):
        self.wp = wp

    def upload_temp_media(self, media_type, media_file):
        """新增临时素材，有效期三天
        @param media_type: 媒体文件类型
        @param media_file: 媒体文件
        """
        url = ApiUrl.upload_temp_media % media_type
        return self.wp.upload(url, media=media_file)

    def download_temp_media(self, media_id):
        """获取临时素材，返回的是文件buffer
        @param media_id: 媒体文件唯一标识
        """
        url = ApiUrl.download_temp_media % media_id
        return self.wp.download(url)

    def upload_perm_media(self, media_type, media_file):
        """新增永久素材,不包含图文素材，有上限值
        @param media_type: 媒体文件类型
        @param media_file: 媒体文件
        """
        url = ApiUrl.upload_perm_media % media_type
        return self.wp.upload(url, media=media_file)

    def download_perm_media(self, media_id):
        """获取永久素材，返回的可能是文件也有可能是json串
        @param media_id: 媒体文件唯一标识
        """
        return self.wp.download(ApiUrl.download_perm_media, dict(media_id=media_id))

    def delete_perm_media(self, media_id):
        """删除永久素材
        @param media_id: 媒体文件唯一标识
        """
        return self.wp.post(ApiUrl.delete_perm_media, dict(media_id=media_id))

    def add_news(self, articles):
        """新增永久图文素材
        @param articles: 图文内容，可以是一个字典也可以是由多个article组成的列表
        """
        return self.wp.post(ApiUrl.add_news, dict(articles=articles))

    def update_news(self, media_id, index, articles):
        """修改永久图文素材
        @param media_id: 媒体文件唯一标识
        @param index: 文章在图文消息中的位置
        @param articles: 修改的文章参数字典包含["title", "thumb_media_id", "author", 
                       "digest", "show_cover_pic", "content", "content_source_url"]
        """
        data = {"media_id": media_id, "index": index, "articles": articles}
        return self.wp.post(ApiUrl.update_news, data=data)

    def get_media_count(self):
        """获取永久素材总数列表
        """
        return self.wp.get(ApiUrl.media_count)

    def get_media_list(self, media_type, offset=0, count=20):
        """分类型获取永久素材的列表
        """
        data = {"type": media_type, "offset": offset, "count": count}
        return self.wp.post(ApiUrl.media_list, data=data)