/*
fb: https://www.facebook.com/sharer.php?u=[post-url]
twt: https://twitter.com/share?url=[post-url]&text=[post-title]&via=[via]&hashtags=[hashtags]
whats: https://api.whatsapp.com/send?text=[post-title] [post-url]
lnkin: https://www.linkedin.com/shareArticle?url=[post-url]&title=[post-title]
*/

let title = document.getElementById("title").innerHTML;
let img = document.getElementById("contestImg").src;
let pageUrl = document.location.href;
let facebookBtn = document.getElementById("facebook");
let twitterBtn = document.getElementById("twitter");
let whatsappBtn = document.getElementById("whatsapp");
let linkedinBtn = document.getElementById("linkedin");

function btninit(){
    facebookBtn.setAttribute("href", `https://www.facebook.com/sharer.php?u=${pageUrl}`);
    twitterBtn.setAttribute("href", `https://twitter.com/share?url=${pageUrl}&text=${title}`);
    whatsappBtn.setAttribute("href", `https://api.whatsapp.com/send?text=${title} ${pageUrl}`);
    linkedinBtn.setAttribute("href", `https://www.linkedin.com/shareArticle?url=${pageUrl}&title=${title}`);
}
btninit();