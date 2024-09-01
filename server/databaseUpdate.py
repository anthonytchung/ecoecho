import sqlite3
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from tensorflow.keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from typing import Tuple

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
    def __init__(self, database_path: str):
        self.database_path = database_path
    
    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)
    
    def fetch_items(self) -> list:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, image_url FROM clothes")
            return cursor.fetchall()
    
    def update_item_features(self, item_id: int, features: bytes):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clothes SET features = ? WHERE id = ?", (features, item_id))
            conn.commit()

class FeatureUpdater:
    def __init__(self, database_path: str):
        self.db_manager = DatabaseManager(database_path)
        self.feature_extractor = FeatureExtractor()
        self.image_downloader = ImageDownloader()
    
    def update_features(self):
        items = self.db_manager.fetch_items()
        for item_id, image_url in items:
            try:
                image_path = self.image_downloader.download_image(image_url)
                features = self.feature_extractor.extract_features(image_path)
                features_blob = features.tobytes()
                self.db_manager.update_item_features(item_id, features_blob)
            except Exception as e:
                print(f"Error processing item {item_id}: {e}")

def main():
    clothes_db = "./clothing_scraper/clothes.db"
    updater = FeatureUpdater(clothes_db)
    updater.update_features()

if __name__ == "__main__":
    main()
