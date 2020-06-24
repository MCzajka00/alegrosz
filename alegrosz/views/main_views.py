from flask import Blueprint, render_template, send_from_directory

from alegrosz.dbs.dbs import get_db
from alegrosz.utils.utils import upload_path

main_bp = Blueprint('main', __name__, url_prefix="/")


@main_bp.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(upload_path, filename)


@main_bp.route('/')
def home():
    conn = get_db()
    c = conn.cursor()

    c.execute("""SELECT
        i.id, i.title, i.description, i.price, i.image, c.name, s.name
        FROM
        items AS i
        INNER JOIN categories AS c ON i.category_id = c.id
        INNER JOIN subcategories AS s ON i.subcategory_id = s.id
    """)

    items_from_db = c.fetchall()
    items = []
    for row in items_from_db:
        item = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "image": row[4],
            "category": row[5],
            "subcategory": row[6]
        }
        items.append(item)

    return render_template('home.html', items=items)
