from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from tutorial.items import DmozItem


class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.flowersinspace.com",
        "http://www.trabajostecnicos.es",
        "http://www.evalgon.com",
        "http://www.claveweb.com",
        "http://www.cococomunicazione.com",
        "http://www.3dsvq.es",
        "http://www.optiweb.es",
        "http://www.softtron.net",
        "http://www.redycomercio.com",
        "http://www.graphik.es",
        "http://www.dbisual.com",
        "http://www.recreativosdg.com",
        "http://www.gaarquitectos.com",
        "http://www.yosoytupadre.com",
        "http://www.clamsol.com",
        "http://www.estudiogokiburi.com",
        "http://www.oklan.es",
        "http://www.disenocreativo.es",
        "http://www.bassali.es/",
        "http://www.estampamultiple.com",
        "http://www.solucionesdirectas.com",
        "http://www.elsegnor3.com",
        "http://www.solucionempresarial.net",
        "http://www.fogonrural.es",
        "http://www.sputnix.es",
        "http://www.rotulia.es",
        "http://www.iniciatec.es",
        "http://www.disenograficosevilla.com",
        "http://www.redycomercio.com",
        "http://www.soltury.com",
        "http://www.evalgon.com",
        "http://www.agenciamediasur.es",
        "http://www.cococomunicazione.com",
        "http://www.asycom.es",
        "http://www.redycomercio.com",
        "http://www.lacasetadejuanleon.com/",
        "http://www.oklan.es",
        "http://www.disenocreativo.es",
        "http://habitaquo.mastmas.net",
        "http://www.e-geide.com",
        "http://www.tapasconarte.com",
        "http://www.cerotec.net",
        "http://www.semseo.es",
        "http://www.iniciatec.es",
        "http://www.redycomercio.com",
        "http://www.redycomercio.com",
        "http://reparaciondeordenadores-sevilla.blogspot.com",
        "http://www.evalgon.com",
        "http://www.grupoinova.es",
        "http://www.asycom.es",
        "http://www.softtron.net",
        "http://www.kaipioni.es",
        "http://www.finode.com",
        "http://www.svintegra.net",
        "http://www.anter.org",
        "http://www.beecoder.com",
        "http://www.disenocreativo.es",
        "http://www.sadiel.es/",
        "http://www.s-dos.es",
        "http://www.iniciatec.es",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            item['desc'] = site.select('text()').extract()
            items.append(item)
        return items
