
#filename:requests_.py
#folder:backup
import traceback
import urllib.request as req
import base64
import numpy as np
import time
from dataclasses import dataclass
# import .__ignore
from .utils import *
from .__ignore import *
# ortak = Ortak()
@dataclass
class ConnectionClass:
    status: str
    content: str
class Requests:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Requests, cls).__new__(cls)
            cls.pp = kwargs["pp"]
            cls.uu = kwargs["uu"]
            # cls.connectionTest = ConnectionClass()
            cls.error_links_array = []
        return cls.instance
    def test_connection(self, url="https://www.google.com"):
        ret = self.make(url)
        print(f"status of the connection : {ret.status}")
        # print(f"content : {ret.content}")
        return ret.status == "connected"
    def make(cls, url=None):
        if url in cls.error_links_array:
            print(True, "bu adresi daha önce hatalılara eklemiştim tekrar bakmıyorum ...")
            return None
        if url is None:
            url = "https://stackoverflow.com/questions/11763028/python-3-urllib-http-error-407-proxy-authentication-required"
        p = base64.b64decode(cls.pp).decode("utf-8")
        proxy = req.ProxyHandler({'http': r'http://{}:{}@proxy.gmail.com:8080'.format(cls.uu, p),
                                  'https': r'https://{}:{}@proxy.gmail.com:8080'.format(cls.uu, p)})
        auth = req.HTTPBasicAuthHandler()
        delays = [1, 2]
        delay = np.random.choice(delays)
        # time.sleep(delay)
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        # headers = {
        #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        # }
        headers = {
                'user-agent': agent,
                'referrer': 'https://google.com',
                'Accept': "*/*",
                'Accept-Language': 'en-US,en;q=0.9',
                'Pragma': 'no-cache',
        }
        # Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
        req.Request(url, headers=headers)
        opener = req.build_opener(proxy, auth, req.HTTPHandler)
        req.install_opener(opener)
        try:
            conn = req.urlopen(url)
            return_str = conn.read()
            cls.status = "connected"
            # print(return_str)
        except:
            cls.status = "not connected"
            cls.error_links_array.append(url)
            print(True, "bu adresi ekledim :{}".format(cls.error_links_array))
            return_str = None
        return  ConnectionClass( cls.status , return_str)
    def error_report(cls, hash_=None):
        if hash_ is None:
            hash_ = get_random_hash( 5 )
        dec = ""
        for item in cls.error_links_array:
            dec += item + "\n"
        cls.yaz(hash_, dec)
    def yaz(self, hash_, dec):
        # hash_ = ortak.get_hash()
        if not len(dec) > 0:
            dec = "Hatalı URL isteği yok."
        try:
            with open(r'out\hatalı_adresler-{}.txt'.format(hash_), 'w', encoding="utf-8") as f:
                f.write(str(dec))
        except Exception as ex:
            traceback.print_exc()
def test():
    r = Requests(pp=pp , uu="xx")
    ret = r.test_connection()
    print(ret)
    print(get_random_hash(5))
if "__main__" == __name__:
    test()
