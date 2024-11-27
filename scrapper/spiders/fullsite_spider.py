import scrapy
from scrapper.cleaner import clean_html_content

class FullSiteSpider(scrapy.Spider):
    name = "fullsite"
    allowed_domains = [
        "dataciders.com",
        "catenate.com",
        "cth-bi.de",
        "datalytics-consulting.com",
        "www.inmediasp.de",
        "ixto.de",
        "www.paso-solutions.com",
        "prodato.de",
        "www.quinscape.de",
        "redpoint.teseon.com",
        "sd-c.de"
    ]

    start_urls = [
        "https://dataciders.com/",
        "https://catenate.com/",
        "https://cth-bi.de/",
        "https://datalytics-consulting.com/",
        "https://www.inmediasp.de/",
        "https://ixto.de/",
        "https://www.paso-solutions.com/",
        "https://prodato.de/",
        "https://www.quinscape.de/",
        "https://redpoint.teseon.com/",
        "https://sd-c.de/"
    ]

    def parse(self, response):
        # Rohdaten aus der Antwort extrahieren
        raw_html = response.body.decode('utf-8')

        # Bereinigte Daten erstellen
        cleaned_text = clean_html_content(raw_html, target_language='de')  # 'de' für Deutsch

        # Daten speichern
        yield {
            'url': response.url,
            'raw_html': raw_html,  # Unveränderte Rohdaten
            'cleaned_text': cleaned_text,  # Bereinigter Text
            'timestamp': response.headers.get('Date', '').decode('utf-8'),
        }

        # Folge allen Links auf der Seite
        for link in response.css('a::attr(href)').getall():
            if link.startswith('http') or link.startswith('/'):
                yield response.follow(link, self.parse)
