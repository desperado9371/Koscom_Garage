import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
import mysql.connector as sql
from datetime import datetime


def CleanText(readData):
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
    zExchangeUSD = Get_ExchangUSD()
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor()

    # ==== insert example ====
    query = "insert into exchange_rate(base_dt,coin_type,exchange_rate) values (%s, %s, %s)"
    db_cursor.execute(query, (zTodayDate, 'bitcoin', float(zExchangeUSD)))
    db_connection.commit()




