from datetime import datetime
from random import randint
keywords_category = ['android','mobile','mobility','big_data','ios','iphone','hp','cisco','smart-phone','dell','apple-mac','samsung','htc','google','twitter','facebook','microsoft']

#This decides the number of entries in the dummy database
no_entries = 10000
max_categories = 5
max_keywords = 3
#maximum length of the title
title_max = 30

#maximum length of the description
description_max = 50

#maximum length of the text
text_max = 600
f = open('input.txt','w')

for i in xrange(0,no_entries):
	number_categories = randint(1,max_categories) 
	#This choses the number of categories for the entry


	categories_list = []
	categories_tuple = ()
	for i in xrange(0,number_categories):
		
		 rand_int = randint(0,len(keywords_category)-1)
		 #This is done to make sure that if same random number is generated then the catgeory is not repeated in the category tuple
		 if keywords_category[rand_int] not in categories_list:
		 	categories_list.append(keywords_category[rand_int])


	for eachElement in categories_list:
		categories_tuple = categories_tuple + (eachElement,)



	number_keywords = randint(1,max_keywords)

	keywords_list = []
	keywords_tuple = ()

	for i in xrange(0,number_keywords):
		rand_int = randint(0,len(keywords_category)-1)

		if keywords_category[rand_int] not in keywords_list:
			keywords_list.append(keywords_category[rand_int])

	for eachElement in keywords_list:
		keywords_tuple = keywords_tuple + (eachElement,)


	#97 and 122 is the bounds of the lower case characters in ASCII and hence used
	title = "".join([chr(randint(97,122)) for i in xrange(0,randint(1,title_max))])
	description = "".join([chr(randint(97,122)) for i in xrange(0,randint(1,description_max))])
	text = "".join([ chr(randint(97,122)) for i in xrange(0,randint(1,text_max))])

	max_likes = 200
	max_comments = 200
	likes = str(randint(0,max_likes))
	comments = str(randint(0,max_comments))
	pub_date = str(datetime.now())

	f.writelines(str(dict(category=categories_tuple,likes=likes,comments=comments,title=title,keywords=keywords_tuple,description=description,text=text,pub_date = pub_date)))
	f.writelines('\n')

f.close()