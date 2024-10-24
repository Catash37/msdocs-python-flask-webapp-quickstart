import os

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# Set up credentials
subscription_key = os.getenv('89772058661344f592eb00a4947d2b7b')
endpoint = os.getenv('https://testwebappface.cognitiveservices.azure.com/')

# Initialize FaceClient
face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

def detect_faces(image_url):
    # Detect face from image
    detected_faces = face_client.face.detect_with_url(url=image_url)
    if not detected_faces:
        raise Exception("No face detected")

    return detected_faces[0].face_id


from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

@app.route('/detect-face', methods=['POST'])
def detect_face():
    image = request.files['image']
    image_url = save_image_to_blob(image)  # Or save locally
    face_id = detect_faces(image_url)
    return f"Face detected, ID: {face_id}"


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
