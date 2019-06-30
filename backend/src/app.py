from flask import Flask
from flask import jsonify
from mongoengine import connect
import os
import logging.config
from logging_config import logging_config
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, headers="*")


from apiv1 import all_blueprints
for blueprint in all_blueprints:
    app.register_blueprint(blueprint)

print app.url_map


MONGO_HOSTNAME = os.environ.get('MONGO_HOST')
MONGO_PORT= int(os.environ.get('MONGO_PORT'))
MONGO_DB = os.environ.get('MONGO_DB')


connect(MONGO_DB, host=MONGO_HOSTNAME, port=MONGO_PORT)

if __name__ == "__main__":
    logging.config.dictConfig(logging_config)
    app.run(debug=True,  threaded=True)
