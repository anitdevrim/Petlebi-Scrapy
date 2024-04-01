import json

import scrapy


class PetlebiScrapy(scrapy.Spider):
    name = 'petlebi_scrapy'  # Assing name to the scrapy spider
    start_urls = ['https://www.petlebi.com/kus-petshop-urunleri?page=1','https://www.petlebi.com/kopek-petshop-urunleri?page=1', 'https://www.petlebi.com/kemirgen-petshop-urunleri?page=1', 'https://www.petlebi.com/kedi-petshop-urunleri?page=1']

    def parse(self, response):

        '''
        Scrapy spider will go through each url stated in start_urls.
        Each url will be fetched and get a response back.
        Then scrapy spider will look for the requested attributes and store them.
        '''

        for products in response.css('div.search-product-box'):
            # Json file that includes some of the attributes
            data = json.loads(products.css('a.p-link').attrib['data-gtm-product'])

            # Assign for each attribute
            product_brand = data.get('brand')
            product_name = data.get('name')
            product_id = data.get('id')
            product_price = int(data.get('price')[1:-2])
            product_category = data.get('category')
            product_stock = data.get('dimension2')

            # Yield Block
            yield {
                'product_name' : product_name,
                'product_id' : product_id,
                'product_brand': product_brand,
                'product_price' : product_price,
                'product_stock' : product_stock,
                'product_category' : product_category,
                'product_url' : products.css('a.p-link').attrib['href'],
                'product_img' : products.css('img.mb-2').attrib['data-original'][2:],
                'product_barcode': 'Null',
                'product_description': 'Null',
                'product_sku' : 'Null',
            }
        
        '''
        In the each category(animal) there is 30 products that are visible in a page.
        While scrolling down on website url of the website changes.
        By finding the url of the next page, we can iterate through all the products in the same category.
        Next page link for each page(until last page) is stored in a button.
        Finding the link through button named '»', we can go to the next page and fetch the data iteratively.
        '''

        next_page_link = None  # Assign it to None
        for link in response.css('a.page-link'):
            if link.css('::text').get() == '»':
                next_page_link = link.attrib.get('href')  # Get the link for next page
                break

        if next_page_link:  # If there is next page
            next_page_url = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page_url, callback=self.parse)  # Call parse function to fetch the product data
