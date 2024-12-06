from google.cloud import storage
import requests
from flask import jsonify
import os

# Configure Google Cloud Storage
BUCKET_NAME = "photocloud-img-process-bucket"  # Replace with your GCP bucket name
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

UPLOAD_IMAGE_URL = "https://upload-image-offkfeiooa-uc.a.run.app/"
PROCESS_IMAGE_URL = "https://process-image-offkfeiooa-uc.a.run.app/"

def upload_image(request):
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
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def process_image(request):
    """Handle image processing by calling the Cloud Function."""
    data = request.get_json()
    if not data or 'image_url' not in data or 'filter_type' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    image_url = data['image_url']
    filter_type = data['filter_type']

    try:
        # Send the request to the Cloud Function
        response = requests.post(PROCESS_IMAGE_URL, json={
            "image_url": image_url,
            "filter_type": filter_type
        })

        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def list_processed_images(request):
    """List all processed images and return their URLs."""
    try:
        blobs = bucket.list_blobs(prefix="processed/")  # List blobs with 'processed/' prefix
        processed_images = [blob.public_url for blob in blobs if blob.name.endswith(('jpg', 'jpeg', 'png'))]
        return jsonify({'images': processed_images}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def main(request):
    """Google Cloud Function entry point to handle different routes."""
    if request.path == '/upload' and request.method == 'POST':
        return upload_image(request)
    elif request.path == '/process' and request.method == 'POST':
        return process_image(request)
    elif request.path == '/processed-images' and request.method == 'GET':
        return list_processed_images(request)
    else:
        return jsonify({'error': 'Not Found'}), 404
