import random
import requests


class MyRequest:
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
    ]

    def __init__(self, log):
        self.log = log

    @staticmethod
    def random_user_agent():
        return random.choice(MyRequest.USER_AGENTS)

    def header(self, data=None):
        if data is None:
            data = {}
        header = {"user-agent": self.random_user_agent()}
        header.update(data)
        return header

    def request(self, method, url, data=None, params=None, headers=None, timeout=5):
        try:
            response = requests.request(
                method,
                url,
                data=data,
                params=params,
                headers=self.header(headers),
                timeout=timeout,
            )
            if 200 <= response.status_code < 300:
                return response
            else:
                self.log.error(f"url {method} error code:{response.status_code},link:{url}")
                return False
        except requests.RequestException as e:
            self.log.error(f"{method} request error: {e}, URL:{url}")
            return False
        except Exception as e:
            self.log.error(f"{method} request Exception Error: {e}, URL:{url}")
            return False

    def get(self, url, params=None, headers=None, timeout=5):
        return self.request("GET", url, params=params, headers=headers, timeout=timeout)

    def post(self, url, data=None, headers=None, timeout=5):
        return self.request("POST", url, data=data, headers=headers, timeout=timeout)
