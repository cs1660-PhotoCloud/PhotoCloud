from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
from google.cloud import storage
from PIL import Image, ImageFilter
import os
import io

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure Google Cloud Storage
BUCKET_NAME = "your-bucket-name"  # Replace with your GCP bucket name
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


@app.route('/')
def index():
    """Render the main page."""
    return render_template("index.html")  # Assumes an index.html file in the templates folder


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and save to Cloud Storage."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        blob = bucket.blob(f"uploads/{file.filename}")
        blob.upload_from_file(file)
        blob.make_public()
        return jsonify({'message': 'File uploaded successfully', 'url': blob.public_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process', methods=['POST'])
def process_image():
    """Handle image processing requests."""
    data = request.get_json()
    if not data or 'filename' not in data or 'filter' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    filename = data['filename']
    filter_name = data['filter']

    try:
        # Download the image from Cloud Storage
        blob = bucket.blob(f"uploads/{filename}")
        image_bytes = blob.download_as_bytes()

        # Open the image using Pillow
        image = Image.open(io.BytesIO(image_bytes))

        # Apply the selected filter
        if filter_name == 'grayscale':
            image = image.convert('L')  # Convert to grayscale
        elif filter_name == 'blur':
            image = image.filter(ImageFilter.BLUR)  # Apply blur filter
        else:
            return jsonify({'error': 'Unsupported filter'}), 400

        # Save processed image to Cloud Storage
        processed_blob = bucket.blob(f"processed/{filename}")
        output_buffer = io.BytesIO()
        image.save(output_buffer, format=image.format)
        output_buffer.seek(0)
        processed_blob.upload_from_file(output_buffer, content_type="image/jpeg")
        processed_blob.make_public()

        return jsonify({'message': 'Image processed successfully', 'url': processed_blob.public_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/processed-images', methods=['GET'])
def list_processed_images():
    """List all processed images and render them in the frontend."""
    try:
        blobs = bucket.list_blobs(prefix="processed/")
        processed_images = [blob.public_url for blob in blobs if blob.name.endswith(('jpg', 'jpeg', 'png'))]

        # Render the list in an HTML page
        return render_template("processed_images.html", images=processed_images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
    app.run(host='0.0.0.0', port=8080, debug=True)