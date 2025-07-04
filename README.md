# 🔐 Digital Signature Service

A Flask web application that provides digital signature capabilities for images using RSA cryptography. Users can generate RSA key pairs, sign images with private keys, and verify signatures with public keys.

## ✨ Features

- **🔑 RSA Key Generation** - Generate 2048-bit RSA private/public key pairs
- **✍️ Image Signing** - Sign images with private keys and embed signatures in metadata
- **🔍 Signature Verification** - Verify image authenticity using public keys
- **📱 Modern UI** - Responsive, beautiful web interface with loading states
- **🖼️ Multi-format Support** - PNG and JPEG image formats
- **🔒 Secure** - Uses industry-standard RSA cryptography
- **🧹 Auto-cleanup** - Automatically deletes temporary files after processing

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd antideepfake
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser:**
Navigate to `http://localhost:5000`

## 📖 Usage Guide

### 1. Generate RSA Keys
- Visit the home page
- Click "Generate Keys" to create a new RSA key pair
- Download both private and public keys as `.pem` files
- **Keep your private key secure!**

### 2. Sign an Image
- Navigate to "Sign Image" page
- Upload an image (PNG, JPG, JPEG)
- Upload your private key file (`.txt` or `.pem`)
- Click "Sign & Download"
- The signed image will be automatically downloaded

### 3. Verify a Signature
- Navigate to "Verify Signature" page
- Upload a signed image
- Upload the corresponding public key file (`.txt` or `.pem`)
- Click "Verify Signature"
- View the verification result

## 🏗️ Architecture

### File Structure
```
antideepfake/
├── app.py                    # Main Flask application
├── helper.py                 # Cryptographic and image processing functions
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .gitignore               # Git ignore rules
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css        # Consolidated styles
│   └── js/
│       ├── home.js          # Home page functionality
│       └── forms.js         # Form handling
├── templates/               # HTML templates
│   ├── index.html          # Home page
│   ├── sign.html           # Sign page
│   └── verify.html         # Verify page
└── uploads/                # Temporary file storage (auto-created)
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page with key generation |
| `POST` | `/generate-keys` | Generate RSA key pair |
| `GET` | `/sign` | Sign image page |
| `POST` | `/sign` | Sign image with private key |
| `GET` | `/verify` | Verify signature page |
| `POST` | `/verify` | Verify image signature |

## 🔧 Technical Details

### Cryptography
- **Algorithm**: RSA-2048 with PKCS#1 v1.5 padding
- **Hash Function**: SHA-256
- **Key Format**: PEM (Privacy Enhanced Mail)

### Image Processing
- **Supported Formats**: PNG, JPEG
- **Metadata Storage**:
  - **PNG**: Text chunks in PNG metadata
  - **JPEG**: EXIF data in ImageDescription field
- **Signature Encoding**: Base64

### Security Features
- File type validation
- Maximum file size limits (16MB)
- Automatic cleanup of temporary files
- Secure key handling

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| Pillow | 10.1.0 | Image processing |
| pycryptodome | 3.19.0 | RSA cryptography |
| piexif | 1.1.3 | JPEG EXIF metadata |

## ⚙️ Configuration

### File Size Limits
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Supported File Types
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}           # Images
ALLOWED_TEXT_EXTENSIONS = {'txt', 'pem', 'key'}       # Keys
```

## 🛠️ Development

### Running in Development Mode
```bash
python app.py
```
- Debug mode enabled
- Host: 0.0.0.0
- Port: 5000

### Code Organization
- **Frontend**: HTML templates with external CSS/JS
- **Backend**: Flask routes with helper functions
- **Cryptography**: Centralized in `helper.py`
- **Static Assets**: Organized in `static/` directory

## 🔍 Error Handling

The application includes comprehensive error handling for:
- Missing or invalid files
- Unsupported file formats
- Cryptographic errors
- Network issues
- File system errors

All errors return appropriate HTTP status codes and user-friendly messages.

## ⚠️ Security Notes

- **Private keys should never be shared**
- **Keep your private keys secure and backed up**
- **This is a demonstration application - use production-grade security for real deployments**
- **Consider using hardware security modules (HSMs) for production use**