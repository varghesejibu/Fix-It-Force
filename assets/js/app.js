
const hamb = document.querySelector('[data-hamburger]');
const drawer = document.querySelector('[data-drawer]');
if(hamb && drawer){
  hamb.addEventListener('click', ()=> drawer.classList.toggle('open'));
}
