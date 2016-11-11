# coding: utf-8
import sys
sys.path.append("..")

from examples.init_wechat import wechat
from wechat_sdk.contrib.media import TemporaryMedia, PermanentMedia

# 素材管理接口测试
def test_upload():
	img_name = "test.png"
	my_media = TemporaryMedia(wechat)
	with open(img_name, 'rb') as f:
		print my_media.upload(media=f)
	media_id = "8xjbXRO40_jgSeGtGRqi-qbjuSbztp4FhblA6cfJJQELqlJQjKbS45dcoe5_0MtA"
	#media_id = "jayN-dsxxw2BbFsdU-9afGSjJ0SzliN07too3u7McQ31YulZ8w5IeemauuUsgPOQ"
	#以下为永久
	#media_id = "OVygHfzd3teiBAykiejczQLDG198q6mjeB_ZkNVfyVM"
	#url = "https://mmbiz.qlogo.cn/mmbiz/1ibicwYEENdOISb6EicZzGVpr0t0KAW2c4oJNKdYohiaI7jVCwhgnsPEiav6eqxhP0TvUgWibINV75HVFUTeBGT2x3Vw/0?wx_fmt=png"
	my_image = my_media.download(media_id)
	if my_image["type"] == "json":
	    print my_image
	if my_image["type"] == "buffer":
	    copy_file = open("copy.png", 'wb')
	    copy_file.write(my_image["result"])
	    copy_file.close()
	    print "download success"
	my_media = PermanentMedia(wechat)
	print my_media.get_list()


if __name__ == "__main__":
	test_upload()
