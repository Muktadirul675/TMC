
var second = 0;

const cross_login = () => {
    $("#login_board").css({"display":"none"});
}

const count = () => {
    second++;
    if(second == 2){
        $("#login_board").css({"transform-origin":"left","transform":"scaleX(1)"});
    }
    if(second > 2){
        clearInterval(timer);
    }
}

var timer = setInterval(count, 1000);

$(function (){
    $('[data-toggle="tooltip"]').tooltip()
})

$("table").togleClass("table table-striped table-bordered table-hover");


