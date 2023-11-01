from typing import Any, Iterable, Optional
import scrapy
from scrapy.http import Request, Response
from vagas_scraper.vagas_scraper.items import VagasScraperItem
from scrapy.loader import ItemLoader
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep


class SpiderVagas(scrapy.Spider):
    def iniciar_driver():
        chrome_options = Options()
        LOGGER.setLevel(logging.WARNING)
        arguments = ['--headless', '--start-maximized', '--lang=pt-br']
        for argument in arguments:
            chrome_options.add_argument(argument)
    
        chrome_options.add_experimental_option('prefs', {
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_setting_values.automatic_downloads': 1
        })
        
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=chrome_options)
        
        return driver
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
},
        'FAKEUSERAGENT_PROVIDERS': [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
],
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
        
        'SCRAPEOPS_API_KEY': '<<< Sua API Key do site ScrapeOPS >>>',
        
        'SCRAPEOPS_PROXY_ENABLED': True
    }
    
    def __init__(self, vaga: str, name: str | None = None,**kwargs: Any):
        super().__init__(name, **kwargs)
        self.vaga = vaga
    
    def start_requests(self) -> Iterable[Request]:
        urls = [f'https://br.indeed.com/jobs?q={self.vaga}&']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'url_base': url})
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        for elemento in response.xpath("//div[@class='job_seen_beacon']/table"):
            loader = ItemLoader(item=VagasScraperItem(), selector=elemento, response=response)
            loader.add_xpath("Titulo_da_Vaga", ".//span[@title]/text()")
            loader.add_xpath('Nome_da_Empresa', ".//span[@data-testid='company-name']/text()")
            loader.add_xpath('Localizacao', ".//div[@data-testid='text-location']/text()")
            loader.add_xpath('Detalhes_Cargo', ".//td[@class='resultContent']/div[starts-with(@class, 'heading6 tapItem')]/div/div/text()")
            if loader.get_output_value('Titulo_da_Vaga') is None and loader.get_output_value('Nome_da_Empresa') is None:
                continue
            yield loader.load_item()
        
        
        next_page = response.urljoin(response.xpath("//a[@data-testid='pagination-page-next']/@href").get())
        yield scrapy.Request(url=next_page, callback=self.parse)
        