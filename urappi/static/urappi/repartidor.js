document.querySelectorAll('.Image-container img').forEach(image=>{
image.onclick = ()=>{document.querySelector('.popup-im').style.display = "block";
document.querySelector('.popup-im img').src = image.getAttribute('src')


}
});

document.querySelector('.popup-im span').onclick = () =>{
document.querySelector('.popup-im').style.display = 'none';

}