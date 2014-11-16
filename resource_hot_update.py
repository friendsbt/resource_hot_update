import motor
from tornado.ioloop import IOLoop
from tornado import gen
import random
from datetime import date
import json
from resource_type import ResourceType
from resource_manager import ResourceStoreManager

class HotUpdate(object):
	
	'''
	hot of resources in all_resources DB is like
		hot[{hot_day:hot, download_num_day:download of last period}]
	'''
	def __init__(self):
		self._main_type_sum = ResourceType.get_sum_main_type()
		self._db = motor.MotorClient('127.0.0.1', 27017).fbt
		self._coll = self._db.all_resources
		self._hot_day_coefficence = 0.5
		self._DESCENDING  = -1
		self._hotRankLists = [[] for i in range(self._main_type_sum)]
		
	@gen.coroutine
	def update_hot_day(self):
		cursor = self._coll.find({"public": 1, "hidden": {"$ne": 1}})
		while (yield cursor.fetch_next):
			res = cursor.next_object()
			res["hot"][0]["hot_day"] = res["hot"][0]["hot_day"]*self._hot_day_coefficence+res["hot"][0]["download_num_day"]
			res["hot"][0]["download_num_day"] = 0
			self._coll.save(res)
	
	@gen.coroutine
	def rand_download_num_day(self):
		cursor = self._coll.find({"public":1, "hidden": {"$ne": 1}})
		while (yield cursor.fetch_next):
			res = cursor.next_object()
			res["hot"][0]["download_num"] = random.randint(0,100)
			self._coll.save(res)
	
	@gen.coroutine
	def get_hottest_resource(self, max_records=500):
		assert max_records >= 500
		for res_type in range(self._main_type_sum):
			self._hotRankLists[res_type] = []
			cursor = self._coll.find({"hidden": {"$ne": 1}, "public": 1, "main_type": res_type}, {"_id": 0}).sort([('hot.0.hot_day', self._DESCENDING), ('download_num', self._DESCENDING)]).limit(max_records)
			while (yield cursor.fetch_next):
				res = cursor.next_object()
				one_resource = ResourceStoreManager.extract_resource_from_db(res)
				self._hotRankLists[res_type].append(res)

	def backup_hot_resource(self, max_records=10):
		assert max_records >= 10
		for res_type in range(self._main_type_sum):
			today = date.today().strftime("%Y-%m-%d")
			main_type = ResourceType.get_main_type_by_index(res_type)
			with open("dump-"+main_type+"-"+today+".txt", "w") as outfile:
				json.dump(self._hotRankLists[res_type][0:max_records], outfile)
	
	@gen.coroutine
	def run(self, func):
		IOLoop.current().run_sync(func)

	

	


	
