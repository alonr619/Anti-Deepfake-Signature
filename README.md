# Flask Sign Service

A Flask application that provides a web interface for uploading images and text files, then makes a POST request to a `/sign` endpoint with the uploaded files as parameters.

## Features

- Modern, responsive web interface
- File upload for images (PNG, JPG, JPEG, GIF, BMP, TIFF)
- File upload for text files (TXT, MD, DOC, DOCX)
- Client-side validation
- Loading states and error handling
- Automatic POST request to `/sign` endpoint

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Select an image file using the first file input
2. Select a text file using the second file input
3. Click "Upload & Process" to submit the files
4. The application will:
   - Validate the file types
   - Read the text file content
   - Make a POST request to `http://localhost:5000/sign` with:
     - The image file in the `files` parameter
     - The text content in the `data` parameter as `text_content`

## API Endpoints

- `GET /` - Main upload page
- `GET /sign` - Upload page (same as root)
- `POST /sign` - Process uploaded files and make POST request to `/sign`

## File Structure

```
antideepfake/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── upload.html    # HTML template for the upload form
└── uploads/           # Directory for uploaded files (created automatically)
```

## Configuration

The application can be configured by modifying the following variables in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `ALLOWED_EXTENSIONS`: Allowed image file extensions
- `ALLOWED_TEXT_EXTENSIONS`: Allowed text file extensions
- Target URL for the POST request (currently set to `http://localhost:5000/sign`)

## Error Handling

The application includes comprehensive error handling for:
- Missing files
- Invalid file types
- File reading errors
- Network errors during POST requests
- General exceptions

All errors are returned as JSON responses with appropriate HTTP status codes. 