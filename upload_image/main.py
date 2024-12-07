import os
from google.cloud import storage
from flask import jsonify, request
import tempfile
from PIL import Image, ImageFilter

# Initialize Google Cloud Storage Client
storage_client = storage.Client()
bucket_name = 'photocloud-img-process-bucket'
bucket = storage_client.bucket(bucket_name)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(request):
    """Upload image to Google Cloud Storage after applying a filter."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filter_type = request.form.get('filter', 'none') 

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'No selected file or invalid file type. Allowed file types are png, jpg, jpeg, gif.'}), 400

    try:
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            file.save(temp_file)
            temp_file_path = temp_file.name  # Get the path of the temporary file

            print(f"Temporary file created at: {temp_file_path}")

            image = Image.open(temp_file_path)

            if filter_type == 'none':
                pass  # No filter applied
            elif filter_type == 'grayscale':
                image = image.convert('L')  # Convert image to grayscale
            elif filter_type == 'sepia':
                # Apply sepia filter
                sepia_image = image.convert("RGB")
                width, height = sepia_image.size
                pixels = sepia_image.load()  # Create the pixel map

                for py in range(height):
                    for px in range(width):
                        r, g, b = sepia_image.getpixel((px, py))

                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                        tr = min(255, tr)
                        tg = min(255, tg)
                        tb = min(255, tb)

                        pixels[px, py] = (tr, tg, tb)

                image = sepia_image
            elif filter_type == 'blur':
                image = image.filter(ImageFilter.BLUR) 
            else:
                return jsonify({'error': 'Invalid filter type'}), 400

            image.save(temp_file_path)

            blob = bucket.blob(f"uploads/{file.filename}")
            print(f"Uploading file to: {blob.name}")
            blob.upload_from_filename(temp_file_path)

            print(f"File uploaded successfully. Public URL: {blob.public_url}")

            os.remove(temp_file_path)
            print(f"Temporary file removed: {temp_file_path}")

        # Return the public URL of the uploaded file
        return jsonify({'image_url': blob.public_url}), 200

    except Exception as e:
        print(f"Error while uploading: {str(e)}")
        return jsonify({'error': f'An error occurred while uploading the image: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
