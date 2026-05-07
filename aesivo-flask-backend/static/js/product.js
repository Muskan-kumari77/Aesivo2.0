let selectedSize = null;
let currentProduct = null;


// LOAD PRODUCT FROM BACKEND
async function loadProduct() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  if (!id) {
    alert("Product not found");
    return;
  }

  const res = await fetch(`/api/products/${id}`);
  const product = await res.json();

  currentProduct = product;

  document.getElementById("productName").innerText = product.name;
  document.getElementById("productPrice").innerText = "₹" + product.price;
}


// SIZE SELECT
function selectSize(btn) {
  document.querySelectorAll(".size-options button")
    .forEach(b => b.classList.remove("active"));

  btn.classList.add("active");
  selectedSize = btn.innerText;
}


// QUANTITY
function changeQty(change) {
  let qtyInput = document.getElementById("qty");
  let qty = parseInt(qtyInput.value);

  qty += change;
  if (qty < 1) qty = 1;

  qtyInput.value = qty;
}


// ADD TO CART (BACKEND)
async function addToCart() {

  const user = JSON.parse(localStorage.getItem("user"));

  if (!user) {
    alert("Please login first");
    window.location.href = "/account";
    return;
  }

  if (!selectedSize) {
    alert("Please select size");
    return;
  }

  const quantity = parseInt(document.getElementById("qty").value);

  const res = await fetch("/api/cart/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      user_id: user.id,
      product_id: currentProduct.id,
      quantity: quantity
    })
  });

  if (res.ok) {
    alert("Added to cart!");
  } else {
    alert("Error adding to cart");
  }
}


// AUTO LOAD
loadProduct();