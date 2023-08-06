import requests
import random

letter = "abcdefghijqlmnpqrstuvwxyz"

class rentry:
    def __init__(self, middlewaretoken: str = "b8jg5nXa5j47dSvsECXAdNOaTSJw19hL2uS7kcaXa7nUgVUqqPPgMTrarjxVTHfo"):
        """
        middlewaretoken work like an cookie there is one by default but he can die at any moment so please put your own
        ex host = texthoster("your middlewaretoken")
        """
        self.key = ""
        self.body = ""
        self.url = "https://rentry.co/"
        self.middlewaretoken = middlewaretoken

    def set_body(self, body: str):
        """
        set_body("some data")
        """
        self.body = body

    def share(self, url= ""):
        if url == "":
            for x in range(10):
                url += random.choice(letter)
        headers = {
            'authority': 'rentry.co',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'csrftoken=KgXjw1i9LADSxVriqfAx9f3Gd8MttDW3BCwaLQvWQoWFAYQgcssdIlGGLzASlbUG',
            'origin': 'https://rentry.co',
            'referer': 'https://rentry.co/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        data = {
            'csrfmiddlewaretoken': self.middlewaretoken,
            'text': self.body,
            'edit_code': 'osintmaster-0001',
            'url': url
        }

        response = requests.post(self.url, headers=headers, data=data)
        if response.status_code == 200:
            return (True,f"rentry.co/{url}")
        else:
            return (False,response.text)

if __name__ == "__main__":
    a = rentry()
    a.set_body("api example")
    print(a.share())
