import cryptowatch as cw
import threading


class Server:
    def __init__(self):
        self.__coins = ["AAVE","ALGO","BTC","BCH","ADA","LINK","DASH","DOGE","ETH","ETC","LTC","XRP","XLM","XMR","ZEC"]
        self.__coin_names = {"AAVE":"AAVE", "ALGO":"ALGORAND", "BTC":"BITCOIN", "BCH":"BITCOIN CASH", "ADA":"CARDANO", "LINK":"CHAINLINK", "DASH":"DASH", "DOGE":"DOGECOIN", "ETH":"ETHEREUM", "ETC":"ETHEREUM CLASSIC", "LTC":"LITECOIN", "XRP":"RIPPLE", "XLM":"XLM", "XMR":"MONERO", "ZEC":"ZEC"}
        self.__cache = []
        
        threading.Thread(target=self.fetch_new_data).start()
        
    def read_coins_file(self):
        with open("coins.conf", "r") as f:
            data = f.read()
        ls = []
        data = data.split("\n")
        for line in data:
            if line in self.__coins:
                ls.append(line)
        return ls
        
    def fetch_new_data(self):
        coins = self.read_coins_file()
        ls = []
        for coin in coins:
            req = cw.markets.get("KRAKEN:{}USD".format(coin))
            data = req._http_response._content.decode()
            d = {}
            d['img'] = "{}.png".format(coin.lower())
            d['price'] = "$ {:.2f}".format(round(float(data.split('"last":')[1].split(",")[0]), 2))
            real_change = round(float(data.split('"change":')[1].split(",")[0].split(":")[1])*100, 2)
            if real_change > 0:
                d['change_colour'] = "green"
                d['change'] = "+{:.2f}%".format(real_change)
            else:
                d['change_colour'] = "red" 
                d['change'] = "{:.2f}%".format(real_change)
            d['code'] = coin
            d['name'] = self.__coin_names[coin]
            ls.append(d)
        self.__cache = ls.copy()
        time.sleep(3600)
        fetch_new_data()
        
    def get_data(self):
        return self.__cache
