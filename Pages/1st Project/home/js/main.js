$(".owl-carousel").owlCarousel({
    items: 4,
    margin:15,
    nav: true,
    // loop:true,
    // autoplay:true,
    autoplayTimeout:1500,
    autoplayHoverPause:true,
    responsive:{
        0:{
            items:1,
        },
        580:{
            items:2,
        },
        780:{
            items:3,
        },
        1000:{
            items:3,
        },
        1200:{
            items:4
        }
    }
});

// code for side nav bar

$(".sideTrgr").click(function(){
    $(".sideNabBar").toggleClass("sideInactive");
})

$(".sideSubMenuHead").click(function(){
    $(".sideSubMenu").slideToggle(300);
    $("#sideDownArrow").toggleClass("rotate");
})