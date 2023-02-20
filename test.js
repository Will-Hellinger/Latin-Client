var gid = 1;
var aid = 1100000043;
var thisresponse = 'the next day as soon as he was aroused from sleep, hercules noticed the theft and looked for the lost oxen in all places';
var newDenom = 1;
$.post(
"feedback.php",
[{name:"why",value:"grasp_score"},{name:"denom",value:newDenom},{name:"aid",value:aid},{name:"score", value:100},{name:"gid",value:gid},{name:"response",value:thisresponse}],
function(data){
    console.log(data);
	switch(data){
		case "yes":
		    score = $(".green").length;
		    scorenow = Math.round(100*(score/newDenom));
		    $.post("feedback.php",[{name:"why",value:"grasp_score_uptick"},{name:"denom",value:newDenom},{name:"aid",value:aid},{name:"score",value:scorenow},{name:"gid",value:gid},{name:"response",value:thisresponse}]);
		    break;
	}
	score = $(".green").length;
	score = Math.round(100*(score/newDenom));
	console.log(score);
    $(".showScore").text(score+"% correct");
});