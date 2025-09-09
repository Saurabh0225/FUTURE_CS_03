# app.py (fixes included)

from flask import Flask, request, send_file, render_template, redirect, url_for, flash
from encryption import encrypt_file, decrypt_file, generate_key
from io import BytesIO
import os
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Generate key if it doesn't exist
if not os.path.exists('key.key'):
    generate_key()

# Home page
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename:
        data = file.read()
        encrypted_data = encrypt_file(data)

        # Use UUID to prevent filename collisions
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

        with open(filepath, 'wb') as f:
            f.write(encrypted_data)

        flash(f"File '{file.filename}' uploaded and encrypted successfully!")
    else:
        flash('No file selected!')
    return redirect(url_for('index'))

# Download route
@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        flash('File not found!')
        return redirect(url_for('index'))

    with open(filepath, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_file(encrypted_data)

    # Remove UUID prefix safely
    parts = filename.split("_", 1)
    original_filename = parts[1] if len(parts) > 1 else filename

    return send_file(
        BytesIO(decrypted_data),
        as_attachment=True,
        download_name=original_filename,
        mimetype='application/octet-stream'
    )

if __name__ == '__main__':
    # Allow access via both 127.0.0.1 and 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=True)
