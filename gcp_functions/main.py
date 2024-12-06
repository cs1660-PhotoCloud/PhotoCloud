import os
from google.cloud import storage

BUCKET_NAME = os.environ['BUCKET_NAME']

def upload_image(request):
    request_json = request.get_json()
    if not request_json or 'image' not in request_json or 'filename' not in request_json:
        return 'Invalid request', 400
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)

    image_content = request_json['image']
    filename = request_json['filename']
    blob = bucket.blob(f"uploads/{filename}")

    blob.upload_from_string(image_content, content_type="image/jpeg")
    blob.make_public()

    return {"url": blob.public_url}, 200

def process_image(request):
    request_json = request.get_json()
    if not request_json or 'filename' not in request_json or 'filter' not in request_json:
        return 'Invalid request', 400
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)

    filename = request_json['filename']
    filter_type = request_json['filter']
    blob = bucket.blob(f"uploads/{filename}")

    image_content = blob.download_as_bytes()
    image = Image.open(io.BytesIO(image_content))

    # Apply filter
    if filter_type == "BLUR":
        image = image.filter(ImageFilter.BLUR)
    elif filter_type == "CONTOUR":
        image = image.filter(ImageFilter.CONTOUR)

    # Save processed image back to storage
    output = io.BytesIO()
    image.save(output, format="JPEG")
    output.seek(0)

    processed_blob = bucket.blob(f"processed/{filename}")
    processed_blob.upload_from_file(output, content_type="image/jpeg")
    processed_blob.make_public()

    return {"url": processed_blob.public_url}, 200
