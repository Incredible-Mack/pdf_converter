from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    converted_docx_path = ""
    if request.method == 'POST':
        file = request.files.get('pdf_file')
        if file and file.filename.endswith('.pdf'):
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)
            converted_docx_path = convert_pdf_to_docx(pdf_path)
    return render_template('index.html', converted_docx_path=converted_docx_path)

def convert_pdf_to_docx(pdf_path):
    docx_path = pdf_path.replace('.pdf', '.docx')
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)  # Convert all pages
    cv.close()
    return os.path.basename(docx_path)  # Return just the filename

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(full_path, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
