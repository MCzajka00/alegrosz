from flask import Flask


def create_app():
    alegrosz = Flask(__name__)
    alegrosz.config['SECRET_KEY'] = b'S\xdfCf\xee\xf0\x8d\xf2\xfb\xdaWA"6\xc4\x8f'


    from alegrosz.views.main_views import main_bp

    alegrosz.register_blueprint(main_bp)

    return alegrosz


app = create_app()
