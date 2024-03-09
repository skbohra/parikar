var menuIcon = document.querySelector(".menu-icon");
var sidebar = document.querySelector(".sidebar");
var container = document.querySelector(".container");

menuIcon.onclick = function(){
    sidebar.classList.toggle("small-sidebar");
    container.classList.toggle("large-container");
}


$(function(){
$(".search-button").click(function(e){

	$(this).parent().submit();
});
var success_message = $(".success");
var info_message = $(".error");
var error_message = $(".info");

$.notify(success_message.text(),"success");
$.notify(info_message.text(),"info");
$.notify(error_message.text(),"error");
success_message.parent().hide();
error_message.parent().hide();
info_message.parent().hide();

$(".search-button").click(function(){

	$(".search-form").submit();
});

});
