import flask

# import all endpoints here and register below
import pantry.v1.targets

def register_api(app, url_prefix):
    app.register_blueprint(targets.targets_blueprint, url_prefix=url_prefix)
