const ques = {
    banglaName:"প্রশ্নের বাংলা নাম",
    banglaQues: "বাংলা ভাষা বঙ্গভূমির অধিবাসীদের মাতৃভাষা, যা ভারতের অঙ্গরাজ্য পশ্চিমবঙ্গ এবং বর্তমান জাতিরাষ্ট্র বাংলাদেশ নিয়ে গঠিত। লন্ডনের বৃহৎ বাঙালী অভিবাসীদের আবাস ব্রিকলেনে বাংলা ভাষা মূল অঞ্চলের পাশাপাশি ত্রিপুরা,দক্ষিণ আসাম এবং ভারতীয় ",
    englishName:"Problem Name Here",
    englishQues: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus dolore aperiam dicta exercitationem eos tempora sunt perferendis voluptatum qui placeat corporis facere quos quisquam accusantium, quae, fugit explicabo laborum soluta omnis vero ",
}

// deafult ques lagnuage
$(".quesName h4").text(ques.englishName);
$(".quesTxt").text(ques.englishQues);

function changeLang(){
    if($("#optLang").text() == "Bangla"){
        $(".lang p span").text("Bangla");
        $("#optLang").text("English");
        $(".quesTxt").text(ques.banglaQues);
        $(".quesName h4").text(ques.banglaName);

    }else if($("#optLang").text() == "English"){
        $(".lang p span").text("English");
        $("#optLang").text("Bangla");
        $(".quesTxt").text(ques.englishQues);
        $(".quesName h4").text(ques.englishName);
    }
}