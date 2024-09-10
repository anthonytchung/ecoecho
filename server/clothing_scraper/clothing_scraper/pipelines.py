# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
from pocketbase import PocketBase
from pocketbase.client import FileUpload



class ClothingScraperPipeline:
    def __init__(self):
        self.pb = PocketBase('http://ec2-3-128-254-179.us-east-2.compute.amazonaws.com:8090')
        admin_data = self.pb.admins.auth_with_password('antkjc@gmail.com', 'adminpassword')
        # print("Authentication successful:", admin_data.is_valid)
        self.collection_name = 'clothes'
        


    # def open_spider(self, spider):
        # Open the file and initialize a list to hold the items

    # def close_spider(self, spider):
        # Write the list of items as a JSON array to the file and close it
        # self.con.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            # Download the image
            image_url = adapter.get('image_url')
            image_response = requests.get(image_url, stream=True)

            # Save the image to a temporary file
            with open("temp.jpg", "wb") as image_file:
                for chunk in image_response.iter_content(1024):
                    image_file.write(chunk)
            data = (
                {
                    'title': adapter.get('title'),
                    'price': adapter.get('price'),
                    'original_price': adapter.get('original_price'),
                    'image_url': adapter.get('image_url'),
                    'product_url': adapter.get('product_url'),
                    # "image": FileUpload((f"{adapter.get('title')}.png", open("temp.jpg", "rb"))),
                }
            )
            
            result = self.pb.collection(self.collection_name).create(data)
            # spider.logger.info(f"Item inserted into PocketBase: {adapter.get('title')}")
        except Exception as e:
            spider.logger.error(f"PocketBase error: {e}")

