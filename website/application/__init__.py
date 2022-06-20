from flask import Flask

def create_app():
    """ create flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Imports
        from .views import view
        from .filters import _slice
        from .database import DataBase

        # register routes for views
        app.register_blueprint(view, url_prefix="/")

        # register context processor
        @app.context_processor
        def slice():
            return dict(slice=_slice)

        return app