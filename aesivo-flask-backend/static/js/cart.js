async function loadCart() {

  const user = JSON.parse(localStorage.getItem("user"));
  const container = document.getElementById("cartItems");

  if (!user) {
    container.innerHTML = "<p>Please login</p>";
    return;
  }

  const res = await fetch(`/api/cart/${user.id}`);
  const items = await res.json();

  let total = 0;
  container.innerHTML = "";

  items.forEach(item => {
    total += item.price * item.quantity;

    container.innerHTML += `
      <div class="cart-item">
        <h3>${item.name}</h3>
        <p>₹${item.price}</p>
        <p>Qty: ${item.quantity}</p>
        <button onclick="removeItem(${item.id})">Remove</button>
      </div>
    `;
  });

  document.getElementById("total").innerText = "₹" + total;
}

async function removeItem(id) {
  await fetch(`/api/cart/remove/${id}`, { method: "DELETE" });
  loadCart();
}

loadCart();