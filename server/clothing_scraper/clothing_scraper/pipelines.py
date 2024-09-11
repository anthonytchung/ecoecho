# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests, os
from dotenv import load_dotenv
from pocketbase import PocketBase
from pocketbase.client import FileUpload

load_dotenv()

class ClothingScraperPipeline:
    def __init__(self):
        self.pb = PocketBase(os.getenv('POCKETBASE_URL'))
        admin_data = self.pb.admins.auth_with_password(os.getenv('PB_ADMIN'), os.getenv('PB_PASSWORD'))
        # print("Authentication successful:", admin_data.is_valid)
        self.collection_name = os.getenv('PB_COLLECTION_NAME')
        


    # def open_spider(self, spider):
        # Open the file and initialize a list to hold the items

    # def close_spider(self, spider):
        # Write the list of items as a JSON array to the file and close it
        # self.con.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            # Download the image
            # image_url = adapter.get('image_url')
            # image_response = requests.get(image_url, stream=True)

            # # Save the image to a temporary file
            # with open("temp.jpg", "wb") as image_file:
            #     for chunk in image_response.iter_content(1024):
            #         image_file.write(chunk)
            data = (
                {
                    "brand": adapter.get('brand'),
                    'title': adapter.get('title'),
                    'price': adapter.get('price'),
                    'original_price': adapter.get('original_price'),
                    'image_url': adapter.get('image_url'),
                    'product_url': adapter.get('product_url'),
                    "type": adapter.get('type'),
                    "category": adapter.get('category'),
                    "available_sizes": adapter.get('available_sizes'),
                    # "image": FileUpload((f"{adapter.get('title')}.png", open("temp.jpg", "rb"))),
                }
            )
            
            result = self.pb.collection(self.collection_name).create(data)
            # spider.logger.info(f"Item inserted into PocketBase: {adapter.get('title')}")
        except Exception as e:
            spider.logger.error(f"PocketBase error: {e}")

