from flask import Flask, request, jsonify
import pdfplumber
from docx import Document

app = Flask(__name__)

# 🔑 Your API Key (you can set any value)
API_KEY = "12345"

@app.route('/analyze-document', methods=['POST'])
def analyze_document():

    # ✅ Check API Key from headers
    client_key = request.headers.get('x-api-key')

    if client_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename.lower()

    try:
        if filename.endswith('.pdf'):
            text = extract_pdf(file)

        elif filename.endswith('.docx'):
            text = extract_docx(file)

        else:
            return jsonify({"error": "Only PDF and DOCX supported"}), 400

        return jsonify({
            "filename": filename,
            "extracted_text": text[:500]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def extract_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


def extract_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)