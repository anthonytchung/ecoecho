import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input, VGG16
from sklearn.metrics.pairwise import cosine_similarity
from pocketbase import PocketBase
from rembg import remove
from typing import List, Dict, Any
import base64

class FeatureExtractor:
    def __init__(self):
        self.model = VGG16(weights='imagenet', include_top=False, 
                           pooling='max', input_shape=(224, 224, 3))
    
    def extract_features(self, image_path: str) -> np.ndarray:
        try:
            input_image = Image.open(image_path)
            resized_image = input_image.resize((224, 224))
            image_array = np.expand_dims(img_to_array(resized_image), axis=0)
            features = self.model.predict(image_array)
            return features
        except Exception as e:
            print(f"An error occurred: {e}")
            input_image = Image.open(image_path)
            removed_bg = remove(input_image)
            resized_image = removed_bg.resize((224, 224)).convert('RGB')
            image_array = np.expand_dims(img_to_array(resized_image), axis=0)
            image_array = preprocess_input(image_array)
            features = self.model.predict(image_array)
            return features
            
            # return  # Return an empty array in case of error

class DatabaseManager:
    def __init__(self, pb_url: str, collection_name: str):
        self.pb = PocketBase(pb_url)
        self.collection_name = collection_name
        admin_data = self.pb.admins.auth_with_password('antkjc@gmail.com', 'adminpassword')
    
    def fetch_items(self) -> List[tuple]:
        records = self.pb.collection(self.collection_name).get_full_list()
        items = []
        for record in records:
            items.append({
                "id": record.id,
                "title": record.title,
                "price": record.price,
                "original_price": record.original_price,
                "image_url": record.image_url,
                "product_url": record.product_url,
                "features": record.features
            })
        return items

class SimilarityFinder:
    def __init__(self, pb_url: str, collection_name: str):
        self.db_manager = DatabaseManager(pb_url, collection_name)
    
    def find_similar_items(self, uploaded_features: np.ndarray) -> List[Dict[str, Any]]:
        items = self.db_manager.fetch_items()
        similarities = []
        for item in items:
            if item["features"] is not None:
                features_bytes = base64.b64decode(item["features"])
                db_features = np.frombuffer(features_bytes, dtype=np.float32).reshape(1, -1)
                if db_features.shape[1] == uploaded_features.shape[1]:
                    similarity_array = cosine_similarity(uploaded_features, db_features)
                    similarity_score = float(similarity_array[0, 0])
                    similarities.append({
                        "id": item["id"],
                        "title": item["title"],
                        "price": item["price"],
                        "original_price": item["original_price"],
                        "image_url": item["image_url"],
                        "product_url": item["product_url"],
                        "similarity": similarity_score
                    })
                else:
                    print(f"Feature dimension mismatch for item {item['id']}: DB features {db_features.shape[1]}, uploaded {uploaded_features.shape[1]}")
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities


class ImageSimilarityApp:
    def __init__(self, upload_folder: str, pb_url: str, collection_name: str):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['UPLOAD_FOLDER'] = upload_folder
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        self.feature_extractor = FeatureExtractor()
        self.similarity_finder = SimilarityFinder(pb_url, collection_name)
        
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route("/api/upload", methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return jsonify({'error': 'No file part in the request'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                uploaded_features = self.feature_extractor.extract_features(file_path)
                results = self.similarity_finder.find_similar_items(uploaded_features)

                return jsonify({'similarMatches': results})
    def run(self, debug: bool = True, port: int = 8080):
        self.app.run(debug=debug, port=port)


def main():
    UPLOAD_FOLDER = 'uploads'
    POCKETBASE_URL = 'http://127.0.0.1:8090'
    COLLECTION_NAME = 'clothes'
    app = ImageSimilarityApp(UPLOAD_FOLDER, POCKETBASE_URL, COLLECTION_NAME)
    app.run()

if __name__ == "__main__":
    main()