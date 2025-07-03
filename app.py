from flask import Flask, render_template, request, jsonify
import requests
import os
from PIL import Image
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
ALLOWED_TEXT_EXTENSIONS = {'txt', 'md', 'doc', 'docx'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/sign', methods=['GET'])
def sign_get():
    return render_template('sign.html')

@app.route('/sign', methods=['POST'])
def sign_post():
    if 'image' not in request.files or 'text_file' not in request.files:
        return jsonify({'error': 'Both image and text file are required'}), 400
    
    image_file = request.files['image']
    text_file = request.files['text_file']
    
    if image_file.filename == '' or text_file.filename == '':
        return jsonify({'error': 'Both files must be selected'}), 400
    
    if not allowed_file(image_file.filename, ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid image file type'}), 400
    
    if not allowed_file(text_file.filename, ALLOWED_TEXT_EXTENSIONS):
        return jsonify({'error': 'Invalid text file type'}), 400
    
    try:
        private_key = RSA.import_key(text_file.read().decode('utf-8'))
        img = Image.open(image_file)
        img_data = img.convert('RGB').tobytes()
        hash = SHA256.new(img_data)
        signer = pkcs1_15.new(private_key)
        signature = signer.sign(hash)
        print(str(signature))
        return jsonify({
            'status': 'success',
            'response_status': 200,
            'response_data': str(signature)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 