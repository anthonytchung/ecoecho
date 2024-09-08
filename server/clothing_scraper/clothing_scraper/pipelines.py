# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import sqlite3
from pocketbase import PocketBase



class ClothingScraperPipeline:
    def __init__(self):
        self.pb = PocketBase('http://127.0.0.1:8090')
        admin_data = self.pb.admins.auth_with_password('antkjc@gmail.com', 'adminpassword')
        # print("Authentication successful:", admin_data.is_valid)
        self.collection_name = 'clothes'

        # self.con = sqlite3.connect('./scraped_data/clothes.db')
        # self.cur = self.con.cursor()
        # self.cur.execute("""
        # CREATE TABLE IF NOT EXISTS clothes(
        #     id INTEGER PRIMARY KEY,
        #     title TEXT,
        #     price REAL,
        #     original_price REAL,
        #     image_url TEXT,
        #     product_url TEXT,
        #     features BLOB
        # )
        # """)
        # self.con.commit()
        


    def open_spider(self, spider):
        # Open the file and initialize a list to hold the items
        self.file = open('./scraped_data/clothes.json', 'w')
        self.items = []

    def close_spider(self, spider):
        # Write the list of items as a JSON array to the file and close it
        json.dump({"clothes": self.items}, self.file, indent=4)
        self.file.close()
        # self.con.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
    #         # Insert item into the SQLite database
    #         self.cur.execute("""
    #         INSERT OR IGNORE INTO clothes (id, title, price, original_price, image_url, product_url) VALUES (?, ?, ?, ?, ?, ?)
    #         """, (
    #             adapter.get('id'),
    #             adapter.get('title'),
    #             adapter.get('price'),
    #             adapter.get('original_price'),
    #             adapter.get('image_url'),
    #             adapter.get('product_url')
    #         ))
    #         self.con.commit()

            # Insert item into PocketBase
            data = (
                {
                    'title': adapter.get('title'),
                    'price': adapter.get('price'),
                    'original_price': adapter.get('original_price'),
                    'image_url': adapter.get('image_url'),
                    'product_url': adapter.get('product_url'),
                }
            )
            
            result = self.pb.collection(self.collection_name).create(data)
            spider.logger.info(f"Item inserted into PocketBase: {adapter.get('title')}")
        except Exception as e:
            spider.logger.error(f"PocketBase error: {e}")

    #     # Add the item to the list for JSON output
    #     self.items.append(adapter.asdict())
    #     return item
