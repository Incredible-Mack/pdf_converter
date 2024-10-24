from flask import Flask, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    file = request.files.get('pdf_file')
    
    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)
        
        # Create the DOCX file path
        docx_path = pdf_path.replace('.pdf', '.docx')
        
        # Initialize the Converter and convert the file
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)  # Convert all pages
        cv.close()
        
        # Return the DOCX file
        return send_file(docx_path, as_attachment=True)
    
    return {'error': 'Invalid file format. Please upload a PDF.'}, 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
