from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from vagas_scraper.vagas_scraper.spiders.vagas_indeed_spider import SpiderVagas

class Obter_Dados_Busca():
    def obter_vaga(self, request: int):
        vaga = input('Qual vaga buscar? ').strip()
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

obter_dados_user = Obter_Dados_Busca()
vaga, nome_arquivo = obter_dados_user.obter_vaga(request=1)

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