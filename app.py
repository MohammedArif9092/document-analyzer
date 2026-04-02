from flask import Flask, request, jsonify
import pdfplumber
from docx import Document
import base64
from io import BytesIO

app = Flask(__name__)

API_KEY = "12345"

@app.route('/analyze-document', methods=['POST'])
def analyze_document():

    # 🔐 API Key check
    client_key = request.headers.get('x-api-key')
    if client_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    # ✅ Required fields
    file_name = data.get("fileName")
    file_type = data.get("fileType")
    file_base64 = data.get("fileBase64")

    if not file_name or not file_type or not file_base64:
        return jsonify({"error": "Missing input fields"}), 400

    try:
        # 🔹 Decode Base64
        file_bytes = base64.b64decode(file_base64)
        file = BytesIO(file_bytes)

        # 🔹 Extract text
        if file_type == "pdf":
            text = extract_pdf(file)
        elif file_type == "docx":
            text = extract_docx(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if not text:
            text = ""

        # 🔹 Dummy summary (required field)
        summary = text[:150]

        # 🔹 Dummy entities (required structure)
        entities = {
            "names": [],
            "dates": [],
            "organizations": [],
            "amounts": []
        }

        # 🔹 Dummy sentiment
        sentiment = "Neutral"

        return jsonify({
            "status": "success",
            "fileName": file_name,
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)