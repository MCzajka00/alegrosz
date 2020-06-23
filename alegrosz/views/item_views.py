from flask import Blueprint, request, redirect, render_template, flash, url_for

from alegrosz.dbs.dbs import get_db
from alegrosz.forms.item_form import NewItemForm

item_bp = Blueprint("item", __name__, url_prefix="/items")


@item_bp.route("/add", methods=['GET', 'POST'])
def add_item():
    conn = get_db()
    c = conn.cursor()

    form = NewItemForm()

    if request.method == 'POST':
        c.execute("""INSERT INTO items
            (title, description, price, image, category_id, subcategory_id)
            VALUES (?, ?, ?, ?, ?, ?)""",
                  (
                      form.title.data,
                      form.description.data,
                      float(form.price.data),
                      "",
                      1,
                      1
                  )
            )
        conn.commit()
        flash(f"Item { form.title.data } has been successfully submitted.", "success")
        return redirect(url_for("main.home"))
    return render_template("new_item.html", form=form)
