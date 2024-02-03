

function animation(parik){
gsap.registerPlugin(MotionPathPlugin, EasePack);

var line = $('.line');

var tl = new TimelineLite({
			onComplete: function(){
				tl.restart();
			}
		});

 
TweenLite.defaultEase = Circ.easeInOut;

var time = 0.9;
var y = 100;

if (parik == "default"){
tl
	.add ( TweenMax.staggerFromTo (
		line, time,
			{
				opacity: 0,
				y:y,
			},
			{	
				opacity: 1,
				y: 0,
			},
		2 ))
	.add ( TweenMax.staggerTo (
		line, time,
			{
				delay: time,
				opacity: 0,
				y: -y,
			},
		2 ), 1.3)
} 

if (parik == "why"){

	whyGSAP(tl,line);
}

var slider = $("#ctrl_slider");
var sliderValue = {value:0};
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

tl.eventCallback("onUpdate", function() {
  sliderValue.value = tl.progress() * 100;
  slider.slider(sliderValue);
});
tl.eventCallback("onComplete", function() {
  gsap.to(slider, 1, {autoAlpha:1});
  //replayReveal();
});

$(".video-control-pause").click(function(){
var state = $(this).data("state");
if (state == "play"){
	//pauses wherever the playhead currently is:
	tl.pause();
	$(this).data("state","pause");
	$(this).text("Play");
} else{
	tl.play();
	$(this).data("state","play");
	$(this).text("Pause");

	}
});

function whyGSAP(tl,text) {
      var split = new SplitText(".line", {type:"chars,words"}),
      chars = split.chars,
      centerIndex = Math.floor(chars.length / 2),
      i;
  for (i = 0; i < chars.length; i++) {
    tl.from(chars[i], {x:(i - centerIndex) * 40, opacity:0, duration: 1.8, ease: "power2"}, i * 0.1);
  }
  tl.fromTo(text, {z:500, y:74, visibility:"visible"}, {z:-1000, ease:"slow(0.1, 0.9)", duration: 4}, 0);
  tl.to(text, {rotationX:-720, autoAlpha:0, scale:0.3, duration: 1.5, ease:"power2.inOut"}, "-=1.5");
  return tl;
}

}
