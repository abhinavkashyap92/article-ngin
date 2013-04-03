from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import pymongo
import re
from db_config import get_connection
import json
import re
from datetime import datetime

class myHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		try:
			print "Hey"
			json_obj = self.rfile.read(int(self.headers['Content-Length']))
			json_obj = eval(json_obj)
			# print json_obj

			if json_obj.has_key('type'):
				if json_obj["type"] == "query":
					return_value = handle_query(json_obj['query'])
				if json_obj["type"] == "sign_up":
					return_value = sign_up(json_obj)
				if json_obj["type"] == "sign_in":
					return_value = sign_in(json_obj)
				if json_obj["type"] == "session_check":
					return_value = check_session()

			self.send_response(200)
			self.send_header('Content-type','text-html')
			self.send_header("Access-Control-Allow-Origin","*")
			self.end_headers()
			self.wfile.write(return_value);


		except IOError:
			self.send_error(404,"file not found")

def handle_query(user_query):
	print user_query
	print "This is entering"
	db = get_connection()
	collection = db['articles']
	regex = r'select articles where ((and)?(\s)*(keyword|date_published|author_name|tags)(\s)*(=|AFTER|BEFORE) (\w|[-])+)+'

	m = re.match(regex , user_query)
	if m:
		# There is a match
		user_query = user_query[user_query.index('where')+6:]
		user_query = user_query.strip()

		filter_list = user_query.split('AND')
		result_dict = {}
		for each_filter in filter_list:
			if '=' in each_filter:
				# print "in="
				temp = each_filter.split('=')
				#query = '{'+str(temp[0])+':'+str(temp[1])+'}'
				#result_dict = eval(query)
				temp[0] = temp[0].strip()
				temp[1] = temp[1].strip()
				result_dict[str(temp[0])] = str(temp[1])
				print result_dict
				
			if 'AFTER' in each_filter:
				# print "in after"
				temp = each_filter.split('AFTER')
				temp[0] = temp[0].strip()
				split_date = temp[1].split('-')
				datetime_obj = datetime(int(split_date[2]),int(split_date[1]),int(split_date[0]))
				#query = "{}"
				temp_dict = {}
				temp_dict["$gte"]=datetime_obj
				#print "result_dict"+result_dict
				result_dict[str(temp[0])] = temp_dict
				print result_dict

			if 'BEFORE' in each_filter:
				print "in BEFORE"
				temp = each_filter.split('BEFORE')
				temp[0] = temp[0].strip()
				split_date = temp[1].split('-')
				datetime_obj = datetime(int(split_date[2]),int(split_date[1]),int(split_date[0]))
				temp_dict = {}
				temp_dict["$lt"]=datetime_obj
				#print "result_dict"+result_dict
				result_dict[str(temp[0])] = temp_dict
				print result_dict


		obj = collection.find(result_dict)
		list_of_dictionaries = []
		for doc in obj:
			list_of_dictionaries.append(doc)


		return_list = []

		for eachObject in list_of_dictionaries:
			new_dictionary = {}
			for eachKey in eachObject.keys():
				if isinstance(eachObject[eachKey],unicode):
					# print "This is a string"
					eachKey = eachKey.encode("utf-8")
					new_dictionary[eachKey] = eachObject[eachKey].encode("utf-8")

				elif isinstance(eachObject[eachKey],datetime):
					# print "This is a datetime"
					eachKey = eachKey.encode("utf-8")
					date = eachObject[eachKey]
					new_dictionary[eachKey] = date.strftime("%d %B %y")


				elif isinstance(eachObject[eachKey],list):
					# print "This is alist"
					temp_list = []
					eachKey = eachKey.encode("utf-8")
					for eachString in eachObject[eachKey]:
						temp_list.append(eachString.encode("utf-8"))
					new_dictionary[eachKey] = temp_list
			return_list.append(new_dictionary)

		# print return_list
		if len(return_list)==0:
			return '{"status":"no_matching_articles"}'
		else:
			return json.dumps(return_list)

	else:
		print "The regex is not a match"
		return '{"status":"error"}'








def sign_up(json_obj):

	try:
		user_details = dict(_id=json_obj['user_name'],user_name = json_obj['user_name'] , email=json_obj["sign_up_email"] , password=json_obj["password"])
		db = get_connection()
		collection = db['users']
		collection.insert(user_details)
		return '{"status":"success"}'

	except Exception:
		return '{"status":"error"}'



def sign_in(json_obj):
	user_name = json_obj["user_name"]
	password = json_obj["password"]
	db = get_connection()
	collection = db['users']
	result_cursor = collection.find({"user_name":user_name,"password":password})
	if result_cursor.count() != 0:
		return '{"status":"success"}'
	else:
		return '{"status":"error"}'



def check_session():

	# logged_in = 'username' in session
	logged_in = True

	if logged_in:
		return '{"status":"success"}'
	else:
		return  '{"status":"error"}'


	
def run():
	server_address = ('localhost',9000)
	httpd = HTTPServer(server_address,myHTTPRequestHandler)
	print("HTTPServer running")
	httpd.serve_forever()



if __name__ == '__main__':
	run()