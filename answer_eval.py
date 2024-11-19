import pytesseract
from pdf2image import convert_from_path
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# OCR Configuration (Ensure Tesseract is installed on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    return pytesseract.image_to_string(image_path)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF."""
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def calculate_similarity(reference_answer, student_answer):
    """Use a transformer model (BERT) to calculate semantic similarity."""
    nlp = pipeline("feature-extraction", model="bert-base-uncased")
    ref_embedding = np.mean(nlp(reference_answer)[0], axis=0)
    student_embedding = np.mean(nlp(student_answer)[0], axis=0)

    # Compute cosine similarity
    similarity = cosine_similarity([ref_embedding], [student_embedding])[0][0]
    return similarity * 100  # Return as percentage

def evaluate_answer(reference_answer, student_answer, similarity_threshold=75):
    """Evaluate the student's answer."""
    similarity = calculate_similarity(reference_answer, student_answer)
    if similarity >= similarity_threshold:
        return True, similarity
    return False, similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """Extract text from an image."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

def evaluate_answer(correct_answer, student_answer):
    """Evaluate the answer using NLP and calculate similarity."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([correct_answer, student_answer])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    return similarity

def evaluate_answer(reference_answer, student_answer, threshold=75):
    """
    Evaluate the similarity between the reference answer and the student's answer.
    Returns whether the similarity exceeds the threshold and the similarity percentage.
    """
    # Compute similarity using TF-IDF and cosine similarity
    vectorizer = TfidfVectorizer().fit_transform([reference_answer, student_answer])
    similarity_matrix = cosine_similarity(vectorizer)
    similarity_percentage = similarity_matrix[0, 1] * 100  # Convert to percentage
    
    # Determine pass/fail based on the threshold
    is_pass = similarity_percentage >= threshold
    return is_pass, similarity_percentage

