from flask import Flask, request, jsonify, render_template
import face_recognition
import webbrowser
from threading import Timer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare_faces', methods=['POST'])
def compare_faces():
    try:
        # Get files from request
        file1 = request.files['image1']
        file2 = request.files['image2']
        
        # Load and encode the first image
        image1 = face_recognition.load_image_file(file1)
        encodings1 = face_recognition.face_encodings(image1)
        if len(encodings1) == 0:
            return jsonify({"error": "No face found in the first image."}), 400
        encoding1 = encodings1[0]

        # Load and encode the second image
        image2 = face_recognition.load_image_file(file2)
        encodings2 = face_recognition.face_encodings(image2)
        if len(encodings2) == 0:
            return jsonify({"error": "No face found in the second image."}), 400
        encoding2 = encodings2[0]

        # Calculate the face distance
        face_distance = face_recognition.face_distance([encoding1], encoding2)[0]
        similarity_percentage = (1 - face_distance) * 100

        return jsonify({"similarity": f"{similarity_percentage:.2f}%"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    Timer(1, open_browser).start()  # Open the browser after 1 second
    app.run(debug=True)
