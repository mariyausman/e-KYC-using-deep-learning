import pytesseract
from PIL import Image
import re
import cv2
import numpy as np

def preprocess_image(image_path):
    """Preprocess the image for basic grayscale and binarization, optimized for Tesseract OCR."""
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((pil_image.width * 2, pil_image.height * 2), Image.Resampling.LANCZOS)
    gray_image = pil_image.convert("L")
    image = np.array(gray_image)
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    preprocessed_image_path = "uploads/preprocessed_image.jpg"
    cv2.imwrite(preprocessed_image_path, binary_image)
    return preprocessed_image_path

def correct_date_format(date_text):
    digits_only = re.sub(r"[^\d]", "", date_text)
    if len(digits_only) == 8:
        date_text = f"{digits_only[:2]}/{digits_only[2:4]}/{digits_only[4:]}"
    else:
        return digits_only
    match = re.match(r"(\d{2})/(\d{2})/(\d{4})", date_text)
    return date_text if match else "Invalid date format"

def extract_aadhaar_details(image_path):
    preprocessed_image_path = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image_path, lang='eng+hin', timeout=4)
    print(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    name = "Not found"
    dob = "Not found"
    address = "Not found"
    
    for i, line in enumerate(lines):
        dob_match = re.search(r"(?:DOB|OOB|जन्म तिथि|Year of Birth)[:\s]*([\d/]+)", line, re.IGNORECASE)
        if dob_match:
            dob = correct_date_format(dob_match.group(1))
            if i > 0:
                name = lines[i - 1].strip()
            break

    gender_pattern = re.search(r"(FEMALE|MALE|महिला|पुरुष)", text, re.IGNORECASE)
    aadhaar_number_pattern = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
    
    gender = gender_pattern.group(1).strip() if gender_pattern else "Not found"
    gender = "Female" if gender in ["महिला", "Female"] else "Male" if gender in ["पुरुष", "Male"] else gender
    aadhaar_number = aadhaar_number_pattern.group(0).replace(" ", "") if aadhaar_number_pattern else "Not found"

    # Extract Address: Find the line containing "Address" and capture the following 3 lines as address
    address_index = next((i for i, line in enumerate(lines) if re.search(r"Address[:\s]*", line, re.IGNORECASE)), None)
    if address_index is not None:
        address_lines = lines[address_index + 1: address_index + 4]  # Get 3 lines below "Address"
        address = " ".join(address_lines).strip() if address_lines else "Not found"

    extracted_details = {
        "Name": name,
        "DOB": dob,
        "Gender": gender,
        "Aadhaar Number": aadhaar_number,
        "Address": address
    }
    
    print(extracted_details)
    return extracted_details
