from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from vagas_scraper.vagas_scraper.spiders.vagas_indeed_spider import SpiderVagas
import PySimpleGUI as pg
from time import sleep

class Tratamento_de_Dados():
    def formatar_vaga(self, vaga, request: int):
        vaga = str(vaga).strip()
        nome_vaga = vaga
        if ' ' in vaga:
            nome_vaga = vaga.replace(' ', '_')
            vaga = vaga.replace(' ', '+')
        if request == 1:
            return vaga, nome_vaga
        elif request == 2:
            return vaga
        elif request == 3:
            return nome_vaga

class Windows():
    def __init__(self) -> None:
        pg.theme('DarkAmber')
        layout = [
            [pg.Text('Type the job title for search jobs:'), pg.InputText(key='job_title')],
            [pg.Button('Start Search')]
        ]
        
        self.janela = pg.Window('Search of Jobs', layout=layout)
    
    def initial_window(self):
        while True:
            eventos, valores = self.janela.read()
            if eventos is None:
                return None
            if eventos == 'Start Search':
                if valores['job_title'] == '':
                    pg.popup_error('ERROR: Type the job title before to start the Web Scraping.', )
                else:
                    return valores['job_title']
    
    def scrapy_finished(self):
        pg.popup_ok('Web Scraping of jobs finished! Verify the CSV file created on app folder.')

app_interface = Windows()

while True:
    vaga = app_interface.initial_window()

    if vaga is not None:
        obter_dados_user = Tratamento_de_Dados()
        vaga, nome_arquivo = obter_dados_user.formatar_vaga(vaga=vaga, request=1)

        bot = CrawlerProcess(
            settings={
                'FEEDS': {
                    f'{nome_arquivo}.csv': {'format': 'csv'}
                }
            }
        )

        # spider = SpiderVagas(vaga=vaga, name='vagasSpider')

        bot.crawl(SpiderVagas, vaga=vaga, name='vagasSpider', )
        bot.start()
        app_interface.scrapy_finished()
    
    else:
        break
