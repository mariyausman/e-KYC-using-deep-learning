from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import re
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load Haar Cascade
haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def extract_face_from_document(document_path):
    image = cv2.imread(document_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    return gray[y:y+h, x:x+w]

def decode_base64_image(data_url):
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def compare_faces(face1, face2):
    if face1 is None or face2 is None:
        return False
    face1 = cv2.resize(face1, (100, 100))
    face2 = cv2.resize(face2, (100, 100))
    diff = cv2.absdiff(face1, face2)
    score = np.sum(diff)
    threshold = 5000
    return score < threshold

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return jsonify({"error": "No file part"}), 400
    document = request.files['document']
    if document.filename == '':
        return jsonify({"error": "No selected file"}), 400
    document_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
    document.save(document_path)
    document_face = extract_face_from_document(document_path)
    if document_face is None:
        return jsonify({"error": "No face found in document"}), 400
    app.config['document_face'] = document_face  # Save for later comparison
    return jsonify({"result": "Document uploaded successfully"}), 200

@app.route('/compare_live_video', methods=['POST'])
def compare_live_video():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image data"}), 400
    
    frame = decode_base64_image(data['image'])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        return jsonify({"error": "No face found in video"}), 400

    x, y, w, h = faces[0]
    live_video_face = gray[y:y+h, x:x+w]
    
    # Compare the face from the live video with the document face
    document_face = app.config.get('document_face')
    if document_face is None:
        return jsonify({"error": "Document face not uploaded"}), 400

    if compare_faces(document_face, live_video_face):
        return jsonify({"result": "FACE MATCHED"}), 200
    else:
        return jsonify({"result": "FACE UNMATCHED"}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
