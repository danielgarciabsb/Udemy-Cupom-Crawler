import scrapy


class UdemySpider(scrapy.Spider):
    name = "udemy"
    start_urls = [
        'http://udemycoupon.learnviral.com/coupon-category/free100-discount/page/2/',
    ]

    def parse(self, response):
    
        fo = open("cupons.html", "a")
        
        for quote in response.css('div.item-holder'):
			titulo = quote.css('div.item-frame div.item-panel h3.entry-title').extract_first()
			percentual = quote.css('span.percent::text').extract_first()
			
			if int(percentual[:-1]) >= 75 and titulo.find('100%') != -1:
				yield {
				'text': titulo,
				'percent': percentual,
				}

				fo.write(titulo.encode('ascii', 'ignore'));
				fo.write(percentual);
            

        next_page = response.css('div.pages a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
        fo.close()