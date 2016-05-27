# coding: utf-8
import sys
sys.path.append("..")

from examples.init_wechat import wechat
from wechat_sdk.contrib.media import TemporaryMedia

# 素材管理接口测试
def test_upload():
	img_name = "test.png"
	my_media = TemporaryMedia(wechat)
	with open(img_name, 'rb') as f:
		print my_media.upload(media=f)
	media_id = "8xjbXRO40_jgSeGtGRqi-qbjuSbztp4FhblA6cfJJQELqlJQjKbS45dcoe5_0MtA"
	my_image = my_media.download(media_id)
	if my_image["type"] == "json":
	    print my_image
	if my_image["type"] == "buffer":
	    copy_file = open("copy.png", 'wb')
	    copy_file.write(my_image["result"])
	    copy_file.close()
	my_media = PermanentMedia(wechat)
	print my_media.get_list()


if __name__ == "__main__":
	test_upload()
