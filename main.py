# --code=utf-8
import requests
import json
import MySQLdb
import re
import time
import notify


try:
    log = open("log.txt","w", encoding="utf-8")
    url = "https://apapia.manmanbuy.com/index_json.ashx"
    keyword = "rtx2060"
    data = {
        "methodName"      :"getsearchkeylist",
        "zy"        :0,
        "key"   :keyword,
        "page"      :1,
        "t"       :time.time(),
        "v"       :2,
        "sign"    :time.time(),
        "c_from"  :"wx_trend",
        "jsoncallback":"?"
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
    msg = ""
    if resp.status_code == 200:
        json_txt = re.sub(r'shaixuan.*',"",resp.text)
        lists = json.loads(json_txt)
        for list in lists:
            try:
                output = "标题:{},价格:{},购买地址:{}".format(list['title'],list['price'],list['prourl'])
                curTime = time.strftime("%Y-%m-%d",time.localtime())
                msg+= output+"\n"
                sql = "insert into goods (date,pid,name,price,url,created_at)values('{}','{}','{}','{}','{}','{}')".format(curTime,list['prourl'],list['title'],list['price'].replace("￥",""),list['prourl'],curTime);
                cur.execute(sql)
                conn.commit()
            except Exception as ee:
                conn.rollback()
                print(ee.args)
        log.write(msg)    
        log.close()
except Exception as e:
    print(e.args)
    log.write(msg)
notify.sendDing()