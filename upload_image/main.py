import os
from google.cloud import storage
from flask import jsonify
import tempfile
from PIL import Image, ImageFilter

# Initialize Google Cloud Storage Client
storage_client = storage.Client()
bucket_name = 'photocloud-img-process-bucket'  # Your GCP bucket name
bucket = storage_client.bucket(bucket_name)

def upload_image(request):
    """Upload image to Google Cloud Storage."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filter_type = request.form.get('filter', 'NONE')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)

        # Open the image using Pillow
        with Image.open(temp_file.name) as image:
            # Apply the requested filter
            if filter_type == 'grayscale(100%)':
                image = image.filter(ImageFilter.BLUR)
            elif filter_type == 'CONTOUR':
                image = image.filter(ImageFilter.CONTOUR)
            # Add more filters as needed
            print("1")
            # Save the modified image to a new temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as filtered_temp_file:
                image.save(filtered_temp_file.name)
                filtered_temp_filename = filtered_temp_file.name
        print("2")
        # Upload the filtered image to Cloud Storage
        blob = bucket.blob(f"uploads/{file.filename}")
        blob.upload_from_filename(filtered_temp_filename)
        print("3")
        # Make the file publicly accessible
        blob.make_public()
        print("4")
        # Clean up temporary files
        os.remove(temp_file.name)
        os.remove(filtered_temp_filename)
        print("5")
        # Return the public URL of the uploaded file
        return jsonify({'image_url': blob.public_url}), 200

    except Exception as e:
        # Log error to Cloud Logging (optional) before returning a generic error message
        return jsonify({'error': 'An error occurred while uploading the image'}), 500
