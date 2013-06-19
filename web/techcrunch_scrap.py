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
	
	# ------------------------------------Get the keyword associated with the article------------------------------------------------------------------------------
	
	tag_ = url[7:].split('/')
	keyword = tag_[len(tag_)-1]
	print keyword

	# ------------------------------------Find the contents of the post that is made------------------------------------------------------------------------------
		
	#Now the file is obtained with the html content inside it 
	#Now according to the page that is obtained there is a div with the following syntax <div id="post-somenumber">
	#now use regular expression to obtain this

	#The website keeps on updating articles and the most recent article is the one on the top
	#in post-somenumber the somenumber part is always unique and identifies the article
	#This can also be obtained
	#To enable getting the articles regularly the top article alone is obtained and scrapped

	article_post_regex = r'<div id="post-(\d+)"(.*?)>(.*?)</div><!-- #post-## -->'
	#This heavily depends on the each post ending with the <!-- #post-## --> tag

	# The top article is got by the first index of the list that is returned by the following regex
	# Every element of the list is a tuple 
	# The first element of the tuple gives the article identification provided by the website
	# The last one gives the actual contents in the div
	div_post_contents = re.findall(article_post_regex,html_text,re.DOTALL)

	if(len(div_post_contents)!= 0):
		article_id = div_post_contents[0][0]
		html_text = div_post_contents[0][2]
		html_text.replace(" ","")
	else:
		return

	# ------------------------------------Find the author of the article------------------------------------------------------------------------------

	#The authors are containd in a span <span class="name">author name</span>
	author_regex = r'<span class="name">(.*?)</span>'
	authors_list = re.findall(author_regex , html_text , re.DOTALL)

	if(len(authors_list) != 0):
		print  authors_list[0]
			
	else:
		return
	

	# ------------------------------------Find the headline of the article------------------------------------------------------------------------------

	headline_regex = r'<h2 class="headline">(.*?)</h2>'
	headline_list = re.findall(headline_regex,html_text,re.DOTALL);


	if(len(headline_list) != 0):
		# This list only contains the anchor tags surrounding the headline
		#This contains all the white spaces and other troublesome characters which are removed in the next step
		anchor_tags_wrapping_haeadlines = []

		
		for eachString in headline_list:
			eachString = eachString.replace("\n","")
			eachString = eachString.replace("\r","")
			eachString = eachString.strip()
			anchor_tags_wrapping_haeadlines.append(eachString)

		title_regex = r'<a href="(.*)">(.*)</a>'

		title_list = []
		for eachString in anchor_tags_wrapping_haeadlines:
			list_ = re.findall(title_regex,eachString,re.DOTALL)
			title_list.append(list_[0][1].strip().replace("\n","").replace("\t",""))
			
		# print repr(title_list)
	else:
		return


	# ------------------------------------Find the description  of the article------------------------------------------------------------------------------
	
	decription_div_regex = r'<div class="body-copy">(.*?)</div>'
	description_div_list = re.findall(decription_div_regex,html_text,re.DOTALL)

	if(len(description_div_list) != 0):
		description = description_div_list[0].strip().replace("\r","").replace("\t","")

		#here the paragraph tag is also included in the description
		#let us remove it by taking the inner HTML of the paragraph tag
		description_innerHTML_regex = r'<p>(.*?)</p>'
		description_innerHTML = re.findall(description_innerHTML_regex,description)

		#There will be a read more anchor tag at the last and the index of this is searched and then the description is sliced till here
		slice_till_here =description_innerHTML[0].index('<a')
		description_innerHTML= description_innerHTML[0][:slice_till_here]
		# print description_innerHTML
		#Here the description is got

		#Now get the url where the actual contents of the article is found
		find_a_in_description = r'<a href="(.*?)"(.*?)>(.*?)</a>'
		a_tag = re.findall(find_a_in_description,description,re.DOTALL)
		url_article = a_tag[0][0]


		

	else:
		#This shows that the div is not obtained
		#Chuck the article
		#inconsistent markup
		return

	# ------------------------------------Get the contents of the artice------------------------------------------------------------------------------
	
	# Here the url of the artice is navigated to and then the body-copy div is obtained
	#All the paragraph tags inside the article gives us the content of the article
	try:
		html_content_object = urllib.urlopen(url_article)
		
	
	except IOError:
		print "There is an error in opening the url"
		return

	html_content_file  = html_content_object.read()
	# print html_conent_file

	body_copy_regex = r'<div class="body-copy">(.*?)</div>'
	content_inside_div = re.findall(body_copy_regex,html_content_file,re.DOTALL)[0].strip().replace("\r","").replace("\t","");
	#Now everything that is inside the div is found out

	#now find only the p tags inside this div
	find_p_regex = r'<p>(.*?)</p>'
	all_ps = re.findall(find_p_regex,content_inside_div,re.DOTALL);
	# all_ps contain all the p tags inside the content of the div
	# Every p tag is an element of the list
	# Hence the length of the list is the number of p tags that is got


	final_content = '\n'.join(all_ps)
	# print final_content

	# ------------------------------------Get the publication date from the page------------------------------------------------------------------------------

	#The publication time information is contained in the div with a class of postime

	post_time_regex = r'<div class="post-time">(.*?)</div>'
	get_timeline = re.findall(post_time_regex,html_content_file,re.DOTALL)[0][7:]
	#why 7 is used in slicing?? that is because we want to remove the word posted from the string
	
	if(len(get_timeline) != 0):

		if re.findall(post_time_regex,html_content_file,re.DOTALL)[0][0:6] != "posted":
			mins_ago = 0

		elif get_timeline == "yesterday":

			mins_ago = 24 *60

		else:
			get_time_regex = r'(\d*) (\w*) ago'

			#Here we assume that the article is got within an hour atleast where it is posted
			# This is bound to happen because the article is scrapped at regular intervals
			get_time = re.findall(get_time_regex,get_timeline)


			number_ = int(get_time[0][0])
			
			hours_mins = get_time[0][1]
			# print hours_mins

			if hours_mins == "hours" or hours_mins == "hour":
				mins_ago = number_ * 60

			else:
				mins_ago = number_


		# Subtract the current time with the mins_ago to get the actual publishing date and time
		dt = datetime.now()  - timedelta(minutes=mins_ago)
		#time delta gives the time from the current time
		time_str = dt
		
		#This gives the string representation of the time
		# time_str = dt.strftime("%A, %d %B %Y %I:%M%p")
		# print time_str

	else:
		return

	# ------------------------------------Get the tags associated with the article------------------------------------------------------------------------------

	# The tags are contained in a div with a class of single-tags and inside it are the anchor tags that contain the tags
	tags_div_regex = r'<div class="single-tags">(.*?)</div>'
	all_anchors_list = re.findall(tags_div_regex , html_content_file,re.DOTALL)

	#some times it is found that the page doesnt have the tags bar at the bottom
	#in this case the tags is made equal to the keyword
	if len(all_anchors_list) != 0:
		all_anchors_list[0] = all_anchors_list[0][6:]
		

		a_inner_html = r'<a (.*?)>(.*?)</a>'
		a_list = re.findall(a_inner_html , all_anchors_list[0])

		tags_tuple = ()

		for i in range(len(a_list)):
			tags_tuple = tags_tuple + (a_list[i][1],)


	else:
		tags_tuple = (keyword,)

	# print tags_tuple

	return dict(_id= article_id,title=title_list[0],author_name=authors_list[0],description=description_innerHTML,content=final_content,date_published=time_str,keyword=keyword,tags=tags_tuple)

def main():

	db = get_connection()
	collection = db['articles']
	json_list = []
	categories_list = ['aol','android','amazon','apple','facebook','google','groupon','ipad','iphone','linkedin','microsoft','samsung','square','twitter','yahoo','zynga']

	for eachCategory in categories_list:
		dict_ = scrap("http://techcrunch.com/tag/"+eachCategory)
		if dict_ is not None:
			json_list.append(dict_)
	
	try:
		collection.insert(json_list)

	except Exception:
		print "There is an error in handling"


	

if __name__ == '__main__':
	main()