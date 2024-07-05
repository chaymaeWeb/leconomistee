import json

class MyPipeline:
    def open_spider(self, spider):
        self.file = open('articles.json', 'w')
        self.file_titles = open('article_titles.json', 'w')
        self.exported_items = []

    def close_spider(self, spider):
        self.file.write(json.dumps(self.exported_items, indent=4))
        self.file_titles.write(json.dumps([item['title'] for item in self.exported_items], indent=4))
        self.file.close()
        self.file_titles.close()

    def process_item(self, item, spider):
        # Vérifie si la date est présente dans l'article
        if 'date_published' in item:
            self.exported_items.append(dict(item))
        else:
            spider.logger.warning(f"No date found for article: {item['title']} at {item['link']}. Skipping...")
        return item
