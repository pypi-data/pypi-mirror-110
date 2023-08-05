import time
import pandas as pd
import requests
import sys
import re
import os
import json
import calendar
import math
from datetime import datetime
from itertools import cycle
from tabulate import tabulate
from colorama import Fore, Style 
from Stock import Stock
from data import __Data

sectors = ["devbank", "banking", "finance", "hotels", "manufacture", "others",
           "hydropower", "trading", "nonlifeinsu", "devbank"]

class NEPSE(__Data):
    def __init__(self, _list):
        super().__init__()
        self.symbol_list = _list
        self.stocks_list = self.get_stocks_info()
        self.df = pd.DataFrame(columns=["Symbol", "LTP", "change", "%change",
            "Volume", "PC", "Open", "Close", "low - high", "52 weekrange", 
            "total shares","total public", "networth"])


    def get_stocks_info(self):
        return [Stock(i) for i in self.symbol_list]


    def scrape_stocks_prices(self):
        _remove_stock = list()
        for i in self.stocks_list:
            print(f"{self.stocks_list.index(i)+1}", end="\r")
            x = i.get_price_info()
            if not x:
                _remove_stock.append(i)
        for _ in _remove_stock:
            self.stocks_list.remove(_)


    def _print_table(self, df):
        print(tabulate(df, headers="keys",
                       tablefmt='pretty', showindex=False))
    

    def print_stocks_prices(self):
        # self.scrape_stocks_prices()
        if len(self.stocks_list)==0: return
        for i in self.stocks_list:
            if i.change < 0:
                i.ltp = f"{i.ltp}{Fore.RED}"
            elif i.change > 0:
                i.ltp = f"{i.ltp}{Fore.GREEN}"
            else:
                pass
            dict_ = {
                "Symbol": i.symbol,
                "LTP": i.ltp,
                "change": i.change,
                "%change": i.change_p,
                "PC": f"{i.PC}{Style.RESET_ALL}",
                "Volume" :i.volume,
                "Open": i.Open,
                "Close": i.Close,
                "low - high": f"{i.low}-{i.high}",
                "52 weekrange": f"{i.range_l}-{i.range_h}={i.range_h-i.range_l}",
                "total shares": i.total_listed,
                "total public": i.total_public,
                "networth": i.networth,
            }

            self.df = self.df.append(dict_, ignore_index=True)
        # print(tabulate(self.df.sort_values("%change"), headers="keys",
                       # tablefmt='pretty', showindex=False))
        print(tabulate(self.df.sort_values("Volume"), headers="keys",
                       tablefmt='pretty', showindex=False))
        print(f"total trading scripts: {len(self.stocks_list)}")

    def get_subindices(self):
        r_indices = requests.get(
                self.url_index, 
                headers=self.alt_headers
            ).json()
        r_nepse= requests.get(
                self.url_nepse, 
                headers=self.alt_headers
            ).json()
        r_nepse = [x for x in r_nepse if x["index"] == "NEPSE Index"]
        r_indices.append(r_nepse[0])
        df = pd.DataFrame(
            columns=["index", "change", "perChange", "currentValue"])
        copy_df = df.copy()
        for i in r_indices:
            x = dict()
            x["perChange"] = i["perChange"]
            x["change"] = i["change"]
            if i["change"] < 0:
                x["index"] = str(i["index"]) + f"{Fore.RED}"
                x["currentValue"] = f"{Style.RESET_ALL}" + \
                    str(i["currentValue"])
            if i["change"] > 0:
                x["index"] = str(i["index"]) + f"{Fore.GREEN}"
                x["currentValue"] = f"{Style.RESET_ALL}" + \
                    str(i["currentValue"])

            if i["index"] == "NEPSE Index":
                i["change"] = x["change"]
                i["index"] = x["index"]
                i["currentValue"] = x["currentValue"]
                copy_df = copy_df.append(i, ignore_index=True)
                continue
            df = df.append(x, ignore_index=True)
        #for nepse
        x = requests.get(self.url_nepse, headers=self.alt_headers).json()
        
        # print(df["index"])
        print(tabulate(df.sort_values("perChange", ascending=False),
                headers="keys", tablefmt='pretty', showindex=False)
            )

        print(tabulate(copy_df.dropna(axis=1), headers="keys",
            tablefmt='pretty', showindex=False))


    def get_market_summary(self):
        x = requests.get(self.url_market_summary, headers = self.alt_headers).json()
        self.market_summary = dict()
        for i in x:
            self.market_summary[f"{i['detail']}"] = i['value'] 
            print(f"{i['detail']} = {i['value']}")

    def __get_total_transaction(self):
        pass

    def save_floorsheet(self):
        self.get_market_summary()
        columns = ['S.N.','Symbol', 'Buyer',
                   'Seller', 'Quantity', 'Rate', 'Amount']
        total_iteration = math.ceil(self.market_summary["Total Transactions"]/500)
        table_list = list()
        data = json.dumps({"id":194})
        for _ in range(0, total_iteration):
            url_floorsheet = ("https://newweb.nepalstock.com.np/api/nots/"
                    f"nepse-data/floorsheet?page={_}"
                    "&size=500&sort=contractId,desc")
            try:
                print(f"{_+1}", end = "\r")
                r = requests.post(
                        url_floorsheet,
                        headers=self.headers,
                        data = data
                    ).json()
            except:
                time.sleep(0.4)
                r = requests.post(
                        url_floorsheet,
                        headers=self.headers,
                        data = data
                    ).json()
            floorsheet = r["floorsheets"]["content"]
            for x in floorsheet:
                dict_ = { 
                    "S.N.": _+1,
                    "Symbol": x["stockSymbol"],
                    "Buyer": x["buyerMemberId"],
                    "Seller":x["sellerMemberId"],
                    "Quantity":x["contractQuantity"],
                    "Rate":x["contractRate"],
                    "Amount": x["contractAmount"],
                }
                table_list.append(dict_)
        df = pd.DataFrame(table_list, columns=columns)
        date = datetime.now()
        weekday = calendar.day_name[date.weekday()]
        self.floorsheet = df
        df.to_csv(("/home/buddha/Code/python/webautomation/nepse_floorsheet"
                f"/datas/floorsheet_{date.date()}_{weekday}.csv"))

        # print(tabulate(df, headers="keys", tablefmt='pretty', showindex=False))

