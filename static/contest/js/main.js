var tabBtn1 = document.getElementById("tabBtn1");
var tabBtn2 = document.getElementById("tabBtn2");
var tabBtn3 = document.getElementById("tabBtn3");
var constTab1 = document.getElementById("tab1");
var constTab2 = document.getElementById("tab2");
var constTab3 = document.getElementById("tab3");
function tab1(){
    tabBtn1.classList.add("clickedBtn");
    tabBtn2.classList.remove("clickedBtn");
    tabBtn3.classList.remove("clickedBtn");
    constTab1.style.transform = "translateX(0px)";
    constTab2.style.transform = "translateX(-100%)";
    constTab3.style.transform = "translateX(-100%)";
}
function tab2(){
    tabBtn2.classList.add("clickedBtn");
    tabBtn1.classList.remove("clickedBtn");
    tabBtn3.classList.remove("clickedBtn");
    constTab2.style.transform = "translateX(0px)";
    constTab1.style.transform = "translateX(-100%)";
    constTab3.style.transform = "translateX(-100%)";
}
function tab3(){
    tabBtn3.classList.add("clickedBtn");
    tabBtn2.classList.remove("clickedBtn");
    tabBtn1.classList.remove("clickedBtn");
    constTab3.style.transform = "translateX(0px)";
    constTab2.style.transform = "translateX(-100%)";
    constTab1.style.transform = "translateX(-100%)";
}


