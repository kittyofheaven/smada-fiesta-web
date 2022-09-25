let bg = document.querySelector('#prx_bg');
let cloud = document.querySelector('#cloud');
let rocks = document.querySelector('#rocks');
let text = document.querySelector('#prx_text');

window.addEventListener('scroll', function() {
    let value = window.scrollY;
    bg.style.top = value * 0.5 + 'px';
    // moon.style.left = -value * 0.5 + 'px';
    cloud.style.top = -value * 0.15 + 'px';
    rocks.style.top = value * 0.15 + 'px';
    text.style.top = value * 1 + 'px';
})

window.addEventListener('scroll', reveal);
function reveal(){
    var reveals = document.querySelectorAll('.reveal');

    for(var i = 0; i < reveals.length; i++){

        var windowheight = window.innerHeight;
        var revealtop = reveals[i].getBoundingClientRect().top;
        var revealpoint = 150;

        if(revealtop < windowheight - revealpoint){
            reveals[i].classList.add('active');
        }
        else{
            reveals[i].classList.remove('active');
        }
    }
}

const card = document.querySelectorAll('.card-inner');

card.forEach(card => {
    card.addEventListener('click', function(){
        card.classList.toggle('is-flipped');
    });
});

//      resize upperParallaxBox function
function upperParallaxBoxResize(){
    let client_width = document.documentElement.clientWidth;
    let upperParallaxBox = document.querySelector('.parallaxUpperBox');
    if (client_width <= 350 ){
        upperParallaxBox.style.height = "35vh";
    }
    else {
        let upperParallaxBox_height = 620*20/client_width;
        upperParallaxBox_height = Math.round(upperParallaxBox_height); 
        upperParallaxBox.style.height = (upperParallaxBox_height.toString() + 'vh');
    }
}
upperParallaxBoxResize();
//       resize col-1 function
function parallaxResize(){
    let parallax = document.querySelector('.parallax');
    let client_width = document.documentElement.clientWidth;
    let p_height = client_width/1192 * 175;
    p_height = Math.round(p_height-15);
    parallax.style.height = (p_height.toString()+"vh");
}
parallaxResize()
//      end resize function

window.addEventListener("resize", function(){
    parallaxResize();
    upperParallaxBoxResize();
});

var menuList = document.getElementById("menu-list");
// menuList.style.maxHeight = "0px";

function togglemenu(){
    if (x.matches) {
        if(menuList.style.maxHeight == "0px"){
            menuList.style.maxHeight = "130px";
        }
        else{
            menuList.style.maxHeight = "0px";
        }
    }
    else {
        
    }
}

var x = window.matchMedia("(max-width: 768px)")
togglemenu(x) // Call listener function at run time
x.addListener(togglemenu) // Attach listener function on state changes
