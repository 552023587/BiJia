import smtplib,traceback,os,requests,time,hmac,urllib,base64,hashlib
from email.mime.text import MIMEText
def readFile(filepath):
    with open(filepath,'r',encoding='UTF-8') as fp:
        content=fp.read()
    return content

#邮件推送api来自流星云
def sendEmail():
    #要发送邮件内容
    content = readFile('log.txt')
    #接收方邮箱
    receivers = os.environ.get('EMAIL_COVER')
    #邮件主题
    subject = 'UnicomTask每日报表'
    param = '?address=' + receivers + '&name=' + subject + '&certno=' + content
    res = requests.get('http://liuxingw.com/api/mail/api.php' + param)
    res.encoding = 'utf-8'
    res = res.json()
    print(res['msg'])

#钉钉群自定义机器人推送
def sendDing():
    #要发送邮件内容
    content = readFile('log.txt')
    print(content)
    timestamp = str(round(time.time() * 1000))
    secret = 'SECf3cdf5e2b3e0904e19c338e7cc2b7dc29d0229ae1e112871e55c84699cfa4c25'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'UnicomTask每日报表',
            'text': content
        }
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    DINGTALK_WEBHOOK = ""
    res = requests.post(DINGTALK_WEBHOOK,headers=headers,json=data,verify=False)
    res.encoding = 'utf-8'
    res = res.json()
    if res['errcode'] == '0':
        print('dinngTalk push success')
    else:
        print('dinngTalk push error : ' + res['errmsg'])

