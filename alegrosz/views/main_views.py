from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, url_prefix="/")


@main_bp.route('/')
def home():
    return render_template('home.html')