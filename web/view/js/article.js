$(function(){

	//This says that the document is loaded now 
	var session_json = {

		type:"session_check",
	}

	$.post('http://localhost:9000', JSON.stringify(session_json), function(data) {
		//optional stuff to do after success
		console.log(data);
	});
	




});


$('#query').on('submit',function(event){

	var query_entered = $('#user-query').val();

	var json_obj = {
		type:"query",
		query:query_entered
	}

	$.post('http://localhost:9000', JSON.stringify(json_obj), function(data) {
		//optional stuff; to do after success
		var json_obj = $.parseJSON(data)

		if(json_obj.status == "error")
		{
			console.log("There is an error")
			var toast = new Toast("There is an error in the query!");
			toast.makeToast();

		}

		else if(json_obj.status == "no_matching_articles")
		{
			console.log("There are no matching articles for your query");
			var toast = new Toast("There are no matching articles!!!!")
			toast.makeToast();
		}

		else{

			console.log("This is entering")
			$json_reply = $.parseJSON(data)
			show_fetched_articles($json_reply)
			
		}
	});

	event.preventDefault();
	
	
});



function show_fetched_articles($json_data)
{
	var nudbArticles = {

		init:function(config){

			this.container = config.container;
			this.template = config.template;
			this.json_data = config.json_data;
			this.required_list = new Array();
			this.refresh();
			this.getArticles();

		},

		
		getArticles:function(){

				//iterate over the json_data and call the attach Template function

				$.each(this.json_data , function(index , json_object){
					
					//This here gets every json object
					//This is iterated over again and the following properties ar packaged into a dictionary and then added to the required lis
					// 1.title
					// 2.author_name
					// 3.description
					// 4.Content

					console.log
					nudbArticles.required_list.push({
							thumbnail:'../images/techcrunch.jpg',
							title:json_object['title'],
							author_name:json_object['author_name'],
							date_published:json_object['date_published'],
							description:json_object['description'],
							content:json_object['content']
					})// end of push



				})//end of each function

				this.attachTemplate();

		},

		attachTemplate:function()
		{
			var template = Handlebars.compile(this.template);
			this.container.append(template(this.required_list));
		},

		refresh:function(){

			//find all the div's in the document and then remove it
			$('div.article').remove()
			var $div_articleContent = $('div.article_content')
			$div_articleContent.slideUp(1000 , function(){

				$(this).remove();
			});


		}


	};


	nudbArticles.init({

		container:$('div.articles_container'),
		template:$('#article_template').html(), 
		json_data:$json_data

	});

	$('.title').on('click', function(){


	//once the title is hovered then hide all the sibling articles
	$title = $(this);

	// Find the parent of the title tag that is clicked
	$div_article = $title.closest('div.article');

	//Find the body wrapper that is present in the dom
	//This will be used to add the content of the article
	$body_wrapper = $div_article.parent('div.articles_container');

	//Find all the sibling articles and all of these will be hidden first
	$sibling_articles = $div_article.siblings('div.article');

	//This is the div that is to be shown that is the actual content of the article
	$article_content = $div_article.children('div.article_content')
	console.log($article_content)


	$div_article.slideUp(400, function(){

		if($sibling_articles.length != 0)
		{
			$sibling_articles.slideUp(400);
		}

		$article_content.appendTo($body_wrapper).show({

				duration:1000,
				easing:'linear'

			})
	})

	

	$go_back_icon = $article_content.find('span.icon-undo')

	// The back button on the article is clicked
	$go_back_icon.on('click',function(){

		
		give_everything_back($article_content,$div_article,$body_wrapper)


	})

})//End of the title click event


function give_everything_back($article_content , $div_article , $body_wrapper)
{
	
	// 1.Add the article content back to the div where it belongs
	// 2.Hide the article content again
	// 3.Find all the article in the body and show again
	$article_content.appendTo($div_article).hide();

	$all_articles = $body_wrapper.find('div.article').slideDown(1500);

}


}
// end of show fetched articles function


