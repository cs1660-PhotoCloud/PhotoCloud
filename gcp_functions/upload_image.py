import os
from google.cloud import storage
from flask import jsonify
import tempfile

# Initialize Google Cloud Storage Client
storage_client = storage.Client()
bucket_name = 'photocloud-img-process-bucket'  # Your GCP bucket name
bucket = storage_client.bucket(bucket_name)

def upload_image(request):
    """Upload image to Google Cloud Storage."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Generate a temporary file and store it in Cloud Storage
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file)
        
        # Define the destination path in your GCP bucket
        blob = bucket.blob(f"uploads/{file.filename}")
        blob.upload_from_filename(temp_file.name)
        
        # Make the file publicly accessible
        blob.make_public()

        # Cleanup temporary file
        os.remove(temp_file.name)

        # Return the public URL of the uploaded file
        return jsonify({'image_url': blob.public_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
