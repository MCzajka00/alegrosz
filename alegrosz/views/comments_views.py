from flask import Blueprint, url_for, redirect, request, render_template
from werkzeug.utils import escape

from alegrosz.dbs.dbs import get_db
from alegrosz.forms.comment_forms import NewCommentForm

comment_bp = Blueprint('comment', __name__, url_prefix='/comments')


@comment_bp.route("/", methods=["POST"])
def new_comment():
    conn = get_db()
    c = conn.cursor()

    form = NewCommentForm()
    # ajax - asynchronous js and xml
    try:
        is_ajax = int(request.form['ajax'])
    except Exception as e:
        is_ajax = 0

    if form.validate_on_submit():
        c.execute("""INSERT INTO comments (content, item_id)
        VALUES (?, ?)""", (
            escape(form.content.data),
            form.item_id.data
        ))

        conn.commit()

        if is_ajax:
            return render_template("_comment.html", content=form.content.data)
    if is_ajax:
        return "Content is required.", 400
    return redirect(url_for('item.item', item_id=form.item_id.data))
