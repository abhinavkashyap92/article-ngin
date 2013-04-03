from pymongo import MongoClient 



def get_connection():
	client = MongoClient('localhost',27017)

	db = client['nudb']
	return db