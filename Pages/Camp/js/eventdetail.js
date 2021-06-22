let form =document.getElementById("form");
form.addEventListener('focusin', (event) =>{
    event.target.style.background = "white";
    event.target.style.border = "2px solid #38b6ff";
});

form.addEventListener('focusout', (event) =>{
    event.target.style.background = "transparent";
    event.target.style.border = "2px solid #d4d4d4";
});


let nameFiled = document.getElementById("name");
let mailFiled = document.getElementById("email");
let phnumFiled = document.getElementById("number");
// let divWidth = window.screen.width;

window.addEventListener('resize', () =>{
    var divWidth = window.screen.width;
    // console.log(divWidth);
    width(divWidth);
})
window.addEventListener('load', () =>{
    var divWidth = window.screen.width;
    // console.log(divWidth);
    width(divWidth);
})

function width(px){
    if(px < 350){
        nameFiled.setAttribute("placeholder", "Name*");
        mailFiled.setAttribute("placeholder", "Email*");
        phnumFiled.setAttribute("placeholder", "Phone Number*");
    }else{
        nameFiled.setAttribute("placeholder", "Enter Your Name*");
        mailFiled.setAttribute("placeholder", "Enter Your Email*");
        phnumFiled.setAttribute("placeholder", "Enter Your Number*");
    }
}