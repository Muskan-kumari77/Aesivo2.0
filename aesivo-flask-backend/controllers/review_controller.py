from flask import request, jsonify
from db import get_db

# Add Review
def add_review():
    data = request.json

    conn = get_db()
    conn.execute("""
        INSERT INTO reviews (product_id, rating, comment)
        VALUES (?, ?, ?)
    """, (
        data["product_id"],
        data["rating"],
        data.get("comment")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Review added"}), 201


# Get Reviews
def get_reviews(product_id):
    conn = get_db()

    reviews = conn.execute(
        "SELECT * FROM reviews WHERE product_id=?",
        (product_id,)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in reviews])