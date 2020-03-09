import Exchange_USD
import pymysql
from datetime import datetime
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

def CleanText(readData):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', str(readData))
    return text


def Get_ExchangUSD():
    fp = urllib.request.urlopen('https://finance.naver.com/marketindex/')
    source = fp.read()
    fp.close()
    class_list = ["tit", "sale"]
    soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
    soup = soup.find("span", {'class': 'value'})
    Exchang_USD = re.sub('<.+?>', '', str(soup), 0).strip()

    print(CleanText(Exchang_USD))
    return CleanText(Exchang_USD)

if __name__ == '__main__':
    print("시작")
    zTodayDate = datetime.today().strftime("%Y%m%d")
    zExchangeUSD = Exchange_USD.Get_ExchangUSD()
    conn = pymysql.connect(host="localhost", user="root", passwd="root", db="db_garage", charset ="utf8")
    curs = conn.cursor(pymysql.cursors.DictCursor)

    # ==== insert example ====
    sql = "insert into exchange_rate(base_dt,coin_type,exchange_rate) values (%s, %s, %s)"
    print(sql)
    curs.execute(sql, (zTodayDate, 'bitcoin', float(zExchangeUSD)))
    conn.commit()
    conn.close()