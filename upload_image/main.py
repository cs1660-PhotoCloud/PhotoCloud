import os
from google.cloud import storage
from flask import jsonify, request
import tempfile
from PIL import Image, ImageFilter

# Initialize Google Cloud Storage Client
storage_client = storage.Client()
bucket_name = 'photocloud-img-process-bucket'  # Your GCP bucket name
bucket = storage_client.bucket(bucket_name)

def upload_image(request):
    """Upload image to Google Cloud Storage after applying a filter."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filter_type = request.form.get('filter', 'none')  # Get filter type from form data (default is 'none')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Create a temporary file with explicit cleanup (delete=False)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file)
            temp_file_path = temp_file.name  # Get the path of the temporary file

            # Log the temporary file path for debugging
            print(f"Temporary file created at: {temp_file_path}")

            # Open the image and apply the filter
            image = Image.open(temp_file_path)

            if filter_type == 'BLUR':
                image = image.filter(ImageFilter.BLUR)
            elif filter_type == 'CONTOUR':
                image = image.filter(ImageFilter.CONTOUR)
            else:
                return jsonify({'error': 'Invalid filter type'}), 400

            # Save the filtered image to the temporary file path
            image.save(temp_file_path)

            # Define the destination path in your GCP bucket
            blob = bucket.blob(f"uploads/{file.filename}")
            print(f"Uploading file to: {blob.name}")
            blob.upload_from_filename(temp_file_path)

            # The file is now uploaded and publicly accessible if permissions are set
            print(f"File uploaded successfully. Public URL: {blob.public_url}")

            # Clean up the temporary file manually
            os.remove(temp_file_path)
            print(f"Temporary file removed: {temp_file_path}")

        # Return the public URL of the uploaded file
        return jsonify({'image_url': blob.public_url}), 200

    except Exception as e:
        # Log the detailed error for debugging
        print(f"Error while uploading: {str(e)}")  # For local testing, logs will be printed
        return jsonify({'error': f'An error occurred while uploading the image: {str(e)}'}), 500

