from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
import io

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('Phishing-Image-Detection.h5')

# Function to preprocess the image
def preprocess_image(image):
    # Convert the image from RGBA (4 channels) to RGB (3 channels)
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Convert PIL image to NumPy array
    img = np.array(image)

    # Resize image to match model input size
    img = cv2.resize(img, (256, 256))

    # Normalize pixel values (0-1)
    img = img / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img

# Route for image prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']

    # Read image file
    image = Image.open(io.BytesIO(file.read()))

    # Preprocess image
    processed_image = preprocess_image(image)

    # Make prediction
    yhat = model.predict(processed_image)

    # Define threshold and classify the image
    result = "Phishing" if yhat >= 0.7 else "Safe"

    return jsonify({'prediction': result, 'confidence': float(yhat[0][0])})

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
