from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from src.api.core_features.auth.core import USER_DATABASE

user_authentication = HTTPBasicAuth()


@user_authentication.verify_password
def verify_password(username, password):
    if username in USER_DATABASE and check_password_hash(USER_DATABASE.get(username).password_hash, password):
        return True
    return False
