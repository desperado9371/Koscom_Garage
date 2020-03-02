import Exchange_USD
import pymysql
from datetime import datetime


if __name__ == '__main__':
    print("시작")
    zTodayDate = datetime.today().strftime("%Y%m%d")
    zExchangeUSD = Exchange_USD.Get_ExchangUSD()
    conn = pymysql.connect(host="localhost", user="root", passwd="root", db="db_garage", charset ="utf8")
    curs = conn.cursor(pymysql.cursors.DictCursor)

    # ==== insert example ====
    sql = "insert into exchange_rate(base_dt,coin_type,exchange_rate) values (%s, %s, %s)"
    curs.execute(sql, (zTodayDate, 'bitcoin', float(zExchangeUSD)))
    conn.commit()