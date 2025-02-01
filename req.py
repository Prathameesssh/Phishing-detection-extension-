import requests

# Define the URL for the API endpoint
url = "http://127.0.0.1:5000/predict"

# Path to the image you want to send
file_path = "C:/Users/Prathamesh/Desktop/Image-phishing-detection/image.png"

# Open the image file and send it as part of the request
with open(file_path, "rb") as image_file:
    files = {"file": image_file}
    response = requests.post(url, files=files)

# Print the response from the Flask server
print(response.json())
