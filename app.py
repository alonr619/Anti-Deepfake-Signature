from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from PIL import Image
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from helper import add_text_as_metadata, get_hash_from_image, verify_signature
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_TEXT_EXTENSIONS = {'txt'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/sign', methods=['GET'])
def sign_get():
    return render_template('sign.html')

@app.route('/verify', methods=['GET'])
def verify_get():
    return render_template('verify.html')

@app.route('/verify', methods=['POST'])
def verify_post():
    if 'image' not in request.files or 'public_key' not in request.files:
        return jsonify({'error': 'Both image and public key files are required'}), 400
    
    image_file = request.files['image']
    public_key_file = request.files['public_key']
    
    if image_file.filename == '' or public_key_file.filename == '':
        return jsonify({'error': 'Both files must be selected'}), 400
    
    if not allowed_file(image_file.filename, ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid image file type'}), 400
    
    if not allowed_file(public_key_file.filename, ALLOWED_TEXT_EXTENSIONS):
        return jsonify({'error': 'Invalid public key file type'}), 400
    
    try:
        img = Image.open(image_file)
        public_key = RSA.import_key(public_key_file.read().decode('utf-8'))
        verified = verify_signature(img, public_key)
        return jsonify({
            'status': 'verified' if verified else 'not_found',
            'message': 'Signature verified!' if verified else 'Signature verification failed'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

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
        hash = get_hash_from_image(img)
        signer = pkcs1_15.new(private_key)
        signature = signer.sign(hash)
        add_text_as_metadata(img, signature, str(image_file.filename))
        return send_file(f"uploads/signed_{image_file.filename}", as_attachment=True, download_name=f"signed_{image_file.filename}", mimetype=f'image/{img.format}', max_age=0)
        
    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 