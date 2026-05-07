import os

from flask import Flask, render_template, jsonify  # type: ignore
from flask_cors import CORS  # type: ignore

# ROUTES
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.order_route import order_bp
from routes.review_routes import review_bp
from routes.cart_routes import cart_bp
from routes.contact_routes import contact_bp
from routes.admin_routes import admin_bp
from routes.payment_routes import payment_bp

from db import get_db

# =========================
# CREATE APP
# =========================
app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.config["SECRET_KEY"] = "aesivo-super-secret"

# =========================
# CORS
# =========================
CORS(app)

# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(order_bp, url_prefix="/api/orders")
app.register_blueprint(review_bp, url_prefix="/api/reviews")
app.register_blueprint(cart_bp, url_prefix="/api/cart")
app.register_blueprint(contact_bp, url_prefix="/api/contact")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(payment_bp, url_prefix="/api/payment")

# =========================
# FRONTEND ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/collection")
def collection():
    return render_template("collection.html")

@app.route("/men")
def men():
    return render_template("men.html")

@app.route("/women")
def women():
    return render_template("women.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/orders")
def orders():
    return render_template("orders.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/tryon")
def tryon_page():
    return render_template("tryon.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/shipping")
def shipping():
    return render_template("shipping.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


# =========================
# ADMIN DATA (SECURE THIS LATER WITH JWT)
# =========================
@app.route("/api/admin/contacts")
def get_contacts():
    conn = get_db()
    data = conn.execute(
        "SELECT * FROM contact ORDER BY created_at DESC"
    ).fetchall()

    return jsonify([dict(x) for x in data])


# =========================
# HEALTH CHECK
# =========================
@app.route("/api/health")
def health():
    return jsonify({"status": "OK"})


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


    
