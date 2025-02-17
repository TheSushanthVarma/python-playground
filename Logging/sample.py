# simple flask server
from flask import Flask, request, jsonify
from json_logging import logger
from advanced_logger import logger
from pre import logger


app = Flask(__name__)


@app.route("/")
def index():
    logger.info("Request received")
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)

