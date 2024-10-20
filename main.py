import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2

# Load your CNN model
model = tf.keras.models.load_model('Phishing-Image-Detection.h5')

# Function to preprocess the image
def preprocess_image(image):
    # Convert the image from RGBA (4 channels) to RGB (3 channels)
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Resize the image to 256x256 as expected by the model
    img = np.array(image)
    img = cv2.resize(img, (256, 256))
    img = img / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Streamlit UI
st.title("Image Classifier")
st.subheader("Phishing Website Detection")

# Upload the image
uploaded_file = st.file_uploader("Choose a PNG image...", type="png")

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image (convert to RGB if needed)
    processed_image = preprocess_image(image)
    
    # Make a prediction using the loaded model
    yhat = model.predict(processed_image)
    
    # Classification logic
    if yhat < 0.7:
        st.write("### Predicted Website is Safe")
    else:
        st.write("### Predicted Website is Phishing")

# Add a predict button (optional)
if st.button('Predict'):
    if uploaded_file is None:
        st.write("Please upload an image first.")
