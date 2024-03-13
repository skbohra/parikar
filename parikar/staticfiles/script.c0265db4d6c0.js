/**
 * script.js
 * basic site-level funcitons 
 * related to navigation etc. reside here
 * jQuery based
 */



$(function(){

	var success_message = $(".success");
	var info_message = $(".error");
	var error_message = $(".info");
	var url = window.location;
	const params = new URLSearchParams(url.search);


	//using notify.js to convert django-messages into
	//disapperaing notification alerts

	$.notify(success_message.text(),"success");
	$.notify(info_message.text(),"info");
	$.notify(error_message.text(),"error");

	success_message.parent().hide();
	error_message.parent().hide();
	info_message.parent().hide();

	//search-button to submit form 
	$(".search-button").click(function(e){
		$(this).parent().submit();
	});


	//home page tabs switching based on url

	if(params.has("trending")){
		$("#tab-one").attr("checked","checked");
	}
	if(params.has("popular")){
		$("#tab-two").attr("checked","checked");
	}
	if(params.has("your")){
		$("#tab-three").attr("checked","checked");
	}



	$(".subscribe-channel").click(function(e){
		var button = $(this);
		e.preventDefault();
		var url = $(this).data('url');
		$.get(url,function(response){
			$(button).notify(response.message,response.type);
			if(response.type == "success"){
				$(button).toggleClass("btn-disabled").text(response.btn_text);
			}
		});
	});


});
