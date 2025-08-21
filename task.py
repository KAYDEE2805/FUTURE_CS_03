from flask import  Flask, send_from_directory, render_template, request
import os
from cypto_utils import generate_key, encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = 'statics/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('Flask_SECRET_KEY', 'a_default_secret_key')

ENCRYPTION_KEY = os.environ.get('FILE_ENCRYPTION_KEY', generate_key().decode())

@app.route('/', methods=["GET","POST"])
def index():
    return render_template("task.html")

@app.route('/upload',methods=["GET","POST"])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        encrypt_file(filepath, ENCRYPTION_KEY.encode())
        return 'file uploaded successfully!'
    
    @app.route('/download/<filename>', methods=["GET"])
    def download_file(filename):
        encrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.enc')
        if os.path.exists(encrypted_filepath):
            decrypted_filepath = decrypt_file(encrypted_filepath, ENCRYPTION_KEY.encode())
            return send_from_directory(os.path.dirname(decrypted_filepath), os.path.basename(decrypted_filepath), as_attachment=True)
        return 'File not found or not encrypted.'

    if __name__ == '__task__':
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        app.run(debug=True)
    