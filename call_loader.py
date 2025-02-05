from flask import Flask, request, jsonify
from call_parser import parse_calls
import json
import logging

def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    @app.route('/upload', methods=['GET'])
    def upload_file():
        print("WASSAP")
        if request.is_json:
            data = request.get_json()
            app.logger.info("HELLO WORLD!")
            # Assuming the JSON is a dictionary with one key, whose value is a list of objets
            key = next(iter(data))
            value_list = data[key]
            #app.logger.info(value_list)
            parse_calls(value_list, app.logger)
            return jsonify({"message": "JSON received"}), 200
        else:
            return jsonify({"message": "Request is not JSON"}), 400
    

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200
    

    return app
