from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)

    @app.route('/upload', methods=['GET'])
    def upload_file():
        if request.is_json:
            data = request.get_json()
            return jsonify({"message": "JSON received"}), 200
        else:
            return jsonify({"message": "Request is not JSON"}), 400
    

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200
    

    return app