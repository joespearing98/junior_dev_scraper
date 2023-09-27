import scrapy
import json
import re
import csv
from benedict import benedict
from w3lib.url import add_or_replace_parameter
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import Request

# See https://www.cars24.com/ae/buy-used-cars-dubai/


class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'
    page_number = 1
    start_urls = ['https://www.cars24.com/ae/buy-used-cars-dubai/'] 

    # CSS Scraping Method:

    def parse(self, response):
        for info in response.css('div._3IIl_._1xLfH'):
            yield {
                'Brand / Make of Car': info.css('.RZ4T7::text').get(),
                'Year of Manufacture | Model': info.css('p._1i1E6::text').get(),
                'Link': info.css('a._1Lu5u').attrib['href'],
                'Engine Size': info.css('._3ZoHn li:last-child::text').get(),
                'Price (AED)': info.css('._7yds2::text').get(),
                'Mileage': info.css('._3ZoHn li:nth-child(2)::text').get(),
            }


# Putting Scraped data into CSV file

def cars24_spider_result():
    cars24_results = []

    def crawler_results(item):
        cars24_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(Car24ComSpider)
    crawler_process.start()
    return cars24_results


if __name__ == '__main__':
    cars24_data=cars24_spider_result()

    keys = cars24_data[0].keys()
    with open('cars24_data.csv', 'w', newline='') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys)
        writer.writeheader()
        writer.writerows(cars24_data)







    # Using the Network Tab
    # I think the URL needs to be in cURL format for this to work, I am unfamiliar with this. The data can be found in the JSON file from the URL below...
    # start_urls = ['https://listing-service.c24.tech/v2/vehicle?isSeoFilter=true&sf=city:DU&sf=gaId:1783738129.1695810573&size=25&spath=buy-used-cars-dubai&page=1&variant=filterV5']

    # def parse(self, response):
    #     data = json.loads(response.text)
    #     for result in data['results']:
    #         yield {
    #             'brand': result['make'],
    #             'model': result['model'],
    #             'year of manufacture': result['year'],
    #             'engine size': result['engineSize'],
    #             'fuel type': result['fuelType'],
    #             'price': result['price'],
    #             'mileage': result['odometerReading']
    #         }
        
