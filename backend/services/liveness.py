import cv2
import dlib
import numpy as np
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from scipy.spatial import distance as dist
import os
from services.face_match import face_matching  # Import the face_matching function

# Initialize Blueprint
liveness_bp = Blueprint('liveness', __name__)
CORS(liveness_bp)

# Constants for blink detection
EYE_AR_THRESHOLD = 0.3
EYE_AR_CONSEC_FRAMES = 3

# Initialize face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("services/shape_predictor_68_face_landmarks.dat")

# Function to calculate Eye Aspect Ratio (EAR)
def calculate_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

@liveness_bp.route('/process_liveness', methods=['POST'])
def process_liveness():
    video_file = request.files["video"]
    video_path = "uploads/temp_liveness_video.mp4"
    video_file.save(video_path)

    # Step 1: Blink Detection
    vs = cv2.VideoCapture(video_path)
    blink_detected = False
    COUNTER = 0

    while True:
        ret, frame = vs.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray)

        for face in faces:
            shape = shape_predictor(gray, face)
            left_eye = [(shape.part(i).x, shape.part(i).y) for i in range(36, 42)]
            right_eye = [(shape.part(i).x, shape.part(i).y) for i in range(42, 48)]

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            ear = (left_ear + right_ear) / 2.0

            if ear < EYE_AR_THRESHOLD:
                COUNTER += 1
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    blink_detected = True
                COUNTER = 0

        if blink_detected:
            break

    vs.release()

    # If no blink was detected, return an error message
    if not blink_detected:
        os.remove(video_path)
        return jsonify({"message": "No blink detected, please try again!"})

    # Step 2: Face Matching
    aadhaar_image_path = "uploads/aadhar.png"  # Adjust the path as needed
    face_match_result = face_matching(aadhaar_image_path, video_path)
    os.remove(video_path)

    # Return the face match result
    return jsonify(face_match_result)