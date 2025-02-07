import scrapy
from scrapy_selenium import SeleniumRequest
import html
from leconomiste.items import LeconomisteItem

from leconomiste.items import LeconomisteItem

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["leconomiste.com"]
    start_urls = ["https://www.leconomiste.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)
    
    def parse_article(self, response):
        item = LeconomisteItem()

        item['title'] = response.css('span a.title_home::text').getall()
        item['link'] = response.meta.get('link')
        item['author'] = response.css('.author::text').re_first(r'Par\s+(.*)\|')
        item['date_published'] = response.css('.author::text').re_first(r'Le\s+(\d{2}/\d{2}/\d{4})')
        item['image_url'] = response.urljoin(response.css('img.img-responsive::attr(src)').get())

        content_elements = response.css('.field-item.even p::text').getall()
        item['content'] = " ".join(html.unescape(elem) for elem in content_elements).replace('\n', ' ').replace('\r', '')

        if item['date_published']:
            yield item
        else:
            self.logger.warning(f"No date found for article at {item['link']}. Skipping...")
        # Flash news articles
        flash_news_articles = response.css('.view-flash-news .view-content .flexslider .slides li a::attr(href)').getall()

        if not flash_news_articles:
            self.logger.warning('No flash news articles found.')
        
        for article_link in flash_news_articles:
            article_url = response.urljoin(article_link)
            self.logger.info(f'Found article link: {article_url}')
            yield SeleniumRequest(url=article_url, callback=self.parse_article, meta={'link': article_url})

        # Articles from other sections (assuming it's a single link)
        economie_links = response.css('div.col-xs-12.col-sm-12.col-md-12.col-lg-12 span.title_home a::attr(href)').getall()

        if not other_sections_links:
            self.logger.warning('No links found for other sections.')

        for link in other_sections_links:
            full_url = response.urljoin(link)
            self.logger.info(f'Found section link: {full_url}')
            yield SeleniumRequest(url=full_url, callback=self.parse_article, meta={'link': full_url})

    
        title = response.css('span a.title_home::text').getall()
        link = response.meta.get('link')

        author = response.css('.author::text').re_first(r'Par\s+(.*)\|')
        date_published = response.css('.author::text').re_first(r'Le\s+(\d{2}/\d{2}/\d{4})')

        image_url = response.urljoin(response.css('img.img-responsive::attr(src)').get())

        content_elements = response.css('.field-item.even p::text').getall()
        item['content'] = " ".join(html.unescape(elem) for elem in content_elements).replace('\n', ' ').replace('\r', '')

        if date_published:
            data = { 
                'title': title,
                'link': link,
                'author': author,
                'date_published': date_published,
                'image_url': image_url,
                'content': content
            }

            with open('articles.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
                fieldnames = ['title', 'link', 'author', 'date_published', 'image_url', 'content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(data)
        else:
            self.logger.warning(f"No date found for article at {item['link']}. Skipping...")
