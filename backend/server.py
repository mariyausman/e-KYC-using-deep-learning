# server.py
from flask import Flask
from flask_cors import CORS
import os
from services.upload import otp_bp  # Import OTP Blueprint
from services.liveness import liveness_bp  # Import Liveness Blueprint

app = Flask(__name__)
CORS(app)

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(otp_bp, url_prefix='/api')
app.register_blueprint(liveness_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
