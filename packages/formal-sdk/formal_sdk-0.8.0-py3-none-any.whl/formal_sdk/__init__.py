from . import datastore, sidecar

SERVER_URL = "https://api.formalcloud.net"
SERVER_URL_V2 = "https://adminv2.api.formalcloud.net"


class Client(object):
    """Formal Admin API Client"""

    def __init__(self, api_key):
        """Constructor.

        Args:
            api_key: Formal API Key
        """

        self.DataStoreClient = datastore.DataStoreService(SERVER_URL_V2, api_key)
        self.SidecarClient = sidecar.SidecarService(SERVER_URL, api_key)
