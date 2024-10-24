import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from a .env file (for local development)
load_dotenv()

# Read environment variables
API_KEY = os.environ.get('API_KEY')  # Replace with your actual key names

@app.route('/')
def index():
    return 'Welcome to the PDF to DOCX API!'

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if API_KEY is None:
        return jsonify({'error': 'API Key not found'}), 500

    # Your PDF to DOCX conversion logic goes here
    # Use API_KEY as needed

    return jsonify({'message': 'Conversion successful'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT env var or default to 5000
    app.run(host='0.0.0.0', port=port)
