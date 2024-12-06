from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

UPLOAD_FUNCTION_URL = "YOUR_UPLOAD_FUNCTION_URL"
PROCESS_FUNCTION_URL = "YOUR_PROCESS_FUNCTION_URL"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["image"]
        filter_type = request.form["filter"]
        filename = uploaded_file.filename

        # Upload image to Cloud Storage via Cloud Function
        files = {"image": uploaded_file.stream.read()}
        response = requests.post(
            UPLOAD_FUNCTION_URL, json={"filename": filename, "image": files}
        )
        if response.status_code != 200:
            return jsonify({"error": "Failed to upload image"}), 500

        # Process image using Cloud Function
        process_response = requests.post(
            PROCESS_FUNCTION_URL, json={"filename": filename, "filter": filter_type}
        )
        if process_response.status_code != 200:
            return jsonify({"error": "Failed to process image"}), 500

        # Get processed image URL
        processed_url = process_response.json()["url"]

        return render_template("index.html", processed_image=processed_url)

    return render_template("index.html")
