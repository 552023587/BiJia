import requests
import json
import MySQLdb
import re
import time



try:
    log = open("log.txt")
    url = "https://www.inn-chain.com/GetProuctDataList"
    keyword = "rtx2060"
    key     = "DqqthFfsA772sha0iKh/7TF02nbA3L13"
    data = {
        "page"      :1,
        "zy"        :0,
        "keyWord"   :keyword,
        "type"      :"",
        "key"       :key
    }
    conn= MySQLdb.connect(
        host='localhost',
        port = 3308,
        user='root',
        passwd='123456',
        db ='BiJia',
        charset="utf8"
        )
    cur = conn.cursor()
    resp = requests.post(url,data=data,verify=False)
    if resp.status_code == 200:
        lists = json.loads(resp.text)
        for list in lists:
            output = "标题:{},价格:{},购买地址:{}".format(list['title'],list['price'],list['prourl']);
            #log.write(output)
            print(output)
            curTime = time.strftime("%Y-%m-%d",time.localtime())
            sql = "insert into goods (date,pid,name,price,url,created_at)values('{}','{}','{}','{}','{}','{}')".format(curTime,list['prourl'],list['title'],list['price'].replace("￥",""),list['prourl'],curTime);
            cur.execute(sql)
            conn.commit()
except Exception as e:
    conn.rollback() 
    print(e.args)