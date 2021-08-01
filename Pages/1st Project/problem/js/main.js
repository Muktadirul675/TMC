$(".problemContainer").html($("#allProbs").html())
$(".allProb").addClass("active");

function tab(p){
    if(p == 1){
        $(".problemContainer").html($("#allProbs").html())
        $(".allProb").addClass("active");
        $(".solvedProb").removeClass("active");
        $(".unsolvedProb").removeClass("active");
    }else if(p == 2){
        $(".problemContainer").html($("#solvedProbs").html())
        $(".solvedProb").addClass("active")
        $(".allProb").removeClass("active")
        $(".unsolvedProb").removeClass("active")
    }else if(p == 3){
        $(".problemContainer").html($("#unsolvedProbs").html())
        $(".unsolvedProb").addClass("active")
        $(".solvedProb").removeClass("active")
        $(".allProb").removeClass("active")
    }
}