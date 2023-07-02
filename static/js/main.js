var i=0;

var icon = document.getElementById('dark')

var change_icon = () =>{
    if(i==0){
        i=1;
        icon.innerHTML="<i class='bi bi-moon on'></i>"
        document.getElementsByTagName('body')[0].style.backgroundColor = "black"
        document.getElementsByTagName('body')[0].style.color = "white"
        document.getElementById('about').style.backgroundColor = "black"
        document.getElementById('container4').style.backgroundColor = "black"
        document.getElementById('container').style.backgroundColor = "black"
    }
    else{
        i=0;
        icon.innerHTML="<i class='bi bi-brightness-high on'></i>"
        document.getElementsByTagName('body')[0].style.backgroundColor = "white"
        document.getElementsByTagName('body')[0].style.color = "black"
        document.getElementById('about').style.backgroundColor = "white"
        document.getElementById('container').style.backgroundColor = "white"
        document.getElementById('container4').style.backgroundColor = "white"
    }
}
