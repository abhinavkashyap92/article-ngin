import re
import sys
from datetime import datetime

class nudb:
	#method save() to insert entries into the database
	def __init__(self):
		self.log_fh = open('logs/log.txt','a')

	def save(self,object):
		''' This method  saves the entries into the database 
		    
		    use case:
		    1)If you want to save a single article entry into the article database save method can be used	
		    2)If you would want to save multiple entries into the article database save method can be used
		
		    examples
		    1) db.save({'keywords':('android','ios',),'title':'The android related article'}........)
		    1) db.save([{'keywords':('android','ios',),'title':'The android related article'}........},{'keywords':('hp'),......}])		  
		'''
	 	content_file = "saved_content/content.txt"
	 	#saved_entries_list holds all the entries to be written to the file
	 	#saved content is to write the content of the corresponding entry into a separare file
	 	saved_entries_list =[]
	 	saved_content_list =[]

	 	start = datetime.now()
	 	#if the type of the object passed is a single dictionary
	 	if isinstance(object,dict):
	 	   
	 	    tuple_returned= self.__create_dict(object , content_file)
	 	    saved_entries_list.append(tuple_returned[0])
	 	    saved_content_list.append(tuple_returned[1])

	 	#if the type of the object is a list
	 	elif isinstance(object,list):

	 		for each_document in object:
	 			tuple_returned =self.__create_dict(each_document,content_file)
	 			saved_entries_list.append(tuple_returned[0])
	 			saved_content_list.append(tuple_returned[1])

	 	else:
	 		print "Invalid syntax for save method"
	 		self.log_fh.writelines("Invalid syntax for save method"+" @ "+str(datetime.now()))
	 		sys.exit(1)

	 	
	 	entries_fh = open('saved_entries/entries.txt','a')

	 	for eachEntry in saved_entries_list:
	 		entries_fh.writelines(str(eachEntry))
	 		entries_fh.writelines('\n')
	 	entries_fh.close()

	 	content_fh = open('saved_content/content.txt','a')

	 	for eachContent in saved_content_list:
	 		content_fh.writelines(str(eachContent))
	 		content_fh.writelines('\n')
	 	content_fh.close()

	 	end = datetime.now()

	 	print "Wrote "+str(len(saved_entries_list))+" entries in: "+str(end-start)+" second"
	 	self.log_fh.writelines("Wrote "+str(len(saved_entries_list))+" enrties @ "+str(datetime.now())+"\n")
	 	
	 	

	def  __create_dict(self , object , content_file):
	 	f = open('count.txt','r');
	 	count = int(f.readline())
	 	f.close()
	 	id = count + 1
	 	keywords = object['keywords']
	 	likes = object['likes']
	 	comments = object['comments']
	 	category = object['category']
	 	title = object['title']
	 	pub_date = object['pub_date']
	 	text = str(id) + '-' + str(content_file)
	 	content = object['text']
	 	description = object['description']

	 	save_entry = {'id':id , 'keywords':keywords , 'likes':likes , 'comments':comments ,'category':category , 'text':text , 'pub_date':pub_date}
	 	save_content = {'id':id,'title':title,'description':description , 'content':content}

	 	f = open('count.txt','w')
	 	f.writelines(str(id))
	 	f.close();
	 	return (save_entry , save_content)
	
	def evaluate(self,query):
		'''
		evaluate(query) -> none
		query => string
		If the query is a valid query prints the result/results

		'''
		m = self.__validate(query)
		log_fh = open('logs/log.txt','a')
		if(m):

			start = datetime.now()
			groups = m.groups()
			selected_entries = []
			
			if(groups[0] != None):
				#This means that  ALL has been specified in the query and all the articles have to be displayed
				f = open('saved_content/content.txt' ,'r')

				for eachEntry in f:
					selected_entries.append(eval(eachEntry))

				f.close()
				self.__writelog(query,len(selected_entries))
				return self.__return_articles(selected_entries)
				

			elif(groups[0] == None and (groups[5] == None and groups[6] == None and groups[7] == None  and groups[8] == None and groups[9] == None)) :
				#This means that the query is with the a single projection and there is no conjunction
				selection = groups[1].lower()
				projection1 = groups[2].lower()
				operator1 = groups[3].lower()
				value1 = groups[4].lower()

				if value1 == "max":
					value1 =str(max(self.__find_max_min(projection1)))

				if value1 == "min":
					value1 =str(min(self.__find_max_min(projection1)))

				
				f = open("saved_entries/entries.txt","r")
				for eachEntry in f:
					if self.__filter_entries(eval(eachEntry),projection1,operator1,value1):
						selected_entries.append(eval(eachEntry))

				
				if selection == 'title' or selection == 'articles':	
					f.close()
					self.__writelog(query,len(selected_entries))
					return self.__selection(selected_entries, selection)
				else:

					if len(selected_entries) != 0:
						#This is a list that is used to return the information as JSON
						json_list = []

						for eachEntry in selected_entries:
							# print '#'*75
							# print str(selection).upper()+": " +eachEntry[selection]
							json_list.append({str(selection):str(eachEntry[selection])})
							# print '#'*75
							# print '\n'

						f.close();
						self.__writelog(query,len(selected_entries))
						return json_list				
					else:
						json_list = [{"error_code":"502"}]
						self.log_fh.writelines("Query:"+query+"No matching article"+str(datetime.now())+"\n")
						return json_list
						# print "No Matching article"


			else:
				#There is a second projection with a conjuction or a disjunction
				selection = groups[1].lower()
				projection1 = groups[2].lower()
				operator1 = groups[3].lower()
				value1 = groups[4].lower()
				conjuction_disjunction = groups[6].lower()
				projection2 = groups[7].lower()
				operator2 = groups[8].lower()
				value2 = groups[9].lower()
				
				if value1 == "max":
					value1 =str(max(self.__find_max_min(projection1)))

				if value1 == "min":
					value1 =str(min(self.__find_max_min(projection1)))

				if value2 == "max":
					value2 =str(max(self.__find_max_min(projection2)))

				if value2 == "min":
					value2 =str(min(self.__find_max_min(projection2)))

				
				f = open("saved_entries/entries.txt")
				for eachEntry in f:
					if self.__filter_entries(eval(eachEntry),projection1,operator1,value1,conjuction_disjunction,projection2,operator2,value2):
						selected_entries.append(eval(eachEntry))
				
				if selection == 'title' or selection == 'articles':	
					f.close()
					self.__writelog(query,len(selected_entries))
					return self.__selection(selected_entries, selection)
				else:
					if len(selected_entries) != 0:
						for eachEntry in selected_entries:
							# print '#'*50
							# print str(selection).upper()+": " +eachEntry[selection]
							json_list.append({str(selection):str(eachEntry[selection])})
							# print '#'*50
							# print '\n'
						f.close();
						self.__writelog(query,len(selected_entries))
						return json_list
					else:
						json_list = [{"error_code":"502"}]
						self.log_fh.writelines("Query:"+query+"No matching article"+str(datetime.now())+"\n")
						return json_list
						# print "No Matching article"

			end = datetime.now()
			print "Fetched "+str(len(selected_entries))+" entries in: "+str(end - start)+' second'
			self.log_fh.writelines("Query: "+query+" fetched "+str(len(selected_entries))+" entries @ "+str(datetime.now())+"\n")
		else:

			#This means this is an invalid query
			json_list = []
			#print "Invalid query"
			self.log_fh.writelines("Query: "+query+" Invalid query @ "+str(datetime.now())+"\n")
			json_list.append({'error_code':"500"})
			return json_list


		
	def __selection(self,entries_list,selection):
		# This is called only when the selection is articles or titles
		#This makes sure that the file content.txt has to be really opened
		selection = selection.lower()
		
		id_list = []
		for eachEntry in entries_list:
		 	id_list.append(int(eachEntry["text"].split("-")[0]))
		
		i = 0
		len_id_list = len(id_list)	

		if(len_id_list == 0):
			print "No Matching article"
			return

		f = open('saved_content/content.txt','r')
		json_list = []
		for eachEntry in f:
			each_entry = eval(eachEntry)
			if i < len_id_list:
				if each_entry['id'] == id_list[i]:
					if selection == "title":
						# print '#'*75
						# print str(selection.upper())+": "+each_entry[selection]
						json_list.append(dict(title=str(each_entry['title'])))
						i = i +1
						# print '#'*75
						# print '\n'
						
					else:
						#the selection is articles
						# print '#'*75
						json_list.append(dict(title=str(each_entry['title']),description=str(each_entry['description']),content=str(each_entry['content'])))
						# print "TITLE: " + each_entry['title']
						# print "DESCRIPTION: "+each_entry['description']
						# print "CONTENT: "+each_entry['content']
						i = i+1
						# print '#'*75
						# print '\n'
						

			else:
				break

		return json_list
								 
	def __filter_entries(self,entry,projection1,operator1,value1,conjunction_disjunction=None,projection2=None,operator2=None,value2=None):

		
		if conjunction_disjunction==None:
			if (isinstance(entry[projection1] , tuple)):
				#the projection is a tuple 
				return value1 in entry[projection1]			 	
				

			else:

				try:
					if(operator1 == '='):
						operator1 = '=='
					statement =  entry[projection1]+operator1+value1
					return eval(statement)
				except NameError:
					return False

		else:
			#Here  there is an and/or clause

			if(isinstance(entry[projection1],tuple) and isinstance(entry[projection2],tuple)):
				return eval((str(value1 in entry[projection1]) ) +"  " +conjunction_disjunction + " "+ (str(value2 in entry[projection2])))

			try:
				if(isinstance(entry[projection1],tuple)) and (isinstance(entry[projection2],str)):
					if(operator2 == '='):
						operator2 = '=='
					return eval((str(value1 in entry[projection1])) + " " +conjunction_disjunction+" "+str(eval(entry[projection2]+operator2+value2)))
			except NameError:
				return False

			try:
				if(isinstance(entry[projection1],str)) and (isinstance(entry[projection2],tuple)):
					if(operator1 == '='):
						operator1 = '=='
					return eval(str(eval(entry[projection1]+operator1+value1))+" "+conjunction_disjunction+" "+str(value2 in entry[projection2]))
			except NameError:
				return False

			try:
				if(isinstance(entry[projection1],str)) and (isinstance(entry[projection2],str)):
					if(operator1 == '='):
						operator1 = '=='
					if(operator2 == '='):
						operator2 = '=='

					return eval(str(eval(entry[projection1]+operator1+value1))+" "+conjunction_disjunction+" "+str(eval(entry[projection2]+operator2+value2)))
			except NameError:
				return False

	def __validate(self,query): 
		reg1 = "(SELECT ALL)"
		reg2 = "SELECT (TITLE|PUB_DATE|LIKES|COMMENTS|ARTICLES) WHERE"
		reg3 = "(CATEGORY|PUB_DATE|LIKES|COMMENTS|KEYWORDS)(=|<|>|<=|>=|!=)(\w+)"

		regex = reg1 + "|" + reg2+ " " + reg3 + "( (and|or) " + reg3 +")?"		

		m = re.match(regex,query)
		return m

	def __return_articles(self,list_):
		json_list = []
		
		for eachEntry in list_:
			json_list.append(dict(title=str(eachEntry['title']),description=str(eachEntry['description']),content=str(eachEntry['content'])))
		return json_list			


	def __find_max_min(self,likes_comments):
		likes_comments.lower()
		f = open('saved_entries/entries.txt','r')
		try:
			list_ = [ int(eval(eachLine)[likes_comments]) for eachLine in f] 
		except Exception:
			print "Invalid condition"
			self.log_fh.writelines("Invalid condition specified for maximum minimum....Maximum and minimum of COMMENTS and LIKES only can be found @ "+str(datetime.now())+"\n")
			sys.exit(1);
		finally:
			f.close()
		return list_

	def __del__(self):
		self.log_fh.close()

	def __writelog(self,query,no_of_selected_entries):
		self.log_fh.writelines("Query: "+query+" fetched "+str(no_of_selected_entries)+" entries @ "+str(datetime.now())+"\n")




if __name__ == "__main__":

		
		print '''
						######ARTICLE-NGIN#######
This is an article query engine.Query the past articles and enjoy reading them

THE KEYWORDS THAT ARE INCLUDED IN THE Article-ngin
	SELECT 
	ALL
	WHERE
	MAX
	MIN
	TITLE
	CATEGORY
	KEYWORDS
	PUB_DATE
	COMMENTS
	LIKES

	Querying model is as follows
		
	"SELECT ALL" selects all the entries in the database and displays them
	"SELECT TITLE WHERE CATEGORY=android" selects all the articles where the category = android

	Before the WHERE part is called as SELECTION and after the where part is called as PROJECTION
	THE  SELECTION part may contain the following keywords TITLE,PUB_DATE,LIKES,COMMENTS,ARTICLES
	THE PROJECTION part may contain the following keywords CATEGORY,PUB_DATE,LIKES,COMMENTS,KEYWORDS

	SELECT ARTICLES WHERE LIKES=MAX
	This selects the articles and displays the TITLE DESCRIPTION and TEXT which has the maximum number of likes 
	If there are many articles with the same number of articles then all of them will be displayed

	The operators supported are 
	>
	<
	>=
	<= 
	!=
	=

	SELECT ARTICLES WHERE LIKES > 20 
	selects all the articles having likes greater than 20

	CONJUCTION and DISJUNCTION support

	SELECT TITLE WHERE CATEGORY=android and LIKES=MAX
	This selects all the android articles having maximum number of likes and displays the title

	SELECT TITLE WHERE CATEGORY=android or CATEGORY=big-data
	SELECTS all the articles having cateogry as android or as big data  
	'''
	
		flag = True
		db = nudb()
		while flag == True:
			print"-"*150
			print"1.Save data"
			print"2.Query your favourite article"
			print"3.Exit"
			print"-"*150

			menu_choice = raw_input("Select the choice(Please enter the menu item number) \n")

			if(menu_choice == '1'):

				file_name = raw_input("Enter the file name where the input is present \n")
			 	fh = open(file_name,'r')
			 	list_ = []
			 	for eachLine in fh:
			 		list_.append(eval(eachLine))

			 	db.save(list_)
			 	fh.close();

			elif menu_choice == '2':
			 	query = raw_input('Enter the query: \n')
			 	db.evaluate(query)

			elif menu_choice == '3':
				flag = False

			else:
				print "Invalid choice"