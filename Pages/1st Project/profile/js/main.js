const tabBtn1 = document.getElementsByClassName("tabBtn1")[0];
const tabBtn2 = document.getElementsByClassName("tabBtn2")[0];
const tabBtn3 = document.getElementsByClassName("tabBtn3")[0];
const tabBtn4 = document.getElementsByClassName("tabBtn4")[0];

const tabBtnAlt1 = document.getElementsByClassName("tabBtn1")[1];
const tabBtnAlt2 = document.getElementsByClassName("tabBtn2")[1];
const tabBtnAlt3 = document.getElementsByClassName("tabBtn3")[1];
const tabBtnAlt4 = document.getElementsByClassName("tabBtn4")[1];

const tab1 = document.getElementById("tab1");
const tab2 = document.getElementById("tab2");
const tab3 = document.getElementById("tab3");
const tab4 = document.getElementById("tab4");

const altSelectorDiv = document.querySelector('#selection');
const altSelector = document.querySelector('#selectionTxt');
const altTab = document.querySelector(".altTab");
const altSelectorIcon = altSelectorDiv.querySelector(".fa-chevron-down");


// default
tab2.style.display = 'none';
tab3.style.display = 'none';
tab4.style.display = 'none';
altSelector.innerHTML = document.getElementsByClassName("clickedBtn")[0].innerHTML;

function opntab1(){
    tab1.style.display = 'block';
    tab2.style.display = 'none';
    tab3.style.display = 'none';
    tab4.style.display = 'none';
    tabBtn1.classList.add("clickedBtn");
    tabBtn2.classList.remove("clickedBtn");
    tabBtn3.classList.remove("clickedBtn");
    tabBtn4.classList.remove("clickedBtn");
    tabBtnAlt1.classList.add("clickedBtn");
    tabBtnAlt2.classList.remove("clickedBtn");
    tabBtnAlt3.classList.remove("clickedBtn");
    tabBtnAlt4.classList.remove("clickedBtn");
    altTab.classList.remove("altSelectAct")
    altSelector.innerHTML = document.getElementsByClassName("clickedBtn")[0].innerHTML;
}
function opntab2(){
    tab2.style.display = 'block';
    tab1.style.display = 'none';
    tab3.style.display = 'none';
    tab4.style.display = 'none';
    tabBtn2.classList.add("clickedBtn");
    tabBtn1.classList.remove("clickedBtn");
    tabBtn3.classList.remove("clickedBtn");
    tabBtn4.classList.remove("clickedBtn");
    tabBtnAlt2.classList.add("clickedBtn");
    tabBtnAlt1.classList.remove("clickedBtn");
    tabBtnAlt3.classList.remove("clickedBtn");
    tabBtnAlt4.classList.remove("clickedBtn");
    altTab.classList.remove("altSelectAct")
    altSelector.innerHTML = document.getElementsByClassName("clickedBtn")[0].innerHTML;
}
function opntab3(){
    tab3.style.display = 'block';
    tab2.style.display = 'none';
    tab1.style.display = 'none';
    tab4.style.display = 'none';
    tabBtn3.classList.add("clickedBtn");
    tabBtn2.classList.remove("clickedBtn");
    tabBtn1.classList.remove("clickedBtn");
    tabBtn4.classList.remove("clickedBtn");
    tabBtnAlt3.classList.add("clickedBtn");
    tabBtnAlt2.classList.remove("clickedBtn");
    tabBtnAlt1.classList.remove("clickedBtn");
    tabBtnAlt4.classList.remove("clickedBtn");
    altTab.classList.remove("altSelectAct")
    altSelector.innerHTML = document.getElementsByClassName("clickedBtn")[0].innerHTML;
}
function opntab4(){
    tab4.style.display = 'block';
    tab2.style.display = 'none';
    tab3.style.display = 'none';
    tab1.style.display = 'none';
    tabBtn4.classList.add("clickedBtn");
    tabBtn2.classList.remove("clickedBtn");
    tabBtn3.classList.remove("clickedBtn");
    tabBtn1.classList.remove("clickedBtn");
    tabBtnAlt4.classList.add("clickedBtn");
    tabBtnAlt2.classList.remove("clickedBtn");
    tabBtnAlt3.classList.remove("clickedBtn");
    tabBtnAlt1.classList.remove("clickedBtn");
    altTab.classList.remove("altSelectAct")
    altSelector.innerHTML = document.getElementsByClassName("clickedBtn")[0].innerHTML;
}

altSelectorDiv.addEventListener('click', ()=>{
    altTab.classList.toggle("altSelectAct");
    altSelectorIcon.classList.toggle("scaleInvrs");
});


// ------- progress section events
const progressUpArrow = document.getElementById("upArrow");
const progressDownArrow = document.getElementById("downArrow");
const pgrsbarcontainer = document.querySelector('.progressBarContainer');
const pgrsshowbtn = document.getElementById("divShowBtn");

progressDownArrow.addEventListener('click', () =>{
    pgrsbarcontainer.style.webkitMaskImage = 'none';
    pgrsbarcontainer.style.height = '100%';
    progressDownArrow.style.display = 'none';
    progressUpArrow.style.display = 'block';
});

progressUpArrow.addEventListener('click', () =>{
    pgrsbarcontainer.style.webkitMaskImage = 'linear-gradient(180deg, black, #00000042)';
    pgrsbarcontainer.style.height = '180px';
    progressDownArrow.style.display = 'block';
    progressUpArrow.style.display = 'none';
});

// ------- progress bar settings sample

// var allQuesNum = Number(document.querySelector(".combAll").innerHTML);
// var solvdNum = Number(document.querySelector(".combSolved").innerHTML);

// function initWidth(totNum, solvedNum){
//     return (solvedNum / totNum) * 100;
// };

// var progressBar = document.querySelector(".progressBar");
// progressBar.style.width = initWidth(allQuesNum, solvdNum) + '%';

var allQuesNum = document.getElementsByClassName("combAll");
var solvdNum = document.getElementsByClassName("combSolved");
var progressBar = document.getElementsByClassName("progressBar");

for(i = 0; i < allQuesNum.length; i++){
    var totNum = Number(allQuesNum[i].innerHTML);
    var sNum = Number(solvdNum[i].innerHTML);
    var percent = (sNum / totNum) * 100;
    progressBar[i].style.width = percent + '%';
}


// creating chart

var can1 = document.getElementById('ratingData').getContext('2d');
var myChart = new Chart(can1, {
    type: 'line',
    data: {
        labels: ['1st', '2nd', '3rd', '4th', '5th'],
        datasets: [{
            lineTension: 0.2,
            data: [2, 4, 3, 2, 3],
            backgroundColor:[
                'rgba(255, 121, 112)',
                'rgba(111, 170, 83)',
                'rgba(0, 153, 255)',
                'rgba(255, 255, 0)',
                'rgba(181, 90, 48)',
            ],
            borderColor:'#867b7b',
            pointRadius: 5,
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                grid:{
                    display: false,
                }
            },
            x:{
                display: false,
                grid:{
                    display: false,
                }
            }
        },
        responsive: true,
        plugins:{
            legend: {
                display: false,
            }
        }
    },
});
var can2 = document.getElementById('verdicts').getContext('2d');
var myChart = new Chart(can2, {
    type: 'polarArea',
    data: {
        labels: ['Accepted', 'Wrong Answer', 'Submitted'],
        datasets: [{
            label: 'jj',
            data: [22, 8, 30],
            backgroundColor:[
                'rgb(0, 153, 51)',
                'rgb(255, 64, 0)',
                'rgb(0, 153, 255)',
            ],
            borderColor:'#fff',
            borderWidth: 2,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                display: false,
            }
        },
        responsive: true,
        plugins:{
            legend:{
                labels:{
                    boxWidth: 30,
                    boxHeight: 15
                },
                display: false,
            }
        }
    },
    }
);
// options.plugins.legend.labels