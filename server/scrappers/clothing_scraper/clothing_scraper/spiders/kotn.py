import scrapy, re
from urllib.parse import urljoin
from clothing_scraper.items import ClothingItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse



class KotnSpider(scrapy.Spider):
    name = "kotn"
    allowed_domains = ["kotn.com"]
    start_urls = ["https://kotn.com/en/collections/womens", 
                  "https://kotn.com/en/collections/mens"]
    
    def __init__(self, *args, **kwargs):
        super(KotnSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(10)  # Wait for the page to load

        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')

        # Extract product details from each product card
        for product in response.css('div.ProductCard_container__cdrf0'):
            item = ClothingItem()
            item['brand'] = 'KOTN'
            item['title'] = product.css('h2.ProductCard_title__BY8Xw::text').get().strip()
            item['price'] = product.css('p.ProductCard_text__zdpS_::text').get().replace('$', '').strip()
            original_image_url = product.css('img.ProductCard_image__exZ38::attr(src)').get()
            # https://cdn.shopify.com/s/files/1/0932/1356/files/Women_sMariamTank_BlueLotus2_100x.jpg?v=1725383617
            # https://cdn.shopify.com/s/files/1/0932/1356/files/WOMEN_S-MARIAM-TANK_BLUE-LOTUS_640x.progressive.jpg?v=1724805817

            # https://cdn.shopify.com/s/files/1/0932/1356/files/Women_sLeilaCardigan_LightNimbusMelange2_100x.jpg?v=1725383146
            # https://cdn.shopify.com/s/files/1/0932/1356/files/WOMEN_S-LEILA-CARDIGAN_LIGHT-NIMBUS-MELANGE_256x.progressive.jpg?v=1724808085

            # https://cdn.shopify.com/s/files/1/0932/1356/files/Women_sDoubleBreastedWoolBlazer_908Jesi2_100x.jpg?v=1725391750
            # https://cdn.shopify.com/s/files/1/0932/1356/files/WOMEN_S-DOUBLE-BREASTED-WOOL-BLAZER_908-JESI_256x.progressive.jpg?v=1725391789

            # https://cdn.shopify.com/s/files/1/0932/1356/files/Men_sMemphisDenimShirt_MidnightWash2_100x.jpg?v=1725372317
            # https://cdn.shopify.com/s/files/1/0932/1356/files/MEN_S-MEMPHIS-DENIM-SHIRT_MIDNIGHT-WASH_3840x.progressive.jpg?v=1725372288
            item['image_url'] = transform_url(original_image_url)
            item['product_url'] = response.urljoin(product.css('a').attrib['href'])
            
            yield item
        
        # Handle pagination if it's applicable
        page = 2
        # nextPageButton = response.css('button.f05bd4.aaa2a2.ab0e07::text').get()
        # print(nextPageButton)
        while page < 30:
            next_page = response.urljoin("?page=" + str(page))
            yield scrapy.Request(next_page, callback=self.parse)
            page += 1

    def closed(self, reason):
        self.driver.quit()



def transform_url(url):
    # Step 1: Extract the filename and version
    match = re.search(r'/files/(.+?)(\?v=\d+)?$', url)
    if not match:
        return url  # Return original URL if no match found

    filename = match.group(1)
    version = match.group(2) if match.group(2) else ''

    # Step 2: Transform the filename
    # Convert to uppercase
    filename = filename.upper()
    
    # Replace spaces and underscores with hyphens
    filename = re.sub(r'[\s_]+', '-', filename)
    
    # Remove number before the file extension
    filename = re.sub(r'_\d+x', '', filename)
    
    # Change image resolution
    filename = re.sub(r'\.(jpg|jpeg|png|gif)$', r'_3840x.progressive.\1', filename)

    # Step 3: Adjust version number if present
    if version:
        version_num = int(version[3:])  # Extract number after '?v='
        new_version_num = max(1, version_num - 29)  # Ensure it doesn't go below 1
        version = f'?v={new_version_num}'

    # Step 4: Reconstruct the URL
    transformed_url = re.sub(r'/files/.+?(\?v=\d+)?$', f'/files/{filename}{version}', url)

    return transformed_url


print(transform_url("https://cdn.shopify.com/s/files/1/0932/1356/files/Women_sMariamTank_BlueLotus2_100x.jpg?v=1725383617"))