# e-KYC Verification System

An advanced e-KYC (Electronic Know Your Customer) verification system that automates the identity verification process using deep learning for face recognition, liveness detection, and Optical Character Recognition (OCR) for extracting details from government-issued IDs like Aadhaar. This system eliminates the need for manual checks in most cases, reducing time and cost while ensuring secure and user-friendly KYC processes.

## Features

- **Face Recognition**: Matches a user's live video with their Aadhaar card photo for accurate identity verification.
- **Liveness Detection**: Ensures the user is physically present by detecting natural motions like blinking, preventing spoofing attacks.
- **OCR for ID Extraction**: Extracts text details (Name, DOB, Aadhaar number, Address) from the uploaded ID image using Tesseract OCR.
- **OTP Verification**: Adds a layer of authentication by sending an OTP to the user’s registered mobile number.
- **User-Friendly Interface**: Simple web interface for users to complete KYC verification remotely.

## Benefits

- **Automated ID Verification**: Reduces manual work and associated costs, with optional manual verification for rare cases.
- **Hardware-Free**: No need for specialized biometric tools, as it uses the webcam and mobile verification.
- **Scalable and Flexible**: Supports multiple languages, cloud deployment, and microservices architecture.
- **Adaptive Image Handling**: Automatically processes various resolutions and orientations for ID images.

## Technology Stack

- **Frontend**: React.js
- **Backend**: Python with Flask
- **Database**: MySQL or PostgreSQL
- **APIs**: Twilio for OTP verification, Tesseract OCR for text extraction, dlib and OpenCV for face detection and liveness check

## Project Structure

```plaintext
e-KYC Verification System/
├── backend/
│   ├── services/
│   │   ├── face_match.py              # Face recognition with Aadhaar photo
│   │   ├── liveness.py                # Liveness detection to prevent spoofing
│   │   ├── ocr.py                     # OCR extraction from ID images
│   │   ├── shape_predictor_68_face_landmarks.dat  # Facial landmarks for dlib
│   │   ├── dlib_face_recognition_resnet_model_v1.dat # Deep learning face model
│   │   ├── twilio_otp.py              # OTP verification using Twilio API
│   │   ├── upload.py                  # File upload handling
│   └── server.py                      # Main server file for routing
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json                   # Frontend dependencies
├── uploads/                           # Temporary storage for uploaded files
├── .env                               # Environment variables for sensitive data
└── README.md
