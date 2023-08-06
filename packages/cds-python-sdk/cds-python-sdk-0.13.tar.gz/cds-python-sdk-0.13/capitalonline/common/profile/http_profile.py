# -*- coding: utf-8 -*-

class HttpProfile(object):
    scheme = "https"

    def __init__(self, protocol=None, endpoint=None, reqMethod="POST", reqTimeout=60,
                 keepAlive=False, proxy=None, rootDomain=None, certification=None):
        """HTTP profile.
        :param protocol: http or https, default is https.api
        :type protocol: str
        :param endpoint: The domain to access, like: cdsapi.capitalonline.net
        :type endpoint: str
        :param reqMethod: the http method, valid choice: GET, POST
        :type reqMethod: str
        :param reqTimeout: The http timeout in second.
        :type reqTimeout: int
        :param rootDomain: The root domain to access, like: cdsapi.capitalonline.net.
        :type rootDomain: str
        """
        self.endpoint = endpoint
        self.reqTimeout = 60 if reqTimeout is None else reqTimeout
        self.reqMethod = "POST" if reqMethod is None else reqMethod
        self.protocol = protocol or "https"
        # protocol is not precise word according to rfc
        self.scheme = self.protocol
        self.keepAlive = keepAlive
        self.proxy = proxy
        self.rootDomain = "cdsapi.capitalonline.net" if rootDomain is None else rootDomain
        self.certification = certification