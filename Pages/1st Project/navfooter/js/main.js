// code for side nav bar

$(".sideTrgr").click(function(){
    $(".sideNabBar").toggleClass("sideInactive");
})

$(".sideSubMenuHead").click(function(){
    $(".sideSubMenu").slideToggle(300);
    $("#sideDownArrow").toggleClass("rotate");
})