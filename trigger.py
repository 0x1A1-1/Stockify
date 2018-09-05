import requests
import os

try:
    import config
    url_base = config.URL_BASE
except:
    url_base = os.environ.get('URL_BASE')
    print(url_base)
#requests.request("POST", config.URL_BASE+"/refresh", data="refresh")
