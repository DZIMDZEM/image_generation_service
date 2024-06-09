from flask_restful import Resource

from src.api.logger import get_logger

logger = get_logger(__name__)


class HealthResource(Resource):
    def get(self):
        return {"status": "OK"}
