import json

from flask import Flask
from flask_mysqldb import MySQL
from flask_swagger_ui import get_swaggerui_blueprint

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
app.config['MYSQL_HOST'] = secret['host']
app.config['MYSQL_USER'] = secret['user']
app.config['MYSQL_PASSWORD'] = secret['password']
app.config['MYSQL_DB'] = secret['DB']

mysql = MySQL(app)
