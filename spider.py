import scrapy 
from scrapy_playwright.page import PageMethod
from utils import settings
from scrapy.crawler import CrawlerProcess



class CarsandBids(scrapy.Spider):
    name = 'carsandbids_spider'
    allowed_domains = ['carsandbids.com']
    custom_settings = settings


    def start_requests(self):
        """ This method is called when the spider is opened for scraping. """

        urls = ['https://carsandbids.com/?sort=listed']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_listing, errback=self.close_context_on_error, meta={
                "playwright": True,
                "playwright_context_kwargs": {
                    "ignore_https_errors": True,
                },
                "playwright_page_methods":[
                    PageMethod("wait_for_selector", "//ul[@class='auctions-list  ']"),
                ]
            })


    def parse_listing(self, response):
        for n, car in enumerate(response.xpath("//div[@class='auction-title']/a/@href")):
            url = car.get()
            yield response.follow(url, callback=self.parse_car, errback=self.close_context_on_error, meta={
                "playwright": True,
                "playwright_context": f'context_{n}',
                "playwright_include_page": True,
                "playwright_context_kwargs": {
                    "ignore_https_errors": True,
                },
                "playwright_page_methods":[
                    PageMethod("wait_for_selector", "//div[@class='quick-facts']"),
                ]
            })



    async def parse_car(self, response):
        page = response.meta['playwright_page']
        await page.close()
        await page.context.close()
        item = dict(
            year_make = self.get_title(response),
            model = self.get_value(response, 'Model'),
            description = self.get_description(response),
            sales_price = self.get_price(response),
            auction_end_date = self.get_end_date(response),
            bid_count = self.get_bid_count(response),
            comment_count = self.get_comment_count(response),
            engine = self.get_value(response, 'Engine'),
            drivetrain = self.get_value(response, 'Drivetrain'),
            mileage = self.get_value(response, 'Mileage'),
            vin = self.get_value(response, 'VIN'),
            body_style = self.get_value(response, 'Body Style'),
            transmission = self.get_value(response, 'Transmission'),
            title_status = self.get_value(response, 'Title Status'),
            exterior_color = self.get_value(response, 'Exterior Color'),
            location = self.get_value(response, 'Location'),
            interior_color = self.get_value(response, 'Interior Color'),
            seller = self.get_value(response, 'Seller'),
            seller_type = self.get_value(response, 'Seller Type')
        )
        yield item


    @staticmethod
    def get_title(response):
        title = response.xpath("//title/text()").re_first('\d{4}')
        return title


    @staticmethod
    def get_description(response):
        description = response.xpath("//div[@class='auction-title ']/following-sibling::div/h2/text()").getall()
        return "".join(description)


    @staticmethod
    def get_price(response):
        price = response.xpath("//div[@class='bid-bar ']//span[@class='bid-value']/text()").getall()
        return "".join(price)


    @staticmethod
    def get_end_date(response):
        end_date = response.xpath("//p[@class='end-time']/text()").getall()
        return "".join(end_date)


    @staticmethod
    def get_bid_count(response):
        bid_count = response.xpath("//div[@class='bid-bar ']//li[@class='num-bids']/span[@class='value']/text()").get()
        return bid_count


    @staticmethod
    def get_comment_count(response):
        comment_count = response.xpath("//div[@class='bid-bar ']//li[@class='num-comments']/span[@class='value']/text()").get()
        return comment_count


    @staticmethod
    def get_value(response, key):
        value = response.xpath(f"//div[@class='quick-facts']//dl//dt[contains(text(), '{key}')]/following-sibling::dd//text()").get()
        return value

    
    async def close_context_on_error(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        await page.context.close()


crawler = CrawlerProcess()
crawler.crawl(CarsandBids)
crawler.start()