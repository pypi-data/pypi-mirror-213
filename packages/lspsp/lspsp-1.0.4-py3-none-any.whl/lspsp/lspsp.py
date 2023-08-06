from bs4 import BeautifulSoup
import requests

LSP_HOST = 'https://www.lspsp.me'


class Lspsp:
    _loginuser = None

    def __init__(self, loginuser) -> None:
        self._loginuser = loginuser

    def api(self, uri, method, data):
        url = LSP_HOST + uri
        cookies = {
            "loginUser": self._loginuser
        }
        response = requests.request(
            method=method, url=url, data=data, cookies=cookies).text
        return response

    def list(self):
        ret = {}
        html = self.api('/bonus', 'GET', '')
        bs = BeautifulSoup(html, 'html.parser')
        content = bs.select_one('.main-area #content')
        if content == None:
            return ret
        for item in content.select('.lspfree'):
            btn = item.select_one('button')
            disabled = btn.attrs.get('disabled')
            if disabled == None:
                ret[btn.attrs['data-goid']] = {
                    "name": item.select_one('.title').text,
                    "info": item.select_one('.info ul li').text,
                }
        return ret
