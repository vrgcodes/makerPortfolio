from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
import os
import cv2
import numpy as np
from deepface.DeepFace import represent
from deepface import DeepFace
from werkzeug.utils import secure_filename
from io import BytesIO




app = Flask(__name__)

cred = credentials.Certificate("astroguard-30c33-firebase-adminsdk-r7m1g-76f0dbffd8.json")
firebase_admin.initialize_app(cred, {'storageBucket':'astroguard-30c33.firebasestorage.app'})

bucket = storage.bucket()

tempPicStoreFolder = 'tempFaceStore'

@app.route('/upload', methods=['POST'])

def upload_file():
    if 'image' not in request.files or 'email' not in request.form:
        return jsonify({'message':'No data received'}), 400
    
    file = request.files['image']
    email = request.form['email']
    if file.filename == '':
        return jsonify({"message":"No selected file"}), 400
    
    file.filename = f"{email}.jpg"
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(tempPicStoreFolder, filename)
    
    file.save(file_path)
    
    embeddingFile = generateEmbedding(file_path, email)
    return embeddingFile
    

    
    


def generateEmbedding(imagePath,name):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(imagePath)
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(grayImage, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
 
    if len(faces) == 0:
        print("No faces detected in the image.")
        os.remove(imagePath)
        return jsonify({"message": "No faces detected"}), 400
    else:
        (x, y, w, h) = faces[0]
        face_img = image[y:y+h, x:x+w]
        
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        try:
            # Convert image to bytes
            _, buffer = cv2.imencode('.jpg', face_rgb)
            face_bytes = BytesIO(buffer)
            
            # Upload to cloud storage
            blob = bucket.blob(f'faces/{name}.jpg')
            blob.upload_from_file(face_bytes, content_type='image/jpeg')
            print("Successfully uploaded file")
            
            os.remove(imagePath)
            return jsonify({"message": "Face stored successfully"}), 200
        
        except Exception as e:
            print(f"Error occurred: {e}")
            os.remove(imagePath)
            return jsonify({"message": "Face not stored"}), 400

#         try:
#             embedding = represent(img_path=face_rgb, model_name="Facenet")[0]['embedding']
#             np.save(f'{name}.npy', embedding) 
#             print(f"Embedding generated and saved as {name}.npy")

#             return name
#         except Exception as e:
#             print(f"Error generating embedding: {e}")

@app.route('/recognize', methods=['POST'])
def recognize_Face():
    if 'image' not in request.files or 'email' not in request.form:
        return jsonify({'message':'No data received'}), 400
    
    file = request.files['image']
    email = request.form['email']
    if file.filename == '':
        return jsonify({"message":"No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(tempPicStoreFolder, filename)
    
    file.save(file_path)
    result = processFace(file_path, email)

    os.remove(file_path)

    if result:
        return jsonify({"message": "Face recognized successfully"}), 200
    else:
        return jsonify({"message": "Face not recognized"}), 400
    
   

def processFace(filePath, emailID):
   
    blob = bucket.blob(f'faces/{emailID}.jpg')
    temp_file_path = os.path.join(tempPicStoreFolder, f"{emailID}.jpg")

    try:
        with open(temp_file_path, "wb") as file:
            blob.download_to_file(file)
        print(f"File downloaded successfully to {temp_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
    


    try:
        faceRecResult = DeepFace.verify(filePath, temp_file_path)
        analyze = DeepFace.analyze(filePath, actions=['emotion'])
        if analyze[0]['dominant_emotion'] == "happy" or faceRecResult['verified']:
            os.remove(temp_file_path)
            return True
            
    except IndexError:
        print("Face not detected for embedding")
        os.remove(temp_file_path)
        return False
    except Exception as e:
        print(f"DeepFace error: {e}")
        os.remove(temp_file_path)
        return False

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
