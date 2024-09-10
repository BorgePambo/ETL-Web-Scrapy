import scrapy
from coleta.items import ProductItem

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

    page_count = 1
    max_page = 10

    def parse(self, response):
        products = response.css('.ui-search-result__content')
        for product in products:
            product_item = ProductItem()

            # Extraindo preços e centavos
            prices = product.css('.andes-money-amount__fraction::text').getall()
            cents = product.css('.andes-money-amount__cents::text').getall()

            product_item['name'] = product.css('span.ui-search-item__brand-discoverability::text').get()
            product_item['description'] = product.css('.ui-search-item__title::text').get()
            product_item['old_price'] = prices[0] if len(prices) > 0 else None
            product_item['old_price_cent'] = cents[0] if len(cents) > 0 else None
            product_item['new_price'] = prices[1] if len(prices) > 1 else None
            product_item['new_price_cent'] = cents[1] if len(cents) > 1 else None
            product_item['review_number'] = product.css('.ui-search-reviews__rating-number::text').get()
            product_item['review_amount'] = product.css('.ui-search-reviews__amount::text').get()

            yield product_item

        # Navegar para a próxima página
        next_page_url = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()

        if self.page_count < self.max_page:
            if next_page_url is not None:
                next_page_url = response.urljoin(next_page_url)
                self.page_count += 1
                yield response.follow(next_page_url, callback=self.parse)
