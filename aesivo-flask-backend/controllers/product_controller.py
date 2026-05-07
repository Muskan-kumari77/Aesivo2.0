from flask import jsonify, request
from db import get_db


# =========================
# GET ALL PRODUCTS
# supports: ?category=men&sort=price_asc&limit=20&offset=0
# =========================

def get_products():

    conn = get_db()

    category = request.args.get('category', None)
    sort     = request.args.get('sort', 'newest')
    limit    = int(request.args.get('limit', 20))
    offset   = int(request.args.get('offset', 0))

    sort_map = {
        'newest':     'id DESC',
        'price_asc':  'price ASC',
        'price_desc': 'price DESC',
        'rating':     'rating DESC',
        'name_asc':   'name ASC',
    }
    order = sort_map.get(sort, 'id DESC')

    if category:
        products = conn.execute(f"""
            SELECT * FROM products
            WHERE LOWER(category) = LOWER(?)
            ORDER BY {order}
            LIMIT ? OFFSET ?
        """, (category, limit, offset)).fetchall()

        total = conn.execute("""
            SELECT COUNT(*) FROM products
            WHERE LOWER(category) = LOWER(?)
        """, (category,)).fetchone()[0]
    else:
        products = conn.execute(f"""
            SELECT * FROM products
            ORDER BY {order}
            LIMIT ? OFFSET ?
        """, (limit, offset)).fetchall()

        total = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

    conn.close()

    return jsonify({
        "products": [dict(p) for p in products],
        "total":    total,
        "limit":    limit,
        "offset":   offset,
    })


# =========================
# GET BY CATEGORY (clean URL)
# GET /products/category/men
# =========================

def get_products_by_category(category):

    conn = get_db()

    sort   = request.args.get('sort', 'newest')
    limit  = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))

    sort_map = {
        'newest':     'id DESC',
        'price_asc':  'price ASC',
        'price_desc': 'price DESC',
        'rating':     'rating DESC',
        'name_asc':   'name ASC',
    }
    order = sort_map.get(sort, 'id DESC')

    products = conn.execute(f"""
        SELECT * FROM products
        WHERE LOWER(category) = LOWER(?)
        ORDER BY {order}
        LIMIT ? OFFSET ?
    """, (category, limit, offset)).fetchall()

    total = conn.execute("""
        SELECT COUNT(*) FROM products
        WHERE LOWER(category) = LOWER(?)
    """, (category,)).fetchone()[0]

    conn.close()

    return jsonify({
        "products": [dict(p) for p in products],
        "total":    total,
        "limit":    limit,
        "offset":   offset,
    })
def get_products_by_category(category):

    conn = get_db()

    products = conn.execute("""
        SELECT * FROM products
        WHERE category=?
        ORDER BY rating DESC, id DESC
    """,(category,)).fetchall()

    conn.close()

    return jsonify({
        "total": len(products),
        "products":[dict(x) for x in products]
    })

# =========================
# GET SINGLE PRODUCT
# =========================

def get_product(id):

    conn = get_db()

    product = conn.execute("""
        SELECT * FROM products
        WHERE id=?
    """,(id,)).fetchone()

    conn.close()

    if not product:
        return jsonify({"error":"Product not found"}),404

    return jsonify(dict(product))
# =========================
# RELATED PRODUCTS
# =========================

def related_products(id):

    conn = get_db()

    product = conn.execute(
        "SELECT category FROM products WHERE id = ?", (id,)
    ).fetchone()

    if product and product["category"]:
        products = conn.execute("""
            SELECT * FROM products
            WHERE id != ? AND LOWER(category) = LOWER(?)
            ORDER BY RANDOM()
            LIMIT 4
        """, (id, product["category"])).fetchall()

        if len(products) < 4:
            existing_ids = [p["id"] for p in products] + [id]
            placeholders = ",".join("?" * len(existing_ids))
            extra = conn.execute(f"""
                SELECT * FROM products
                WHERE id NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            """, (*existing_ids, 4 - len(products))).fetchall()
            products = list(products) + list(extra)
    else:
        products = conn.execute("""
            SELECT * FROM products
            WHERE id != ?
            ORDER BY RANDOM()
            LIMIT 4
        """, (id,)).fetchall()

    conn.close()

    return jsonify([dict(p) for p in products])


# =========================
# GET REVIEWS
# =========================

def get_reviews(id):

    conn = get_db()

    reviews = conn.execute("""
        SELECT * FROM reviews
        WHERE product_id = ?
        ORDER BY id DESC
    """, (id,)).fetchall()

    conn.close()

    return jsonify([dict(r) for r in reviews])


# =========================
# ADD REVIEW
# =========================

def add_review(id):

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    reviewer_name = data.get("reviewer_name", "Anonymous")
    rating        = data.get("rating", 5)
    title         = data.get("title", "")
    text          = data.get("text", "")
    image         = data.get("image", None)

    if not text:
        return jsonify({"error": "Review text is required"}), 400

    conn = get_db()

    conn.execute("""
        INSERT INTO reviews (product_id, reviewer_name, rating, title, text, image)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id, reviewer_name, rating, title, text, image))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Review submitted successfully"}), 201