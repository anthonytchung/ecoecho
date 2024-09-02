# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import sqlite3


class ClothingScraperPipeline:
    def __init__(self):
        self.con = sqlite3.connect('./scraped_data/clothes.db')
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS clothes(
            id INTEGER PRIMARY KEY,
            title TEXT,
            sale_price REAL,
            original_price REAL,
            image_url TEXT,
            product_url TEXT,
            features BLOB
        )
        """)

        self.con.commit()


    def open_spider(self, spider):
        # Open the file and initialize a list to hold the items
        self.file = open('./scraped_data/clothes.json', 'w')
        self.items = []
    
    def close_spider(self, spider):
        # Write the list of items as a JSON array to the file and close it
        json.dump({"clothes": self.items}, self.file, indent=4)
        self.file.close()
        self.con.close()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            # Insert item into the database
            self.cur.execute("""
            INSERT INTO clothes (id, title, sale_price, original_price, image_url, product_url) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                adapter.get('id'),
                adapter.get('title'),
                adapter.get('sale_price'),
                adapter.get('original_price'),
                adapter.get('image_url'),
                adapter.get('product_url')
            ))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"\n\nAn error occurred\n {e}")
        # Add the item to the list
        self.items.append(dict(item))
        return item
