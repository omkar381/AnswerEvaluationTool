import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    try:
        # Configure Tesseract OCR path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Error: {e}"
