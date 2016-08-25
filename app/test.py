# coding: utf-8
import sys
sys.path.append("..")

from config.init import init_config
from mongo import SingleMongoClient


config = init_config()
mongo_client = SingleMongoClient(config.get("mongodb", "uri"))
mongo_test = mongo_client.test
cursor = mongo_test.user.find({"name": "liujian_g"})
for document in cursor:
	print document