# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class ColetaPipeline:
    def process_item(self, item, spider):
        return item
    

class ProductPipeline:

    def process_item(self, item, spider):
        ##instaciando a classe 
        adapter = ItemAdapter(item)

        values = ['old_price', 'old_price_cent', 'new_price', 'new_price_cent']

        for value_key in values:
            value = adapter.get(value_key)
            value = value.replace('"', '')
            adapter[value_key] = float(value)

    
        # Obtém o valor da chave 'review_number' como string
        clean_review_numb = adapter.get('review_number')
        if clean_review_numb is not None:
            adapter['review_number'] = float(clean_review_numb)
        else:
            adapter['review_number'] = 0


        #"review_amount": "(1170)"
        clean_review_amount = adapter.get('review_amount')
        if clean_review_amount:
            value = clean_review_amount.replace('(', '').replace(')', '')
            adapter['review_amount'] = float(value)
        else:
            adapter['review_amount'] = 0

        return item

