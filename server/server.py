import os, base64
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
from databaseUpdate import FeatureExtractor, DatabaseManager

load_dotenv()


class SimilarityFinder:
    def __init__(self, pb_url: str, collection_name: str):
        self.db_manager = DatabaseManager(pb_url, collection_name)
    
    def find_similar_items(self, uploaded_features: np.ndarray) -> list[dict[str, any]]:
        items = self.db_manager.fetch_all_items()
        results = []
        for item in items:
            if item["features"] is not None:
                features_bytes = base64.b64decode(item["features"])
                db_features = np.frombuffer(features_bytes, dtype=np.float32).reshape(1, -1)
                if db_features.shape[1] == uploaded_features.shape[1]:
                    similarity_array = cosine_similarity(uploaded_features, db_features)
                    similarity_score = float(similarity_array[0, 0])
                    results.append({
                        "id": item["id"],
                        "brand": item["brand"],
                        "title": item["title"],
                        "price": item["price"],
                        "image_url": item["image_url"],
                        "product_url": item["product_url"],
                        "type": item["type"],
                        "category": item["category"],
                        "available_sizes": item["available_sizes"],
                        "similarity": similarity_score
                    })
                else:
                    print(f"Feature dimension mismatch for item {item['id']}: DB features {db_features.shape[1]}, uploaded {uploaded_features.shape[1]}")
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results


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
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    POCKETBASE_URL = os.getenv('POCKETBASE_URL')
    COLLECTION_NAME = os.getenv('PB_COLLECTION_NAME')
    app = ImageSimilarityApp(UPLOAD_FOLDER, POCKETBASE_URL, COLLECTION_NAME)
    app.run()

if __name__ == "__main__":
    main()