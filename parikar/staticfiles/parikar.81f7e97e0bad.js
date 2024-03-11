
function animation(parik,record_view_url,view_progress){
view_progress = parseInt(view_progress)/10.0;
gsap.registerPlugin(MotionPathPlugin, EasePack);
//gsap.registerPlugin(MotionPathPlugin, SplitText, Physics2DPlugin, ScrambleTextPlugin, EasePack)

var noSleep = new NoSleep();
noSleep.enable(); // keep the screen on!
var line = $('.line');

var tl = new TimelineLite({
			onComplete: function(){
				tl.restart();
			}
		});

if(view_progress != 10.0){
	TweenLite.to(tl, 1, {progress: view_progress/10.0, ease: Linear.easeNone});
}
TweenLite.defaultEase = Circ.easeInOut;

var time = 0.9;
var y = 100;

if (parik == "default"){
tl
	.add ( TweenMax.staggerFromTo (
		line, time,
			{
				opacity: 0,
				delay:0.9,
				y:y,
				autoAlpha:0
			},
			{	
				opacity: 1,
				autoAlpha:1,
				y: 0,
			},
		2 ))
	.add ( TweenMax.staggerTo (
		line, time,
			{
				delay: time,
				opacity: 0,
				autoAlpha:0,
				y: -y,
			},
		2 ), 1.3)

var total_duration = new Date(tl.totalDuration() * 1000).toISOString().slice(11, 19);

$(".total-time").text(total_duration);
} 

if (parik == "horizontal"){

tl
	.add ( TweenMax.staggerFromTo (
		line, time,
			{
				opacity: 0,
				x:-y,
			},
			{	
				opacity: 1,
				y: 0,
			},
		2 )).addLabel("blueGreenSpin", "+=1")
	.add ( TweenMax.staggerTo (
		line, time,
			{
				delay: time,
				opacity: 0,
				x: y,
			},
		2 ), 1.3)


}


$(".speed-button").click(function(e){

e.preventDefault();
var action = $(this).data("state");
$(".speed-button").parent().removeClass("active-speed");
$(this).parent().addClass("active-speed");


if(action == "fast"){
	tl.timeScale(1.5);
}
if(action == "normal"){
	tl.timeScale(1);
}
if(action == "slow"){
	tl.timeScale(0.75);
}
if(action == "slower"){
	tl.timeScale(0.4);
}





});

var sliderValue = {value:0};
var slider = $("#ctrl_slider");

slider.slider({
  range: false,
  min: 0,
  max: 100,
  step:.1,
  start:function() {
    tl.pause();
  },
  slide: function ( event, ui ) {
    tl.progress( ui.value / 100 );
  },
  stop:function() {
    tl.play();
  }
});

/*
var slider = new RangeSliderPips({
  target: document.getElementById("#ctrl_slider"),
  props: {
    min: -50,
    max: 50,
    pips: true,
    pipstep: 1,
    all: "label",
    float: true,
    handleFormatter: (v) => {
      return v;
    }
  }
});
*/

/*
var slider = new RangeSliderPips({
    target: document.querySelector("#ctrl_slider"),
    props: { values: [100], pips: true,pipstep: 1,float:true,    suffix: "%" }
  });

slider.$on('change', function(e) {
  tl.progress( e.detail.value / 100 );
});
*/

var current_progress = 0.0;
tl.eventCallback("onUpdate", function() {
  sliderValue.value = tl.progress() * 100;
  slider.slider(sliderValue);
  //slider.$set({ values: [ tl.progress()*100 ]});

  var time_elapsed = new Date(tl.totalTime() * 1000).toISOString().slice(11, 19);
  $(".time-elapsed").text(time_elapsed);
  
  if(parseInt(tl.progress()*100.00) != current_progress){
	console.log(parseInt(tl.progress()*100.00));
  	var url = record_view_url + "&progress=" + parseInt(tl.progress()*100.00);
        current_progress = parseInt(tl.progress()*100.00);	
  	$.get(url,function(response){});


  }
  });
tl.eventCallback("onComplete", function() {
  gsap.to(slider, 1, {autoAlpha:1});
  //replayReveal();
});

$(".video-control-pause").click(function(e){
e.preventDefault();
var state = $(this).data("state");
if (state == "play"){
	//pauses wherever the playhead currently is:
	tl.pause();
	$(this).data("state","pause");
	$(this).text("Play");
	$('.play-pause-icon').toggleClass("iconoir-pause");
	$('.play-pause-icon').toggleClass("iconoir-play");
	$.notify("Paused","info");
} else{
	tl.play();
	$(this).data("state","play");
	$(this).text("Pause");
	$('.play-pause-icon').toggleClass("iconoir-pause");
	$('.play-pause-icon').toggleClass("iconoir-play");
	$.notify("Playing","info");

	}
});



$(".line-comment").on("click",function(e) {
if ($(this).css('opacity') == 1) {
e.stopPropagation()
e.preventDefault();

$(".video-control-pause").click();
var line_id = $(this).data("line") ;
var line  = $("#"+line_id).text();

$(".popup-data").text(line);

$(".popup").fadeIn(500);

}
});
$(".close").click(function() {
  $(".popup").fadeOut(500);
$(".video-control-pause").click();
});



$(".video").click(function(){
$(".video-control-pause").click();
});

$(".line-comment").hover(function(){
$(".video-control-pause").click();
},
function(){

$(".video-control-pause").click();
}
);



$(function(){


$(".subscribe-channel").click(function(e){

	e.preventDefault();
	var url = $(this).data('url');
	$.get(url,function(response){
	$(".subscribe-channel").notify(response.message,response.type);
	if(response.type == "success"){
		$(".subscribe-channel").toggleClass("btn-disabled").text(response.btn_text);
	}
	});
});



});



}





