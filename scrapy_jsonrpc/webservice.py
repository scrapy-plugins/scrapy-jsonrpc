"""
Scrapy web services extension

See docs/topics/webservice.rst
"""

from twisted.web import server, resource

from scrapy.exceptions import NotConfigured
from scrapy import log, signals
from scrapy.utils.misc import load_object
from scrapy.utils.reactor import listen_tcp
from scrapy.utils.conf import build_component_list

from scrapy_jsonrpc.jsonrpc import jsonrpc_server_call
from scrapy_jsonrpc.serialize import ScrapyJSONEncoder, ScrapyJSONDecoder
from scrapy_jsonrpc.txweb import JsonResource as JsonResource_


WEBSERVICE_RESOURCES_BASE = {
    'scrapy_jsonrpc.resource.crawler.CrawlerResource': 1,
    'scrapy_jsonrpc.resource.enginestatus.EngineStatusResource': 1,
    'scrapy_jsonrpc.resource.stats.StatsResource': 1,
}


class JsonResource(JsonResource_):

    def __init__(self, crawler, target=None):
        JsonResource_.__init__(self)
        self.crawler = crawler
        self.json_encoder = ScrapyJSONEncoder(crawler=crawler)

class JsonRpcResource(JsonResource):

    def __init__(self, crawler, target=None):
        JsonResource.__init__(self, crawler, target)
        self.json_decoder = ScrapyJSONDecoder(crawler=crawler)
        self.crawler = crawler
        self._target = target

    def render_GET(self, txrequest):
        return self.get_target()

    def render_POST(self, txrequest):
        reqstr = txrequest.content.getvalue()
        target = self.get_target()
        return jsonrpc_server_call(target, reqstr, self.json_decoder)

    def getChild(self, name, txrequest):
        target = self.get_target()
        try:
            newtarget = getattr(target, name)
            return JsonRpcResource(self.crawler, newtarget)
        except AttributeError:
            return resource.ErrorPage(404, "No Such Resource", "No such child resource.")

    def get_target(self):
        return self._target


class RootResource(JsonResource):

    def render_GET(self, txrequest):
        return {'resources': self.children.keys()}

    def getChild(self, name, txrequest):
        if name == '':
            return self
        return JsonResource.getChild(self, name, txrequest)


class WebService(server.Site):

    def __init__(self, crawler):
        if not crawler.settings.getbool('WEBSERVICE_ENABLED'):
            raise NotConfigured
        self.crawler = crawler
        logfile = crawler.settings['WEBSERVICE_LOGFILE']
        self.portrange = [int(x) for x in crawler.settings.getlist('WEBSERVICE_PORT', [6023, 6073])]
        self.host = crawler.settings.get('WEBSERVICE_HOST', '127.0.0.1')
        root = RootResource(crawler)
        reslist = build_component_list(
            crawler.settings.get('WEBSERVICE_RESOURCES_BASE', WEBSERVICE_RESOURCES_BASE),
            crawler.settings.get('WEBSERVICE_RESOURCES', {})
        )
        for res_cls in map(load_object, reslist):
            res = res_cls(crawler)
            root.putChild(res.ws_name, res)
        server.Site.__init__(self, root, logPath=logfile)
        self.noisy = False
        crawler.signals.connect(self.start_listening, signals.engine_started)
        crawler.signals.connect(self.stop_listening, signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def start_listening(self):
        self.port = listen_tcp(self.portrange, self.host, self)
        h = self.port.getHost()
        log.msg(format='Web service listening on %(host)s:%(port)d',
                level=log.DEBUG, host=h.host, port=h.port)

    def stop_listening(self):
        self.port.stopListening()

