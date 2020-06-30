from flask import Blueprint, jsonify

from alegrosz.dbs.dbs import get_db

category_bp = Blueprint('category', __name__, url_prefix='/categories')


@category_bp.route('/<int:category_id>')
def category(category_id):
    c = get_db().cursor()

    c.execute("""SELECT id, name FROM subcategories
        WHERE category_id=?""", (category_id,))

    subcategories = c.fetchall()

    return jsonify(subcategories=subcategories)
