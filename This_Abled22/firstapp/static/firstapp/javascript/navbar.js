var ch = document.getElementById("check");
var cm = document.getElementById("com");
var me = document.getElementById("me");

var cd = document.getElementById("check_drop");
var ld = document.getElementById("login_drop");

var ch_num = 0; var me_num = 0; 

ch.addEventListener('click', () => {
    ch_num += 1;

    ch.style.color = "#3c096c";
    cm.style.color = "#757575";
    me.style.color = "#757575";

    if (ch_num%2!=0) { //홀수
        cd.style.display = "block";
    }
    else {
        cd.style.display = "none";
    }
})

me.addEventListener('click', () => {
    me_num += 1;

    ch.style.color = "#757575";
    cm.style.color = "#757575";
    me.style.color = "#3c096c";
    
    if (me_num%2!=0) { //홀수
        ld.style.display = "block";
    }
    else {
        ld.style.display = "none";
    }
})

cm.addEventListener('click', () => {
    ch.style.color = "#757575";
    cm.style.color = "#3c096c";
    me.style.color = "#757575";
})