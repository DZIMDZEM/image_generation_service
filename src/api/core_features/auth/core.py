import random
import string
from typing import Optional, List

import attr


def generate_random_key(length):
    return ''.join(random.choice(string.digits + string.ascii_letters) for x in range(length))


@attr.s
class SystemUser:
    user_id: str = attr.ib()
    principal_name: str = attr.ib()
    password_hash: Optional[str] = attr.ib(default=None)
    roles: Optional[List[str]] = attr.ib(default=attr.Factory(list))


USER_DATABASE = {user.user_id: user for user in [
    SystemUser(
        password_hash='pbkdf2:sha256:150000$oNYiMH30$dac3a68f05dc19774ec13287d455ba07af5b49b5060fe4e4c983e41d240cacd9',
        roles=['admin'],
        user_id='admin',
        principal_name='root@localhost',
    ),
    SystemUser(
        password_hash='pbkdf2:sha256:150000$oNYiMH30$dac3a68f05dc19774ec13287d455ba07af5b49b5060fe4e4c983e41d240cacd9',
        roles=['test_user'],
        user_id='test_user',
        principal_name='root@localhost',
    ),
]}
