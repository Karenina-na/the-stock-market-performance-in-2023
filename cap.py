# 爬虫
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import pandas as pd

reflect = {
    "f1" : "",
    "f2" : "最新价",
    "f3" : "涨跌幅",
    "f4" : "涨跌额",
    "f5" : "成交量",
    "f6" : "成交额",
    "f7" : "振幅",
    "f8" : "换手率",
    "f9" : "市盈率",
    "f10" : "量比",
    "f11" : "",
    "f12" : "代码", 
    "f13" : "",
    "f14" : "名称",
    "f15" : "最高",
    "f16" : "最低",
    "f17" : "今开",
    "f18" : "昨收",
    "f20" : "市值",
    "f21" : "流通市值",
    "f22" : "",
    "f23" : "市净率",
    "f24" : "",
    "f25" : "",
    "f62" : "",
    "f115" : "",
    "f128" : "",
    "f136" : "",
    "f140" : "",
    "f141" : "",
    "f152" : "",
}

def get_data_page(page):
    # h = get_html('https://quote.eastmoney.com/center/gridlist.html?st=ChangePercent&sortType=C&sortRule=-1#hs_a_board')
    # print(h)
    time_stamp = int(time.time() * 1000)
    url_base = "https://12.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406888471835011891_1716369042850&" + \
        f"pn={page}" \
        + "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&"+ \
        f"_={time_stamp}"
    response = requests.get(url_base)
    response.encoding = 'utf-8'
    prefix = "jQuery112406888471835011891_1716369042850("
    endfix = ");"
    data = json.loads(response.text[len(prefix):-len(endfix)])
    return data["data"]['diff'], data["data"]['total']

def get_data():
    data = []
    total = 0
    for page in range(1, 100000):
        print(page * 20)
        data_temp, total = get_data_page(page)
        if page * 20 > total:
            break
        data += data_temp
    data = pd.DataFrame(data)
    # 将index替换
    index = data.columns.values.tolist()
    for i in range(len(index)):
        if index[i] in reflect:
            index[i] = reflect[index[i]]
    data.columns = index
    return data


if __name__ == "__main__":
    data = get_data()
    data.to_csv("./trading_data_" + time.strftime("%Y-%m-%d", time.localtime()) + ".csv", index=False)