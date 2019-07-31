from lxml import html
import csv,os,json,sqlite3
import requests
from exceptions import ValueError
from time import sleep
import datetime

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)

    sleep(3)
    try:
        doc = html.fromstring(page.content)
        XPATH_NAME = '//h1[@id="title"]//text()'
        XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()' # or contains(@id,"dealprice")
        XPATH_ORIGINAL_PRICE = '//span[contains(@class,"StrikePrice")]/text()'  #contains(text(),"List Price") or contains(text(),"M.R.P") or
        XPATH_DEAL_PRICE = '//span[contains(@id,"dealprice")]/text()' # or contains(@id,"dealprice")
        XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
        XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

        RAW_NAME = doc.xpath(XPATH_NAME)
        RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
        RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
        RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
        RAW_DEAL_PRICE = doc.xpath(XPATH_DEAL_PRICE)
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

        NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
        SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).encode("utf-8").replace('\xe2\x82\xb9','').replace('\xc2\xa0','').strip() if RAW_SALE_PRICE else None
        CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
        ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).encode("utf-8").replace('\xe2\x82\xb9','').replace('\xc2\xa0','').strip() if RAW_ORIGINAL_PRICE else None
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        DEAL = ''.join(RAW_DEAL_PRICE).encode("utf-8").replace('\xe2\x82\xb9','').replace('\xc2\xa0','').strip() if RAW_DEAL_PRICE else None

        if not ORIGINAL_PRICE:
            ORIGINAL_PRICE = SALE_PRICE

        if page.status_code!=200:
            raise ValueError('captha')

        db = sqlite3.connect(os.path.join(os.path.dirname(__file__),"AmazonScrappedProducts.db"))
        c = db.cursor()
        data = (NAME,SALE_PRICE,CATEGORY,ORIGINAL_PRICE,DEAL,AVAILABILITY,url,datetime.datetime.now())
        sql = "insert into ScrapedProducts (NAME , SALE_PRICE , CATEGORY , ORIGINAL_PRICE , DEAL_PRICE , AVAILABILITY , URL, DATETIME) values(?,?,?,?,?,?,?,?)"
        c.execute(sql,data)
        db.commit()
        db.close()


    except Exception as e:
        print e


def ReadAsin():
    f = open(os.path.join(os.path.dirname(__file__),"AsinList.csv"))
    AsinList = f.readline().replace('\n','').split(',')
    f.close()

    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__),"AmazonScrappedProducts.db"))
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ScrapedProducts' ''')
    if c.fetchone()[0]==0 : {
    c.execute(''' CREATE TABLE ScrapedProducts(NAME TEXT, SALE_PRICE TEXT, CATEGORY TEXT, ORIGINAL_PRICE TEXT, DEAL_PRICE TEXT, AVAILABILITY TEXT, URL TEXT NOT NULL,DateTime TEXT); ''')
    }
    conn.commit()
    conn.close()


    for i in AsinList:
        url = "http://www.amazon.in/dp/"+i
        print "Processing: "+url
        AmzonParser(url)
        sleep(5)

if __name__ == "__main__":
    ReadAsin()
