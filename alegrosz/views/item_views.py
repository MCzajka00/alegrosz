from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_wtf.file import FileRequired

from alegrosz.dbs.dbs import get_db
from alegrosz.forms.comment_forms import NewCommentForm
from alegrosz.forms.item_forms import ItemForm, NewItemForm, DeleteItemForm, EditItemForm
from alegrosz.utils.utils import save_image_upload

item_bp = Blueprint("item", __name__, url_prefix="/items")


@item_bp.route("/<int:item_id>")
def item(item_id):
    c = get_db().cursor()
    c.execute("""SELECT
        i.id, i.title, i.description, i.price, i.image, c.name, s.name
        FROM
        items AS i
        INNER JOIN categories AS c ON i.category_id = c.id
        INNER JOIN subcategories AS s ON i.subcategory_id = s.id
        WHERE i.id = ?""", (item_id,))

    row = c.fetchone()

    try:
        good = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "image": row[4],
            "category": row[5],
            "subcategory": row[6]
        }
    except IndexError:
        good = {}

    if good:
        comments_from_db = c.execute("""SELECT content FROM comments
        WHERE item_id = ? ORDER BY id DESC""", (item_id,))

        comments = [{"content": row[0]} for row in comments_from_db]

        comment_form = NewCommentForm()
        comment_form.item_id.data = item_id

        delete_item_form = DeleteItemForm()

        return render_template("item.html", item=good, deleteItemForm=delete_item_form, comments=comments,
                               commentForm=comment_form)
    return redirect(url_for('main.home'))


@item_bp.route("/add", methods=['GET', 'POST'])
def add_item():
    conn = get_db()
    c = conn.cursor()

    form = NewItemForm()

    c.execute("SELECT id, name FROM categories")
    categories = c.fetchall()
    form.category.choices = categories

    c.execute("""SELECT id, name FROM subcategories
                WHERE category_id = ?""",
              (1,)
              )
    subcategories = c.fetchall()
    form.subcategory.choices = subcategories

    if form.validate_on_submit() and form.image.validate(form, extra_validators=(FileRequired(),)):
        filename = save_image_upload(form.image)

        c.execute("""INSERT INTO items
            (title, description, price, image, category_id, subcategory_id)
            VALUES (?, ?, ?, ?, ?, ?)""",
                  (
                      form.title.data,
                      form.description.data,
                      float(form.price.data),
                      filename,
                      form.category.data,
                      form.subcategory.data
                  )
                  )
        conn.commit()
        flash(f"Item {form.title.data} has been successfully submitted.", "success")
        return redirect(url_for("main.home"))
    return render_template("new_item.html", form=form)


@item_bp.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    row = c.fetchone()

    try:
        good = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "image": row[4],
        }
    except IndexError:
        good = {}

    if good:
        form = EditItemForm()
        if form.validate_on_submit():
            filename = good["image"]
            if form.image.data:
                filename = save_image_upload(form.image)

            c.execute("""UPDATE items SET
            title = ?, description = ?, price = ?, image = ?
            WHERE id = ?""", (
                form.title.data,
                form.description.data,
                float(form.price.data),
                filename,
                item_id
            ))

            conn.commit()

            flash(f"Item {form.title.data} has been successfully updated.", "success")
            return redirect(url_for("item.item", item_id=item_id))

        form.title.data = good["title"]
        form.description.data = good["description"]
        form.price.data = good["price"]

        return render_template("edit_item.html", form=form, item=good)


@item_bp.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    row = c.fetchone()

    try:
        good = {
            "id": row[0],
            "title": row[1],
        }
    except IndexError:
        good = {}

    if good:
        c.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        flash(f"Item {good['title']} has been successfully deleted.", "success")
    else:
        flash(f"This item does not exist", "danger")

    return redirect(url_for("main.home"))
