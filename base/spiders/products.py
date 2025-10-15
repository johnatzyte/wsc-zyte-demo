import scrapy
from base.items import ProductItem, CategoryItem

class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["toscrape.com"]
    
    url: str = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

    async def start(self):
        yield scrapy.Request(self.url, callback=self.parse_category)
    
    async def parse_category(self, response, item: CategoryItem):
        for book_url in item.book_urls:
            yield response.follow(book_url, callback=self.parse_book)
        if item.next_page_url:
            yield response.follow(item.next_page_url, callback=self.parse_category)

    async def parse_book(self, _, item: ProductItem):
        yield item