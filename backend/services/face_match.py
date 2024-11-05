import cv2
import face_recognition
import numpy as np
import os

# Function to enhance image visibility
def enhance_image_visibility(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    v = cv2.add(v, 30)
    s = cv2.add(s, 40)
    enhanced_hsv_image = cv2.merge([h, s, v])
    enhanced_bgr_image = cv2.cvtColor(enhanced_hsv_image, cv2.COLOR_HSV2BGR)
    enhanced_gray_image = cv2.cvtColor(enhanced_bgr_image, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(enhanced_gray_image, -1, kernel)

# Function to get face encoding from an image file
def get_face_encoding(image_path):
    image = cv2.imread(image_path)
    enhanced_image = enhance_image_visibility(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    rgb_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2RGB)
    encodings = face_recognition.face_encodings(rgb_image)
    return encodings[0] if encodings else None

# Function to extract frame encodings from a video
def extract_frame_encodings(video_path, num_frames=10, interval=5):
    cap = cv2.VideoCapture(video_path)
    frame_encodings = []
    frame_count = 0

    while len(frame_encodings) < num_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        success, frame = cap.read()
        if not success:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
        
        if face_locations:
            face_encoding = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations)[0]
            frame_encodings.append(face_encoding)

        frame_count += interval

    cap.release()
    return frame_encodings

# Function to match faces
def match_faces(aadhar_encoding, video_encodings, tolerance=0.5):
    if not video_encodings:
        return False
    distances = face_recognition.face_distance(video_encodings, aadhar_encoding)
    match_score = np.mean(distances < tolerance)
    return match_score >= 0.6

# Main function to perform face matching
def face_matching(aadhar_image_path, video_path):
    aadhar_encoding = get_face_encoding(aadhar_image_path)
    if aadhar_encoding is None:
        return {"message": "No face detected in Aadhaar image."}

    video_encodings = extract_frame_encodings(video_path, num_frames=10, interval=5)
    if not video_encodings:
        return {"message": "No face detected in video frames."}

    is_match = match_faces(aadhar_encoding, video_encodings)

    if is_match:
        return {"message": "Face match found!"}
    else:
        return {"message": "Face does not match Aadhaar."}