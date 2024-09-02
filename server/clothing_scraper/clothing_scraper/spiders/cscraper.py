import scrapy
from urllib.parse import urljoin
from clothing_scraper.items import ClothingItem

class HMSpider(scrapy.Spider):
    name = 'hm_clothing'
    allowed_domains = ['hm.com']
    start_urls = ['https://www2.hm.com/en_us/men/sale/view-all.html']
    
    count = 0

    def parse(self, response):
        # Extract product details from each product card
        # print(response.body)
        
        for product in response.css('article.f0cf84'):
            item = ClothingItem()
            item['id'] = self.count
            item['title'] = product.css('h2.a04ae4::text').get().strip()
            item['sale_price'] = product.css('span.aa21e8::text').get().replace('$ ', '').strip()
            item['original_price'] = product.css('span.b19650::text').get().replace('$ ', '').strip()
            srcset = product.css('img::attr(srcset)').get()
            if srcset:
                # Split the string by comma to separate different resolutions
                image_urls = srcset.split(',')
                # Each entry in image_urls now looks like "url sizeW", so split by space and get the first part
                highest_resolution_image = image_urls[-1].strip().split()[0]  # Selecting the last URL, usually the highest resolution
                item['image_url'] = highest_resolution_image
            item['product_url'] = product.css('a.db7c79').attrib['href']
            
            self.count += 1
            yield item
        
        # Handle pagination if it's applicable
        page = 2
        # nextPageButton = response.css('button.f05bd4.aaa2a2.ab0e07::text').get()
        # print(nextPageButton)
        while page < 13:
            next_page = response.urljoin("?page=" + str(page))
            yield scrapy.Request(next_page, callback=self.parse)
            page += 1

