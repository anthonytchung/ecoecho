import os
from typing import List, Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

class FeatureExtractor:
    def __init__(self):
        self.model = VGG16(weights='imagenet', include_top=False, 
                           pooling='max', input_shape=(224, 224, 3))
    
    def extract_features(self, image_path: str) -> np.ndarray:
        input_image = Image.open(image_path)
        resized_image = input_image.resize((224, 224))
        image_array = np.expand_dims(image.img_to_array(resized_image), axis=0)
        return self.model.predict(image_array)

class DatabaseManager:
    def __init__(self, database_path: str):
        self.database_path = database_path
    
    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)
    
    def fetch_items(self) -> List[tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, sale_price, original_price, image_url, product_url, features FROM clothes")
            return cursor.fetchall()

class SimilarityFinder:
    def __init__(self, database_path: str):
        self.db_manager = DatabaseManager(database_path)
    
    def find_similar_items(self, uploaded_features: np.ndarray) -> List[Dict[str, Any]]:
        items = self.db_manager.fetch_items()
        similarities = []
        for item in items:
            if item[6] is not None:
                db_features = np.frombuffer(item[6], dtype=np.float32).reshape(1, -1)
                if db_features.shape[1] == uploaded_features.shape[1]:
                    similarity_score = float(cosine_similarity(uploaded_features, db_features).reshape(1,))
                    print(similarity_score)
                    similarities.append({
                        "id": item[0],
                        "title": item[1],
                        "sale_price": item[2],
                        "original_price": item[3],
                        "image_url": item[4],
                        "product_url": item[5],
                        "similarity": similarity_score
                    })
                else:
                    print(f"Feature dimension mismatch for item {item[0]}: DB features {db_features.shape[1]}, uploaded {uploaded_features.shape[1]}")
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:3]

class ImageSimilarityApp:
    def __init__(self, upload_folder: str, database_path: str):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['UPLOAD_FOLDER'] = upload_folder
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        self.feature_extractor = FeatureExtractor()
        self.similarity_finder = SimilarityFinder(database_path)
        
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
    DATABASE_PATH = "./clothing_scraper/clothes.db"
    app = ImageSimilarityApp(UPLOAD_FOLDER, DATABASE_PATH)
    app.run()

if __name__ == "__main__":
    main()