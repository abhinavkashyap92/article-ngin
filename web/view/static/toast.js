function Toast(text,width,height)
{
	
	this.toast_text = text||'Please enter a text';
	this.width = width||'280';
	this.height = height||'35';
	this.border_radius ='8px';
	this.div='body';
	this.toast = this.createToast();
}

Toast.prototype.createToast = function()
{
	//This is creatin a toast with desired properties and appending to the body of the document
	var $toast = this;
	var toast = $('<div></div>')
	.css({
		'display':'none',
		'position':'absolute',
		'top':'0',
		'background-color':'rgba(74,81,158,0.5)',
		'width':$toast.width,
		'height':$toast.height,
		'border-radius':$toast.border_radius,
		'color':'rgba(7,11,82,1)',
		'text-align':'left',
		'padding-top':$toast.height/2,
		'padding-left':'5',
		'font-family':"PlayBall , cursive",
		'font-size':'1.3em',
		'font-weight':'bold',
		'margin-left':function(){

		 	return  ($(window).width()/2)- (parseInt($toast.width)/2);
		 },
	})
	.appendTo($toast.div);

	return toast;
}

Toast.prototype.makeToast = function()
{
	
	var $toast = this.toast;

	$toast
	.text(this.toast_text)
	.fadeIn({

		duration:1500,
		complete:function(){
			$toast.fadeOut(1500);
		}

	});


}
