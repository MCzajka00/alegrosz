from flask import Flask, g


def create_app():
    alegrosz = Flask(__name__)
    alegrosz.config['SECRET_KEY'] = b'S\xdfCf\xee\xf0\x8d\xf2\xfb\xdaWA"6\xc4\x8f'

    from alegrosz.views import main_bp
    from alegrosz.views import item_bp
    from alegrosz.views import comment_bp
    from alegrosz.views import category_bp

    alegrosz.register_blueprint(main_bp)
    alegrosz.register_blueprint(item_bp)
    alegrosz.register_blueprint(comment_bp)
    alegrosz.register_blueprint(category_bp)

    return alegrosz


app = create_app()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
