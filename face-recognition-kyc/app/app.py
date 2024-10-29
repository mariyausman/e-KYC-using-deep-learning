from flask import Flask, request, render_template, jsonify
import os
import cv2
import dlib
import fitz  # PyMuPDF for handling PDF
import pytesseract
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Dlib's face detector
detector = dlib.get_frontal_face_detector()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling file uploads
@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    aadhar_pdf = request.files['aadhar_pdf']

    # Save uploaded files
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], aadhar_pdf.filename)
    video.save(video_path)
    aadhar_pdf.save(pdf_path)

    # Extract face from Aadhaar PDF
    face_from_aadhar = extract_face_from_aadhar(pdf_path)

    # Extract face from video
    face_from_video = extract_face_from_video(video_path)

    # Compare faces
    if face_from_aadhar is not None and face_from_video is not None:
        match_result = compare_faces(face_from_aadhar, face_from_video)
        message = "Faces Matched" if match_result else "Faces Not Matched"
    else:
        message = "Unable to detect faces in either Aadhaar or video."

    return jsonify({'message': message})

def extract_face_from_aadhar(pdf_path):
    # Extract the first page of the PDF as an image
    pdf = fitz.open(pdf_path)
    page = pdf.load_page(0)
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # Extract the first detected face
    if len(faces) > 0:
        return img[faces[0].top():faces[0].bottom(), faces[0].left():faces[0].right()]
    return None

def extract_face_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if len(faces) > 0:
            return frame[faces[0].top():faces[0].bottom(), faces[0].left():faces[0].right()]
    return None

def compare_faces(face1, face2):
    # Resize both faces for comparison (Optional: You can use a pre-trained model like VGGFace)
    face1_resized = cv2.resize(face1, (150, 150))
    face2_resized = cv2.resize(face2, (150, 150))

    # Calculate the mean squared error between the two faces
    diff = cv2.absdiff(face1_resized, face2_resized)
    mse = np.mean(diff**2)

    # Threshold for matching faces
    return mse < 1000  # You can adjust this threshold

if __name__ == '__main__':
    app.run(debug=True, port=4555)
