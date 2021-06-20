
$(document).ready(()=> {

    var active_tab = "#blog";

    $(".tab-body").html($("#blog").html());

    $("#blog_btn").on("click",()=>{
        $(".tab-body").html($("#blog").html())
    })

    $("#camp_btn").on("click",()=>{
        $(".tab-body").html($("#camp").html())
    })

    $("#rsrc_btn").on("click",()=>{
        $(".tab-body").html($("#resources").html())
    })

    $("#sbmsn_btn").on("click",()=>{
        $(".tab-body").html($("#submissions").html())
    })

})

