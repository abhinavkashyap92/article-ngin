from bs4 import BeautifulSoup
import urllib
import re
from datetime import datetime
from datetime import timedelta
from db_config import get_connection


def scrap(url):

	try:
		html_object = urllib.urlopen(url)

	except IOError:
		print "There is an error in opening the url"
		return

	html_text = html_object.read()

	#---------------------------------------------------------Get the keyword associated with the article--------------------------------------------------

	tag_ = url[7:].split('/')
	keyword = tag_[len(tag_)-1]
	print keyword

	#---------------------------------------------------------Find the contents of the post that is made--------------------------------------------------

	soup = BeautifulSoup(html_text)

	#Find the post that is made in the webpage
	divs_post = soup.find_all('div',id=re.compile("post-(\d+)"))

	if len(divs_post) != 0:
		the_top_article = str(divs_post[0])

	else:
		return

	#---------------------------------------------------------Find the name of the author of the post------------------------------------------------------

	soup_top_article = BeautifulSoup(the_top_article)
	author_name = soup_top_article.find('span',class_="name")

	if author_name != None:
		author_name = author_name.string.encode("utf-8")

	else:
		return

	#---------------------------------------------------------Find the title of the article----------------------------------------------------------------

	title = soup_top_article.find('h2',class_="headline")
	print title	

	if title != None:
		title= title.find('a').string.encode("utf-8").replace("\n","").replace("\t","").strip()

	else:
		return

	#---------------------------------------------------------Find the description of the article----------------------------------------------------------

	#The description of the article is found in a div with a class of body-copy
	if soup_top_article.find("div",class_ = "body-copy"):
		description = [string for string in soup_top_article.find("div",class_="body-copy").find('p').strings]
		description = " ".join([string.encode("utf-8") for string in description])
		description = description.replace("\n","").replace("\t","").strip()

	else:
		return

	#---------------------------------------------------------Find the date of publish of the article------------------------------------------------------

	#The time posted is found in a div with a class of post-time
	date = soup_top_article.find("div",class_="post-time").string

	if date != None:

		mins_ago = 0
		if "posted" in date:

			#This means that the article has been posted recently and time can be obtained with respect to the current time

			#This handles entries like "posted yesterday"
			if "yesterday" in date:
				mins_ago = 24 * 60

			#This handles entries like "posted 1 hour ago","posted 25 mins ago"
			else:
				date_ = date[7:].split(' ')
				number_ = date_[0]
				hours_mins = date_[1]

				if hours_mins == "hour" or "hours":
					mins_ago = 60

				else:
					mins_ago = number_

			date_published = datetime.now() - timedelta(minutes = mins_ago)
		

		else:

			month_dictionary = {"january":1 , "february":2 , "march":3 , "april":4 , "may":5 , "june":6 , "july":7 ,"august":8 , "september":9,"october":10,"november":11 , "december":12}

			#They have mentioned a date in the date_published and has to be converted into proper date and time object
			date = date.replace(",","").replace("th","").replace("st","").replace("nd","").replace("rd","")
			date = [string.encode("utf-8") for string in date.split(" ")]
			date_published = datetime(int(date[2]) , int(month_dictionary[date[0].lower()]) , int(date[1]))
			print date_published

	else:
		return


	#---------------------------------------------------------Find the detail content of the article---------------------------------------------------
	
	#For this find the read more link and open it 
	read_more_url = soup_top_article.find("a",class_="more-link")

	if read_more_url != None:
		#create a soup of the actual contents of the article
		read_more_url = read_more_url.get("href")
		try:
			soup_content = BeautifulSoup(urllib.urlopen(read_more_url).read())
			all_ps = [each_p for each_p in soup_content.find("div","body-copy").find_all("p")]

			content = ""
			for eachP in all_ps:
				content = content +  " ".join([string.encode("utf-8") for string in eachP.strings])

			content = content.replace("\n","").replace("\t","").strip()


	#---------------------------------------------------------Find the detail tags associated with the article---------------------------------------------

			#The tags are found within a div with a class of single tags

			tags = soup_content.find("div",class_="single-tags").find_all("a")
			tags_tuple = ()

			if len(tags) != 0:
				for eachAnchorTag in tags:
					tags_tuple = tags_tuple + (eachAnchorTag.string.encode("utf-8"),)

			else:
				tags_tuple = (keyword,)

		except IOError:
			print "There is an error in opening the url"
	
	else:
		return

	return dict(_id=title , title=title , author_name = author_name , description = description , content = content , date_published = date_published , keyword = keyword , tags = tags_tuple)

if __name__ == '__main__':
	
	db = get_connection()
	collection = db['articles']
	json_list = []
	categories_list = ['aol','android','amazon','apple','facebook','google','groupon','ipad','iphone','linkedin','microsoft','samsung','square','twitter','yahoo','zynga']

	for eachCategory in categories_list:
		dict_ = scrap("http://techcrunch.com/tag/"+eachCategory)
		if dict_ is not None:
			json_list.append(dict_)
	

	collection.insert(json_list)