from db import get_db


# =========================
# GET SINGLE PRODUCT
# =========================

def get_product(product_id):
    conn = get_db()
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()
    return product


# =========================
# GET ALL PRODUCTS
# =========================

def get_all_products():
    conn = get_db()
    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return products


# =========================
# GET RELATED PRODUCTS
# =========================

def get_related_products(product_id, category=None, limit=4):
    conn = get_db()

    if category:
        products = conn.execute("""
            SELECT * FROM products
            WHERE id != ? AND category = ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (product_id, category, limit)).fetchall()

        # Top up with random products if not enough in same category
        if len(products) < limit:
            existing_ids = [p["id"] for p in products] + [product_id]
            placeholders = ",".join("?" * len(existing_ids))
            extra = conn.execute(f"""
                SELECT * FROM products
                WHERE id NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            """, (*existing_ids, limit - len(products))).fetchall()
            products = list(products) + list(extra)
    else:
        products = conn.execute("""
            SELECT * FROM products
            WHERE id != ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (product_id, limit)).fetchall()

    conn.close()
    return products


# =========================
# GET REVIEWS
# =========================

def get_reviews(product_id):
    conn = get_db()
    reviews = conn.execute("""
        SELECT * FROM reviews
        WHERE product_id = ?
        ORDER BY id DESC
    """, (product_id,)).fetchall()
    conn.close()
    return reviews


# =========================
# ADD REVIEW
# =========================

def add_review(product_id, reviewer_name, rating, title, text, image=None):
    conn = get_db()
    conn.execute("""
        INSERT INTO reviews (product_id, reviewer_name, rating, title, text, image)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (product_id, reviewer_name, rating, title, text, image))
    conn.commit()
    conn.close()