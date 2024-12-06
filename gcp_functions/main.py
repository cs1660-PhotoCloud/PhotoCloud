import os
import json
from google.cloud import storage
from PIL import Image
import io
from flask import Request, jsonify

# Initialize GCP storage client
storage_client = storage.Client()
bucket = storage_client.bucket("YOUR_BUCKET_NAME")

def upload_image(request: Request):
    """Handle image upload and save it to GCP Cloud Storage."""
    try:
        # Check if the request contains the file
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded image to Google Cloud Storage
        blob = bucket.blob(f"uploads/{file.filename}")
        blob.upload_from_file(file)

        # Get public URL of the uploaded image
        blob.make_public()
        return jsonify({'message': 'Image uploaded successfully', 'url': blob.public_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_image(request: Request):
    """Process an image (e.g., apply color filter) and return the processed image."""
    try:
        data = request.get_json()
        image_url = data.get("image_url")
        filter_type = data.get("filter_type")

        if not image_url or not filter_type:
            return jsonify({'error': 'Missing parameters'}), 400

        # Download image from Cloud Storage
        blob = bucket.blob(image_url)
        image_data = blob.download_as_bytes()
        
        image = Image.open(io.BytesIO(image_data))
        
        # Apply a simple filter (e.g., grayscale)
        if filter_type == "grayscale":
            image = image.convert("L")
        # More filters can be added here

        # Save processed image back to Cloud Storage
        processed_blob = bucket.blob(f"processed/{blob.name}")
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)
            processed_blob.upload_from_file(output, content_type="image/png")
        
        # Make processed image public and return URL
        processed_blob.make_public()
        return jsonify({'message': 'Image processed successfully', 'url': processed_blob.public_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

