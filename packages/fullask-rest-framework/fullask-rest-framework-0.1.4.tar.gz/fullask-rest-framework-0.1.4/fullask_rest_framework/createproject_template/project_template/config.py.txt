# config.py from fullask-rest-framework.

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

API_TITLE = ""
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.2"

SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "db.sqlite"))
