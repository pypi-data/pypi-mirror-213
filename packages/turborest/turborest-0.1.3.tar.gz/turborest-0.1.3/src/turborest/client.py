import urllib.parse
import urllib.request
import json

class Client:
    def __init__(self, format: str = "json", auth: tuple = None, proxy: str = None) -> None:
        """
        Create a pyResty client
        """
        self.headers = {}
        self.headers["User-Agent"] = "TurboRest/0.1.0"
        self.headers["Content-Type"] = f"application/{format}"
        if auth:
            self.headers["Authorization"] = f"{auth[0]} {auth[1]}"
        self.json = False
        if format == "json":
            self.json = True
        self.proxy = proxy
    
    def query(self, url: str, method: str = "GET", data: dict = None) -> urllib.request.Request:
        """
        Query a REST endpoint
        """
        if data:
            data = urllib.parse.urlencode(data)
            data = data.encode("ascii")
        if self.proxy:
            proxy = urllib.request.ProxyHandler({"http": self.proxy, "https": self.proxy})
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
        req = urllib.request.Request(url, data=data, headers=self.headers, method=method)
        return req
    
    def get(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with GET
        """
        req = self.query(url, method="GET", data=data)
        res = self.send(req)
        if self.json:
            return json.loads(res)
        return res
        
    def post(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with POST
        """
        req = self.query(url, method="POST", data=data)
        res = self.send(req)
        if self.json:
            return json.loads(res)
        return res
        
    def put(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with PUT
        """
        req = self.query(url, method="PUT", data=data)
        res = self.send(req)
        if self.json:
            return json.loads(res)
        return res
        
    def delete(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with DELETE
        """
        req = self.query(url, method="DELETE", data=data)
        res = self.send(req)
        if self.json:
            return json.loads(res)
        return res
    
    def patch(self, url: str, data: dict = None) -> None:
        """
        Query a REST endpoint with PATCH
        """
        req = self.query(url, method="PATCH", data=data)
        res = self.send(req)
        if self.json:
            return json.loads(res)
        return res
        
    def send(self, req: urllib.request.Request) -> None:
        """
        Send a request
        """
        with urllib.request.urlopen(req) as res:
            return res.read().decode("utf-8")
            
        