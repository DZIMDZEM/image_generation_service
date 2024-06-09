import os

from src.api.app import create_app
from src.api.logger import get_logger

app = create_app()

logger = get_logger(__name__, log_filename="api-server.log", rotating_file_handler=True)

logger.info("Application has fully started. Current env %s", os.environ)

logger.info("Starting application")
app.debug = True
app.run(host="0.0.0.0", port="8080")
