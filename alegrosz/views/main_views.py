from flask import Blueprint, render_template, send_from_directory, request

from alegrosz.dbs.dbs import get_db
from alegrosz.forms.item_forms import FilterForm
from alegrosz.utils.utils import upload_path

main_bp = Blueprint('main', __name__, url_prefix="/")


@main_bp.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(upload_path, filename)


@main_bp.route('/')
def home():
    conn = get_db()
    c = conn.cursor()

    form = FilterForm(request.args, meta={"csrf": False})

    c.execute("SELECT id, name FROM categories")
    categories = c.fetchall()
    categories.insert(0, (0, "---"))
    form.category.choices = categories

    c.execute("SELECT id, name FROM subcategories WHERE category_id = ?", (1,))
    subcategories = c.fetchall()
    subcategories.insert(0, (0, "---"))
    form.subcategory.choices = subcategories

    query = """SELECT
        i.id, i.title, i.description, i.price, i.image, c.name, s.name
        FROM
        items AS i
        INNER JOIN categories AS c ON i.category_id = c.id
        INNER JOIN subcategories AS s ON i.subcategory_id = s.id
    """

    if form.validate():

        filter_queries = []
        parameters = []

        if form.title.data.strip():
            filter_queries.append("i.title LIKE ?")
            parameters.append(f"%{form.title.data}%")

        if form.category.data:
            filter_queries.append("i.category_id = ?")
            parameters.append(form.category.data)

        if form.subcategory.data:
            filter_queries.append("i.subcategory_id = ?")
            parameters.append(form.subcategory.data)

        if filter_queries:
            query += "  WHERE "
            query += " AND ".join(filter_queries)

        if form.price.data:
            if form.price.data == 1:
                query += " ORDER BY i.price DESC"
            else:
                query += " ORDER BY i.price"
        else:
            query += " ORDER BY i.id DESC"

        items_from_db = c.execute(query, tuple(parameters))
    else:
        items_from_db = c.execute(query + " ORDER BY i.id DESC")

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

    return render_template('home.html', items=items, form=form)
