# -*- coding: utf-8 -*-


import sys
sys.path.append("..")

from examples.base_test import wechat_app
from wechat_sdk.contrib.media import MediaManager, MediaType


# 素材管理接口测试
def media_test():
    media_manager = MediaManager(wechat_app)
    media_list = media_manager.get_media_list(MediaType.image)
    print media_list
    my_image = media_manager.download_perm_media(media_list["item"][0]["media_id"])
    if my_image["type"] == "buffer":
        with open("copy.png", "wb") as f:
            f.write(my_image["buffer"])
        print "download success"
    print media_manager.get_media_count()


if __name__ == "__main__":
    media_test()
