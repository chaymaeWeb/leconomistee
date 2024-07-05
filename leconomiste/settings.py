SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = 'c:/Users/chaym/Downloads/chromedriver-win64/chromedriver.exe'
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # Exécuter le navigateur en mode headless

DOWNLOADER_MIDDLEWARES = {
    'leconomiste.middlewares.SeleniumMiddleware': 543,
}

# Respecter les règles de robots.txt
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'leconomiste.pipelines.MyPipeline': 300,
}

# Paramètres dont la valeur par défaut est obsolète pour une valeur future
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Définir le codage de l'exportation des flux
FEED_EXPORT_ENCODING = "utf-8"

# Définir le format de sortie et le fichier
FEEDS = {
    'article_titles.json': {
        'format': 'json',
        'encoding': 'utf8',
        'fields': ['title'],
    },
}
