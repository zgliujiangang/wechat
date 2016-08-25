# coding: utf-8
from pymongo import MongoClient
from pattern.singleton import singleton


@singleton
class SingleMongoClient(MongoClient):
	pass