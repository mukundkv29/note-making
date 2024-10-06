from flask import Flask, request, jsonify
# import pytesseract
from PIL import Image
import os
import pytesseract

# Replace this with the path to the tesseract executable on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to handle image upload and convert to text
@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Check if a file is uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_path)

    # Open the image and run it through Tesseract OCR
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Save the text to a .txt file
        text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file.filename}.txt")
        with open(text_file_path, 'w') as text_file:
            text_file.write(text)

        return jsonify({
            "message": "Image processed successfully",
            "text_file": text_file_path,
            "extracted_text": text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
