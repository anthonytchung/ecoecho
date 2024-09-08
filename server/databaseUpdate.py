import sqlite3
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from tensorflow.keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from typing import Tuple
from pocketbase import PocketBase
import base64

class FeatureExtractor:
    def __init__(self):
        self.model = VGG16(weights='imagenet', include_top=False, 
                           pooling='max', input_shape=(224, 224, 3))
        
    def extract_features(self, image_path: str) -> np.ndarray:
        input_image = Image.open(image_path)
        resized_image = input_image.resize((224, 224))
        image_array = np.expand_dims(image.img_to_array(resized_image), axis=0)
        return self.model.predict(image_array)

class ImageDownloader:
    @staticmethod
    def download_image(image_url: str) -> str:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.save("temp.jpg")
        return "temp.jpg"

class DatabaseManager:
    def __init__(self, pb_url: str, collection_name: str):
        self.pb = PocketBase(pb_url)
        admin_data = self.pb.admins.auth_with_password('antkjc@gmail.com', 'adminpassword')
        self.collection_name = collection_name
    
    def fetch_items(self) -> list:
        items = []
        records = self.pb.collection(self.collection_name).get_full_list()
        for record in records:
            items.append((record.id, record.image_url))
        return items
    
    def update_item_features(self, item_id: str, features: str):
        features_bytes = features.tobytes()
        features_base64 = base64.b64encode(features_bytes).decode('utf-8')
        # print(item_id, features_base64)
        self.pb.collection(self.collection_name).update(item_id, {
            'features': features_base64,
        })

class FeatureUpdater:
    def __init__(self, pb_url: str, collection_name: str):
        self.db_manager = DatabaseManager(pb_url, collection_name)
        self.feature_extractor = FeatureExtractor()
    
    def update_features(self):
        items = self.db_manager.fetch_items()
        for item_id, image_url in items:
            # print(item_id, image_url)
            image_path = ImageDownloader.download_image(image_url)
            features = self.feature_extractor.extract_features(image_path)
            self.db_manager.update_item_features(item_id, features)

# Example usage
if __name__ == "__main__":
    PB_URL = 'http://127.0.0.1:8090'  # URL where PocketBase is running
    COLLECTION_NAME = 'clothes'
    feature_updater = FeatureUpdater(PB_URL, COLLECTION_NAME)
    feature_updater.update_features()
