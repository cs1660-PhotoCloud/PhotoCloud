from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
from google.cloud import storage
from PIL import Image, ImageFilter
import os
import io

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure Google Cloud Storage
BUCKET_NAME = "photocloud-img-process-bucket"  # Replace with your GCP bucket name
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

UPLOAD_IMAGE_URL = "https://upload-image-offkfeiooa-uc.a.run.app/"
PROCESS_IMAGE_URL = "https://process-image-offkfeiooa-uc.a.run.app/"

@app.route('/')
def index():
    """Render the main page."""
    return render_template("index.html")  # Assumes an index.html file in the templates folder


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload by calling the Cloud Function."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Send the file to the Cloud Function
        files = {'file': (file.filename, file.stream, file.mimetype)}
        response = requests.post(UPLOAD_IMAGE_URL, files=files)

        # Return the response from the Cloud Function
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process', methods=['POST'])
def process_image():
    """Handle image processing by calling the Cloud Function."""
    data = request.get_json()
    if not data or 'filename' not in data or 'filter' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    try:
        # Send the request to the Cloud Function
        response = requests.post(PROCESS_IMAGE_URL, json=data)

        # Return the response from the Cloud Function
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/processed-images', methods=['GET'])
def list_processed_images():
    """List all processed images and render them in the frontend."""
    try:
        blobs = bucket.list_blobs(prefix="processed/")  # List blobs with 'processed/' prefix
        processed_images = [blob.public_url for blob in blobs if blob.name.endswith(('jpg', 'jpeg', 'png'))]

        # Render the list in an HTML page
        return render_template("processed_images.html", images=processed_images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    # Make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
    app.run(host='0.0.0.0', port=8080, debug=True) 