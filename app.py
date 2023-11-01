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

class Telas():
    def __init__(self) -> None:
        pg.theme('DarkAmber')
        layout = [
            [pg.Text('Insira uma profissão para buscar suas vagas:'), pg.InputText(key='profissão')],
            [pg.Button('Realizar Busca')]
        ]
        
        self.janela = pg.Window('Busca por Vagas', layout=layout)
    
    def janela_inicial(self):
        while True:
            eventos, valores = self.janela.read()
            if eventos is None:
                return None
            if eventos == 'Realizar Busca':
                if valores['profissão'] == '':
                    pg.popup_error('ERRO: Informe alguma profissão antes de realizar a busca.', )
                else:
                    return valores['profissão']
    
    def scrap_finalizado(self):
        pg.popup_ok('Extração de vagas finalizado! Verifique o arquivo criado na pasta do arquivo executado.')

app_interface = Telas()

while True:
    vaga = app_interface.janela_inicial()

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
        app_interface.scrap_finalizado()
    
    else:
        break
