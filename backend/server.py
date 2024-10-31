# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import cv2
# import dlib
# import face_recognition
# import numpy as np

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Set the upload folder path
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Initialize dlib's face detector
# face_detector = dlib.get_frontal_face_detector()

# def enhance_image_visibility(image):
#     # Convert image to HSV to adjust saturation and brightness
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#     hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv_image)

#     # Increase brightness and saturation
#     v = cv2.add(v, 30)  # Increase brightness
#     s = cv2.add(s, 40)  # Increase saturation

#     # Merge and convert back to grayscale
#     enhanced_hsv_image = cv2.merge([h, s, v])
#     enhanced_bgr_image = cv2.cvtColor(enhanced_hsv_image, cv2.COLOR_HSV2BGR)
#     enhanced_gray_image = cv2.cvtColor(enhanced_bgr_image, cv2.COLOR_BGR2GRAY)

#     # Apply sharpening
#     kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
#     sharpened_image = cv2.filter2D(enhanced_gray_image, -1, kernel)

#     return sharpened_image

# def get_face_encoding(image_path):
#     # Load the image file and convert to RGB
#     image = cv2.imread(image_path)
#     enhanced_image = enhance_image_visibility(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
#     rgb_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2RGB)

#     # Detect and encode the face
#     encodings = face_recognition.face_encodings(rgb_image)
#     return encodings[0] if encodings else None

# def extract_frame_encodings(video_path, num_frames=10, interval=5):
#     """Extracts multiple frame encodings from the video at regular intervals."""
#     cap = cv2.VideoCapture(video_path)
#     frame_encodings = []
#     frame_count = 0

#     while len(frame_encodings) < num_frames:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
#         success, frame = cap.read()
#         if not success:
#             break
        
#         # Convert to RGB and find face encodings
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
        
#         if face_locations:
#             face_encoding = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations)[0]
#             frame_encodings.append(face_encoding)

#         frame_count += interval

#     cap.release()
#     return frame_encodings

# def match_faces(aadhar_encoding, video_encodings, tolerance=0.5):
#     """Compares Aadhaar face encoding with multiple video encodings for a similarity score."""
#     if not video_encodings:
#         return False

#     # Calculate the distance from the Aadhaar encoding to each frame encoding
#     distances = face_recognition.face_distance(video_encodings, aadhar_encoding)
#     match_score = np.mean(distances < tolerance)

#     # Define a match if over 60% of frames are within tolerance
#     return match_score >= 0.6

# @app.route('/api/upload', methods=['POST'])
# def upload_files():
#     if 'aadhar' not in request.files or 'pan' not in request.files or 'selfie' not in request.files or 'video' not in request.files:
#         return jsonify({"error": "All files are required: Aadhaar, PAN, selfie, and video."}), 400

#     aadhar = request.files['aadhar']
#     pan = request.files['pan']
#     selfie = request.files['selfie']
#     video = request.files['video']

#     # Save files
#     aadhar_path = os.path.join(app.config['UPLOAD_FOLDER'], 'aadhar.png')
#     aadhar.save(aadhar_path)

#     pan_path = os.path.join(app.config['UPLOAD_FOLDER'], 'pan.png')
#     pan.save(pan_path)

#     selfie_path = os.path.join(app.config['UPLOAD_FOLDER'], 'selfie.png')
#     selfie.save(selfie_path)

#     video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video.webm')
#     video.save(video_path)

#     return jsonify({"message": "Files uploaded successfully!"}), 200

# @app.route('/api/match', methods=['POST'])
# def face_match():
#     aadhar_path = os.path.join(app.config['UPLOAD_FOLDER'], 'aadhar.png')
#     video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video.webm')
    
#     # Check if files exist
#     if not os.path.exists(aadhar_path) or not os.path.exists(video_path):
#         return jsonify({"error": "Aadhaar or video file not found."}), 400

#     # Get Aadhaar face encoding
#     aadhar_encoding = get_face_encoding(aadhar_path)
#     if aadhar_encoding is None:
#         return jsonify({"error": "No face detected in Aadhaar image."}), 500

#     # Get video frame encodings
#     video_encodings = extract_frame_encodings(video_path, num_frames=10, interval=10)
#     if not video_encodings:
#         return jsonify({"error": "No face detected in video frames."}), 500

#     # Perform face matching
#     is_match = match_faces(aadhar_encoding, video_encodings)

#     if is_match:
#         return jsonify({"message": "Face match found!"}), 200
#     else:
#         return jsonify({"message": "Face does not match."}), 200

# @app.route('/test', methods=['GET'])
# def test_connection():
#     return jsonify({"message": "Connection successful!"})

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from services.ocr import extract_aadhaar_details
from services.twilio_otp import send_otp, verify_otp

app = Flask(__name__)
CORS(app)

aadhaar_to_mobile_map = {
    "680746720046": "+919569879937",
    "844233800631": "+917905206186"
}

# In-memory storage for testing purposes
temporary_store = {}

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'aadhar' not in request.files or 'pan' not in request.files:
        return jsonify({"error": "Both Aadhaar and PAN files are required."}), 400

    aadhar = request.files['aadhar']
    pan = request.files['pan']
    aadhar_path = os.path.join(app.config['UPLOAD_FOLDER'], 'aadhar.png')
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

@app.route('/api/verify_otp', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

