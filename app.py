from flask import Flask, render_template, request, jsonify, send_file
import os
from PIL import Image
from Crypto.PublicKey import RSA
from helper import save_image_with_metadata, get_hash_from_image, verify_image_signature, get_signature_from_hash, generate_rsa_key_pair

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_TEXT_EXTENSIONS = {'txt', 'pem', 'key'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-keys', methods=['POST'])
def generate_keys():
    try:
        private_key, public_key = generate_rsa_key_pair()
        return jsonify({
            'status': 'success',
            'private_key': private_key,
            'public_key': public_key
        })
    except Exception as e:
        return jsonify({'error': f'Error generating keys: {str(e)}'}), 500

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
        verified = verify_image_signature(img, public_key)
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
        print(hash)
        signature = get_signature_from_hash(hash, private_key)
        save_image_with_metadata(img, signature, str(image_file.filename))
        
        response = send_file(f"uploads/signed_{image_file.filename}", as_attachment=True, download_name=f"signed_{image_file.filename}", mimetype=f'image/{img.format}', max_age=0)
        
        try:
            os.remove(f"uploads/signed_{image_file.filename}")
        except OSError as e:
            print(f"Warning: Could not delete signed image: {e}")
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 