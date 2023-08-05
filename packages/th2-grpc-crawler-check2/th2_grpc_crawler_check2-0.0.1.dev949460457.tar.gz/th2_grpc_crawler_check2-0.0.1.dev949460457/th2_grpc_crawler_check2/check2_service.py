from . import crawler_check2_pb2_grpc as importStub

class Check2Service(object):

    def __init__(self, router):
        self.connector = router.get_connection(Check2Service, importStub.Check2Stub)

    def crawlerConnect(self, request, timeout=None):
        return self.connector.create_request('crawlerConnect', request, timeout)

    def sendEvent(self, request, timeout=None):
        return self.connector.create_request('sendEvent', request, timeout)

    def sendMessage(self, request, timeout=None):
        return self.connector.create_request('sendMessage', request, timeout)