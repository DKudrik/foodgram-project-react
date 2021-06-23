let prev_element = document.getElementsByClassName('nav__item nav__item_active');


function change_class() {
  prev_element[0].className = ('nav__item');
  this.className = ('nav__item nav__item_active');
  return;
}


prev_element[0].addEventListener('click', change_class);
console.log(this.classList.className);