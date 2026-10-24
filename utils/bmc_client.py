import requests
import urllib3

class BMCClient:
    def __init__(self,host,username,password):
        self.base_url=f"https://{host.rstrip('/')}"
        self.session=requests.Session()
        self.username=username
        self.password=password
        self.session.verify = False
        self.session.auth=(username,password)
        self.timeout=15 

    def get(self,endpoint):
        url=f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url,timeout=self.timeout)

    def close(self):
        self.session.close()

    def post(self,endpoint,json=None):
        url=f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.post(url,json=json,timeout=self.timeout)
    