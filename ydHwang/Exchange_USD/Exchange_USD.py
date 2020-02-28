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


class Exchange_USD:
    pass
