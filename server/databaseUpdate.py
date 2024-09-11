import numpy as np
import requests
import base64, os
import asyncio, aiohttp
import time, logging
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input, VGG16
from rembg import remove
from pocketbase import PocketBase

load_dotenv()

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
    

class DatabaseManager:
    def __init__(self, pb_url: str, collection_name: str):
        self.pb = PocketBase(pb_url)
        admin_data = self.pb.admins.auth_with_password(os.getenv('PB_ADMIN'), os.getenv('PB_PASSWORD'))
        self.collection_name = collection_name
    
    @staticmethod
    async def download_image(session, image_url: str) -> str:
        async with session.get(image_url) as response:
            img = Image.open(BytesIO(await response.read()))
            img.save("temp.jpg")
            return "temp.jpg"
        
    
    def fetch_all_items(self) -> list:
        items = []
        records = self.pb.collection(self.collection_name).get_full_list()
        for record in records:
            items.append({
                "id": record.id,
                "brand": record.brand,
                "title": record.title,
                "price": record.price,
                "image_url": record.image_url,
                "product_url": record.product_url,
                "type": record.type,
                "category": record.category,
                "available_sizes": record.available_sizes,
                "features": record.features,
            })
        return items
    
    def fetch_no_features_items(self) -> list:
        items = []
        records = self.pb.collection(self.collection_name).get_full_list()
        for record in records:
            if record.features == "":
                items.append({
                    "id": record.id,
                    "brand": record.brand,
                    "title": record.title,
                    "price": record.price,
                    "image_url": record.image_url,
                    "product_url": record.product_url,
                    "type": record.type,
                    "category": record.category,
                    "available_sizes": record.available_sizes,
                    "product_url": record.product_url,
                })
        return items
    
    def update_database_item(self, item_id: str, features: str):
        features_bytes = features.tobytes()
        features_base64 = base64.b64encode(features_bytes).decode('utf-8')
        self.pb.collection(self.collection_name).update(item_id, {
            'features': features_base64,
        })

class FeatureUpdater:
    def __init__(self, pb_url: str, collection_name: str):
        self.db_manager = DatabaseManager(pb_url, collection_name)
        self.feature_extractor = FeatureExtractor()
    
    async def update_db_features(self):
        items = self.db_manager.fetch_no_features_items()
        async with aiohttp.ClientSession() as session:
            tasks = []
            for item in items:
                tasks.append(self.process_item(session, item))
            await asyncio.gather(*tasks)
    
    async def process_item(self, session, item: dict):
        image_url = item['image_url']
        item_id = item['id']
        image_path = await DatabaseManager.download_image(session, image_url)
        features = self.feature_extractor.extract_features(image_path)
        self.db_manager.update_database_item(item_id, features)
        

# Example usage
if __name__ == "__main__":
    PB_URL = os.getenv('POCKETBASE_URL')  # URL where PocketBase is running
    COLLECTION_NAME = os.getenv('PB_COLLECTION_NAME')  # Name of the collection in PocketBase
    feature_updater = FeatureUpdater(PB_URL, COLLECTION_NAME)
    asyncio.run(feature_updater.update_db_features()) # INFO:root:Execution time: 189.2262032032013 seconds 
    # feature_updater.update_features() # INFO:root:Execution time: 342.80014300346375 seconds
