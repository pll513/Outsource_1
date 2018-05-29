from . import main
from flask import jsonify, url_for


@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({
        'code': 404
    })


@main.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'code': 500
    })

