import base64
from flask import Flask, request, jsonify, render_template
import face_recognition
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Global variable to store the reference encoding
reference_encoding = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_reference_image', methods=['POST'])
def upload_reference_image():
    global reference_encoding
    try:
        # Get uploaded reference image
        file = request.files['image1']
        image = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            return jsonify({"error": "No face found in the reference image."}), 400

        reference_encoding = encodings[0]
        return jsonify({"message": "Reference image uploaded successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global reference_encoding
    try:
        if reference_encoding is None:
            return jsonify({"error": "Reference image not uploaded."}), 400

        # Decode the base64 webcam frame
        frame_data = request.json.get('frame', None)
        if not frame_data:
            return jsonify({"error": "No frame data provided."}), 400

        frame_data = frame_data.split(",")[1]  # Remove "data:image/png;base64,"
        frame_image = Image.open(BytesIO(base64.b64decode(frame_data)))
        frame_image_np = face_recognition.load_image_file(BytesIO(base64.b64decode(frame_data)))

        # Encode the frame
        encodings = face_recognition.face_encodings(frame_image_np)
        if len(encodings) == 0:
            return jsonify({"similarity": "No face detected in frame."})

        frame_encoding = encodings[0]

        # Calculate the face distance
        face_distance = face_recognition.face_distance([reference_encoding], frame_encoding)[0]
        similarity_percentage = (1 - face_distance) * 100

        return jsonify({"similarity": f"{similarity_percentage:.2f}%"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
