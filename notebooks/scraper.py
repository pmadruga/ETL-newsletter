import scrapy

class randomSpider(scrapy.Spider):
    name = "helpme"
    allowed_domains = ["example.com"]
    start_urls = ['http://example.com/categories', ]

    def parse(self, response):
        for i in response.css('div.CategoryTreeSection'):
            # This is where you select the subcategory url
            subcategory = i.css('Put your selector here')
            req = scrapy.Request(subcategory, callback=self.parse_subcategory)
            req.meta['category'] = i.css('a::text').extract_first()
            yield req

    def parse_subcategory(self, response):
        yield {
            'category': response.meta.get('category')
            # Select the name of the subcategory
            'subcategory': response.css('Put your selector here')
            # Select the data of the subcategory
            'subcategorydata': response.css('Put your selector here')
        }
