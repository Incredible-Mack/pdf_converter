import os
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from pdf2docx import Converter

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

# Read environment variables
API_KEY = os.environ.get('API_KEY')  # Replace with your actual key names

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'Welcome to the PDF to DOCX API!'

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    # Check for the API key
    if API_KEY is None:
        return jsonify({'error': 'API Key not found'}), 500

    # Get the file from the request
    file = request.files.get('pdf_file')

    # Validate the uploaded file
    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)
        
        # Create the DOCX file path
        docx_path = pdf_path.replace('.pdf', '.docx')
        
        # Initialize the Converter and convert the file
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)  # Convert all pages
        cv.close()
        
        # Construct the download link (assuming your API is hosted at this URL)
        download_link = f"{request.host_url}download/{file.filename.replace('.pdf', '.docx')}"
        
        # Return the success message with the download link
        return jsonify({
            'message': 'Conversion successful',
            'download_link': download_link
        }), 200
    
    return jsonify({'error': 'Invalid file format. Please upload a PDF.'}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Endpoint to download the converted DOCX file."""
    docx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(docx_path):
        return send_file(docx_path, as_attachment=True)
    
    return jsonify({'error': 'File not found.'}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT env var or default to 5000
    app.run(host='0.0.0.0', port=port)
