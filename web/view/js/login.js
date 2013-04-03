(function(){
								
			
			var formWrapper = $('#form-wrapper')
						
			$('#have-sign-in').on('click', function(){

			formWrapper.toggleClass("flipped")
			
			});

			$('#go-back').on('click' , function(){
								
				formWrapper.toggleClass("flipped");
							
			});
						
						
})();



$("#sign-up").on('submit',function(event){

		console.log("Form submitted");
		var sign_up_name = $('#sign-up-name').val();
		var sign_up_password = $('#sign-up-password').val();
		var sign_up_confirm_password = $("#sign-up-confirm-password").val();
		var sign_up_email = $("#sign-up-email").val();

		if(sign_up_name == "" || sign_up_password == "" || sign_up_confirm_password == "" || sign_up_email == "")
		{
			var toast = new Toast("All the fields must be entered!!")
			toast.makeToast();
		}

		
		else if (sign_up_password != sign_up_confirm_password)
		{
			setTimeout(function(){

				var toast = new Toast("Passwords dont match!!!");
				toast.makeToast();	

			},500)
			
		}

		else{


		var sign_up_object = {
			type:"sign_up",
			user_name:sign_up_name,
			password:sign_up_password,
			sign_up_email:sign_up_email
		}


		$.post('http://localhost:9000',JSON.stringify(sign_up_object),function(data, textStatus, xhr) {
					//optional stuff to do after success
					var json_object = $.parseJSON(data);

					if(json_object.status === "success")
					{
						
						var toast = new Toast("Signed up successfully");
						toast.makeToast();	

						

						var formWrapper = $('#form-wrapper')
						formWrapper.toggleClass("flipped")

					}

					if(json_object.status === "error")
					{

						var toast = new Toast("User name already exits");
						toast.makeToast();	
					}


			});
		


	 }//end of else


		event.preventDefault();

});//End of submit handler


$("#sign-in").on('submit',function(event){

	var user_name = $('#sign-in-user-name').val();
	var password = $('#sign-in-password').val();

	if(user_name == '' || password == '')
	{
		var toast = new Toast("All the fields must be entered");
		toast.makeToast();
	}

	else
	{
		var sign_in_obj = {
			type:"sign_in",
			user_name:user_name,
			password:password

		}

		$.post('http://localhost:9000', JSON.stringify(sign_in_obj), function(data, textStatus, xhr) {
			//optional stuff to do after success
			var json_object = $.parseJSON(data)

			if(json_object.status === "success")
					{
						
						window.location.replace("../html/article.html");

					}

					if(json_object.status === "error")
					{

						var toast = new Toast("Wrong credentials!!!!!");
						toast.makeToast();	
					}

		});
		
	}


	event.preventDefault();
})