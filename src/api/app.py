import logging
import logging.config
import sys
from os import environ

import flask_restful
from flask import Flask, jsonify
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_restful import output_json
from werkzeug.exceptions import default_exceptions, HTTPException

from src.api.core_features.exception.request import ValidationError
from src.api.core_features.infrastructure.custom_json import output_vnd_json
from src.api.core_features.infrastructure.modules import create_modules
from src.api.domain_features.dcgan.dcgan_resource import GenerateImageResource
from src.api.domain_features.display_output.display_resource import DisplayImageResource

from src.api.logger import get_logger

from src.api.domain_features.health.health_resource import HealthResource


logger = get_logger(__name__)


def create_app(modules=None):
    logger.info("Creating application")

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    logger.info("Flask App ready")

    class Api(flask_restful.Api):
        def __init__(self, *args, **kwargs):
            super(Api, self).__init__(*args, **kwargs)
            self.representations = {
                "application/vnd.synth+json": output_vnd_json,
                "application/json": output_json,
            }

    api = Api(app, catch_all_404s=True)

    with app.app_context():
        app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        app.logger.setLevel(logging.DEBUG)

    def setup_json_error_handling(app):
        def make_json_error(ex):
            message = f"{str(ex.message)}" if hasattr(ex, "message") else f"{str(ex)}"
            app.logger.exception(ex)

            data = {
                "type": ex.__class__.__name__,
                "message": message
            }

            if isinstance(ex, HTTPException):
                data["code"] = ex.code
                response = jsonify(data)
                response.status_code = ex.code
            else:
                response = jsonify(data)
                response.status_code = 400 if isinstance(ex, ValidationError) else 500

            return response

        for code in default_exceptions.keys():
            app.register_error_handler(code, make_json_error)

        app.register_error_handler(Exception, make_json_error)

        return app

    app = setup_json_error_handling(app)

    api.add_resource(HealthResource, "/health", "/api/v1/health")
    api.add_resource(GenerateImageResource, "/generate", "/api/v1/generate")
    api.add_resource(DisplayImageResource, "/display", "/api/v1/display")

    logger.info("API Configured")

    if not modules:
        modules = create_modules()

    app.injector = FlaskInjector(app=app, modules=modules).injector

    cors = CORS(resources={r"/api/*": {"origins": "*"}})
    cors.init_app(app)

    logger.info("API has fully started!")
    logger.debug("Current env %s", environ)

    return app
