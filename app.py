from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import os

app = Flask(__name__, static_folder="static", template_folder="static")  # Ensure static and template folders are correctly set
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

API_KEY = "key_75200c77f44253c3920c36214aa0a177fd054d27d28fddf4dcd53b6dc53ec3831aa7f39597baac575d38024c89bb105168671b5f90191c7b74a2446207b3cd99"
RUNWAY_API_URL = "https://api.runwayml.com/v1/models/image-to-image/query"


# Serve the homepage
@app.route('/')
def index():
    return app.send_static_file('index.html')  # Serve the frontend file from /static/index.html

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    try:
        # Send image to RunwayML API
        with open(image_path, 'rb') as f:
            response = requests.post(
                RUNWAY_API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                files={"image": f}
            )
        if response.status_code != 200:
            return jsonify({"error": "RunwayML API failed", "details": response.text}), 500

        # Save the output image
        output_image_path = os.path.join(OUTPUT_FOLDER, f"output_{image.filename}")
        with open(output_image_path, 'wb') as out_f:
            out_f.write(response.content)

        return jsonify({"output_url": f"/outputs/output_{image.filename}"})

    except Exception as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

@app.route('/outputs/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
