import json

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

SECRET_PATH = "secret.json"

app = Flask(__name__)

secret = json.load(open(SECRET_PATH))

SWAGGER_URL = secret["swagger_url"]
SWAGGER_JSON = secret["swagger_json"]
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_JSON,
    config={
        'app_name': secret["app_name"]
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{}:{}@{}/{}".format(secret['user'], secret['password'], secret['host']
                                                                     , secret['DB'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

