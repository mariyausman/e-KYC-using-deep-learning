from flask import Blueprint, request, jsonify, current_app
import os
from .ocr import extract_aadhaar_details
from .twilio_otp import send_otp, verify_otp

otp_bp = Blueprint('otp', __name__)

# Mock map for Aadhaar to mobile number
aadhaar_to_mobile_map = {
    "680746720046": "+919569879937",
    "844233800631": "+917905206186"
}

# Temporary in-memory storage for testing purposes
temporary_store = {}

@otp_bp.route('/upload', methods=['POST'])
def upload_files():
    if 'aadhar' not in request.files or 'pan' not in request.files:
        return jsonify({"error": "Both Aadhaar and PAN files are required."}), 400

    aadhar = request.files['aadhar']
    pan = request.files['pan']
    aadhar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'aadhar.png')
    aadhar.save(aadhar_path)
    
    extracted_details = extract_aadhaar_details(aadhar_path)
    
    # Get the Aadhaar number from extracted details
    aadhaar_number = extracted_details.get("Aadhaar Number")
    
    # Look up the mobile number using the Aadhaar number
    mobile_number = aadhaar_to_mobile_map.get(aadhaar_number)
    if not mobile_number:
        return jsonify({"error": "Mobile number not found for this Aadhaar number."}), 404

    # Store mobile number in the temporary store
    temporary_store['mobile_number'] = mobile_number

    if send_otp(mobile_number):
        return jsonify({"message": "OTP sent successfully.", "details": extracted_details}), 200
    else:
        return jsonify({"error": "Failed to send OTP."}), 500

@otp_bp.route('/verify_otp', methods=['POST'])
def verify_user_otp():
    data = request.get_json()
    otp_code = data.get('otp_code')
    
    # Retrieve mobile number from the temporary store
    mobile_number = temporary_store.get('mobile_number')

    if not otp_code or not mobile_number:
        return jsonify({"error": "OTP code and mobile number are required."}), 400

    if verify_otp(mobile_number, otp_code):
        return jsonify({"message": "OTP verified successfully."}), 200
    else:
        return jsonify({"message": "Invalid OTP."}), 400
