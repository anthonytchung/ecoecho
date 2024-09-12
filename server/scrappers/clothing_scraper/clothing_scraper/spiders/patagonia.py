import scrapy
from urllib.parse import urljoin
from clothing_scraper.items import ClothingItem


class PatagoniaSpider(scrapy.Spider):
    name = "patagonia"
    allowed_domains = ["patagonia.com"]
    start_urls = ["https://www.patagonia.com/shop/mens", 
                  "https://www.patagonia.com/shop/womens"]

    def parse(self, response):
        # Extract product details from each product card
        # print(response.body)
        
        for product in response.css('div.product-tile__content'):
            item = ClothingItem()
            item['brand'] = 'Patagonia'
            item['title'] = product.css('p.product-tile__name::text').get().strip()
            if product.css('span.sales.text-sales-price::text').get():
                item['price'] = product.css('span.sales.text-sales-price > span.value::text').get().replace('$', '').strip()
            else:
                item['price'] = product.css('span.value::text').get().replace('$', '').strip()
            srcset = product.css('source::attr(srcset)').get()
            if srcset:
                # Split the string by comma to separate different resolutions
                image_urls = srcset.split(',')
                # Each entry in image_urls now looks like "url sizeW", so split by space and get the first part
                highest_resolution_image = image_urls[-1].strip().split()[0]  # Selecting the last URL, usually the highest resolution
                item['image_url'] = highest_resolution_image
            item['product_url'] = response.url + product.css('a').attrib['href']
            
            yield item
        
        # Handle pagination if it's applicable
        page = 2
        # nextPageButton = response.css('button.f05bd4.aaa2a2.ab0e07::text').get()
        # print(nextPageButton)
        while page < 30:
            next_page = response.urljoin("?page=" + str(page))
            yield scrapy.Request(next_page, callback=self.parse)
            page += 1