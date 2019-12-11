import requests,websocket,ssl

def StatusCode(url):
   try:
       ws = websocket.create_connection(url,timeout=5,header=["User-Agent:wss_check"],sslopt={"cert_reqs": ssl.CERT_NONE})
       print(101 if ws.status == 101 else url)
   except Exception as e:
       print(url,'错误类型',e)

with open('d:/posttest/api/utils/fg','r') as f:
    for line in f.readlines():
        url = 'wss://' + line.strip()
        StatusCode(url)

