from google.cloud import storage
import requests
from PIL import Image, ImageFilter
from flask import jsonify
import tempfile
import io, os

# Initialize Google Cloud Storage Client
storage_client = storage.Client()
bucket_name = 'photocloud-img-process-bucket'
bucket = storage_client.bucket(bucket_name)

def process_image(request):
    request_json = request.get_json()

    if not request_json or 'image_url' not in request_json or 'filter_type' not in request_json:
        return jsonify({'error': 'Invalid request'}), 400

    image_url = request_json['image_url']
    filter_type = request_json['filter_type']

    try:
        # Download image from the provided URL
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))

        if filter_type == 'BLUR':
            image = image.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            image = image.filter(ImageFilter.CONTOUR)
        else:
            return jsonify({'error': 'Unsupported filter type'}), 400

        output_blob = bucket.blob(f"processed/{image_url.split('/')[-1]}")
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            image.save(temp_file, format='PNG')
            temp_file.close()

            output_blob.upload_from_filename(temp_file.name)
            output_blob.make_public()

            os.remove(temp_file.name)

        return jsonify({'processed_image_url': output_blob.public_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
