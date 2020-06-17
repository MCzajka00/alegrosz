from flask import Flask


def create_app():
    alegrosz = Flask(__name__)

    from alegrosz.views.main_views import main_bp

    alegrosz.register_blueprint(main_bp)

    return alegrosz


app = create_app()
