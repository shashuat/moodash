from flask import Blueprint

errors = Blueprint('errors', __name__)

# custom error pages


@errors.app_errorhandler(404)
def error404(error):
    # second value is status code, default is 200
    return "<h1>Where you goin?</h1>", 404


@errors.app_errorhandler(403)
def error403(error):
    return "<h1>What you doin?</h1>", 403
