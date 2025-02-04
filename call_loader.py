from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)

    @app.route('/upload', methods=['GET'])
    def upload_file():
        if request.is_json:
            data = request.get_json()
            return jsonify({"message": "JSON received", "data": data}), 200
        else:
            return jsonify({"message": "Request is not JSON"}), 400
    
    return app