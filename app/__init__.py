# coding=utf-8
import flask_httpauth
import pymongo
import flask
import config
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


db = pymongo.MongoClient().Outsource_1
auth = flask_httpauth.HTTPBasicAuth()
photos = UploadSet('photos', IMAGES)



def create_app(config_name):
    app = flask.Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)

    from .main import main as main_blueprint
    from .authen import authen as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    configure_uploads(app, photos)
    patch_request_class(app)  # 文件大小限制，默认为16MB

    return app
