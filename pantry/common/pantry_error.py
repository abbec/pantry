import flask

pantry_error = flask.Blueprint('muffin_error', __name__)


class PantryError(Exception):

    def __init__(self, message, payload=None, status_code=None):
        super().__init__(self)
        self.message = message
        self.payload = payload
        self.status_code = status_code or 400

    def to_dict(self):
        d = dict(self.payload or ())
        d['message'] = self.message
        return d


@pantry_error.app_errorhandler(PantryError)
def handle_pantry_error(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code

    return response


@pantry_error.app_errorhandler(404)
def handle_404(error):
    del error
    response = flask.jsonify(
        {"message": "the requested resource could not be found."})
    response.status_code = 404

    return response


# log all 500 errors
@pantry_error.app_errorhandler(500)
def handle_500(error):
    response = flask.jsonify({"message": "an internal server error occured."})
    response.status_code = 500

    flask.current_app.logger.exception(error)

    return response
