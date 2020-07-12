import requests
import time


class Request:
    def __init__(self, config, retry=None, headers=None, use_proxy=False, payload=None, latency=0):
        self._config = config
        self._retry = retry or 5
        self._headers = headers or {
            'Accept': '*/*',
            'Accept-Encoding': 'deflate, br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Accept-Language': 'en-US;q=0.8,en;q=0.7'
        }
        self._use_proxy = use_proxy
        self._payload = payload
        self._latency = latency

    def get(self, url):
        for index in range(self._retry):
            session = requests.session()
            try:
                if self._use_proxy:
                    proxies = {
                        'http:': self._config['PROXY'],
                        'https': self._config['PROXY']
                    }
                    response = session.get(url, headers=self._headers, proxies=proxies, timeout=30)
                else:
                    response = session.get(url, headers=self._headers, timeout=30)
            except requests.RequestException:
                time.sleep(self._latency)
                continue
            else:
                return {
                    'status': response.status_code,
                    'text': response.text
                }
        return {
            'status': 449,
            'text': 'Request Max Retried'
        }

    def post(self, url):
        for index in range(self._retry):
            session = requests.session()
            try:
                if self._use_proxy:
                    proxies = {
                        'http:': self._config['PROXY'],
                        'https': self._config['PROXY']
                    }
                    response = session.post(url, headers=self._headers, proxies=proxies, data=self._payload, timeout=30)
                else:
                    response = session.post(url, headers=self._headers, data=self._payload, timeout=30)
            except requests.RequestException:
                time.sleep(self._latency)
                continue
            else:
                return {
                    'status': response.status_code,
                    'text': response.text
                }
        return {
            'status': 449,
            'text': 'Request Max Retried'
        }
