// Smooth entrance animation

const elements = document.querySelectorAll('.animate');

const observer = new IntersectionObserver((entries) => {

entries.forEach(entry => {

if(entry.isIntersecting){

entry.target.classList.add('show');

}

});

},{
threshold:0.15
});

elements.forEach(el => {

observer.observe(el);

});



// Optional: Smooth scroll effect

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

anchor.addEventListener("click", function(e){

e.preventDefault();

document.querySelector(this.getAttribute("href")).scrollIntoView({

behavior:"smooth"

});

});

});
// Size selector highlight

const sizes = document.querySelectorAll('.size-options button');

sizes.forEach(size=>{
size.addEventListener('click',()=>{
sizes.forEach(btn=>btn.classList.remove('active'));
size.classList.add('active');
});
});
// Quantity buttons

document.querySelectorAll('.qty-btn').forEach(button=>{

button.addEventListener('click',()=>{

let span = button.parentElement.querySelector('span');
let value = parseInt(span.textContent);

if(button.textContent === "+"){
span.textContent = value + 1;
}

if(button.textContent === "-" && value > 1){
span.textContent = value - 1;
}

});

});
// Account page tabs

const tabs = document.querySelectorAll('.account-tab');
const panels = document.querySelectorAll('.account-panel');

tabs.forEach(tab => {

tab.addEventListener('click', () => {

tabs.forEach(t => t.classList.remove('active'));
panels.forEach(p => p.classList.remove('active'));

tab.classList.add('active');

document.getElementById(tab.dataset.tab).classList.add('active');

});

});
window.addEventListener("load", ()=>{
document.body.classList.add("fade-page");
setTimeout(()=>{
document.body.classList.add("active");
},100);
});
document.querySelectorAll('.product-img').forEach(img=>{

const original = img.src;
const hover = img.dataset.hover;

img.addEventListener('mouseenter',()=>{
img.src = hover;
});

img.addEventListener('mouseleave',()=>{
img.src = original;
});

});
const filterButtons = document.querySelectorAll('.filters button');
const products = document.querySelectorAll('.product-card');

filterButtons.forEach(btn=>{
btn.addEventListener('click',()=>{

const filter = btn.dataset.filter;

products.forEach(p=>{
if(filter === "all" || p.classList.contains(filter)){
p.style.display="block";
}else{
p.style.display="none";
}
});

});
});
const cursor = document.querySelector('.cursor');

document.addEventListener('mousemove', e => {
cursor.style.left = e.clientX + 'px';
cursor.style.top = e.clientY + 'px';
});
// Loader animation

window.addEventListener("load", ()=>{

setTimeout(()=>{
document.querySelector(".loader").style.opacity="0";

setTimeout(()=>{
document.querySelector(".loader").style.display="none";
},600);

},1500);

});
// change product image

const thumbs = document.querySelectorAll('.thumb');
const mainImage = document.getElementById('mainProductImage');

thumbs.forEach(thumb => {

thumb.addEventListener('click', ()=>{

mainImage.src = thumb.src;

});

});


// quantity

const plus = document.querySelector('.qty-plus');
const minus = document.querySelector('.qty-minus');
const qtyInput = document.querySelector('.qty-box input');

if(plus){

plus.addEventListener('click', ()=>{
qtyInput.value = parseInt(qtyInput.value) + 1;
});

}

if(minus){

minus.addEventListener('click', ()=>{
if(qtyInput.value > 1){
qtyInput.value = parseInt(qtyInput.value) - 1;
}
});

}
function changeShirt(src){
document.getElementById("shirtLayer").src = src;
}

function changePant(src){
document.getElementById("pantLayer").src = src;
}
function openTryOn(){
document.getElementById("tryonModal").classList.add("active");
}

function closeTryOn(){
document.getElementById("tryonModal").classList.remove("active");
}
let selectedRating = 0;

function setRating(rating){
selectedRating = rating;

document.querySelectorAll(".stars span").forEach((star, i)=>{
star.classList.toggle("active", i < rating);
});
}

function submitReview(){

const text = document.getElementById("reviewText").value;

if(!text || selectedRating === 0){
alert("Please add rating and review");
return;
}

const reviewHTML = `
<div class="review">
<p>${"★".repeat(selectedRating)}</p>
<p>${text}</p>
</div>
`;

document.getElementById("reviewsList").innerHTML += reviewHTML;

document.getElementById("reviewText").value = "";
selectedRating = 0;

document.querySelectorAll(".stars span").forEach(s => s.classList.remove("active"));
}
const user = JSON.parse(localStorage.getItem("user"));

if (!user || user.email !== "muskanpd2003@gmail.com") {
  const adminLink = document.querySelector(".admin-link");
  if (adminLink) adminLink.style.display = "none";
}