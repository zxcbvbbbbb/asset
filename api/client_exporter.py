#!/bin/python3
from flask import Response, Flask, request
import websocket, json, re, requests, ssl
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime

app = Flask(__name__)


def StatusCode():
    url = request.args['target']
    try:
        ws = websocket.create_connection(url, timeout=5, header=["User-Agent:wss_check"],
                                         sslopt={"cert_reqs": ssl.CERT_NONE})
        print(url, True if ws.status == 101 else False)
        return ['', ws.status]
    except Exception as e:
        print(url, '错误类型', e)
        v = re.compile('.*status (\d{3}).*')
        print('------------------------->v匹配', v)
        if v.match(str(e)):
            code = v.match(str(e)).groups()[0]
            try:
                url = url.replace('wss://', 'https://') + '/socket/websocket'
                response = requests.get(url, timeout=5)
                if response.text.rstrip() == '404.' and response.status_code == 502:
                    code = 200
                    print('------------------------->502匹配')
                    return [response.reason, code]
                else:
                    return [str(e), code]
            except Exception:
                return [str(e), code]
        else:
            code = 999
            print('-->here is 999')
        return [str(e), code]


@app.route("/probe", methods=["GET", "POST"])
def probe():
    return Response('wss_check{error="%s"} %s' % (StatusCode()[0], str(StatusCode()[1])))


@app.route('/berrychat', methods=[
    "POST"])  # Alertmanager客户端(Prometheus)首先发送POST消息，并将所有要处理的警报发送到/api/v1/alerts,这里是http://192.168.200.216:9093/api/v1/alerts
def berrychat():
    '''以webhook的方式触发告警的推送;开放一个接口(/berrychat),用以接收webhook调用,然后解析告警内容并发送到bearychat的群'''
    chat = json.loads(request.data)
    print('-->json data', chat)
    print('-->group labels%s' % chat['groupLabels']['env'])
    if chat['groupLabels']['env'] == 'MChat-PRO':
        group = '4912'
    if chat['groupLabels']['env'] == '口袋PRO':
        group = '2545'
    if chat['groupLabels']['env'] == 'PTUAT' or chat['groupLabels']['env'] == 'PTPRO':
        group = '10956'
    if chat['groupLabels']['env'] == 'ZZPRO' or chat['groupLabels']['env'] == 'ZZVEST':
        group = '11627'
    print('-->which group %s' % group)
    data = chat['alerts']
    # summary = data[0]['annotations']['summary']
    text_list = []
    for item in data:
        name = item['labels']['name']
        status = item['status']
        if status == 'resolved':
            status = '恢复'
        elif status == 'firing':
            status = '故障'
        print('-->item status %s' % status)
        summary = item['annotations']['summary']
        description = item['annotations']['description']
        startsAt = item['startsAt'].replace('T',' ').split('.')[0]
        resolve = ''
        if item['endsAt'].startswith('0'):
            endsAt = ''
            resolve = ''
        else:
            endsAt = item['endsAt'].replace('T',' ').split('.')[0]
            resolve = '【恢复】 '
        message = status + '█' + ':' + name + '\n' + '【' + summary + '】' + '\n' + description + '\n' + '【开始】 ' \
        + startsAt + '\n' + resolve + endsAt
        print('-->item message',message)
        text_list.append(message)
    text = '\n'.join(text_list)
    url = 'https://im.hygtchat.com:15001/robot/api/incoming/message/c8ba5153e3124887b5c9cb0a4cf4b9bc'
    data = {
        "group": "%s" % group,
        "title": '告警通知',
        "text": text,
    }

    requests.post(url, timeout=5, json=data, headers={'Content-Type': 'application/json'}, verify=False)
    return Response('ok')


@app.route("/domain", methods=["GET", "POST"])
def domain():
    domain = request.args['target']
    print('-->domain', domain)
    url = 'http://whois.chinaz.com/%s' % domain
    try:
        rep = requests.get(url)
    except Exception as e:
        return Response('domain_check{info="%s"} %s' % (e, 0))

    try:
        soup = BeautifulSoup(rep.text, 'html.parser')
        tags = soup.find(attrs={'id': 'sh_info'})

        if not tags:
            return Response('domain_check{info="域名不正确"} -1')

        for tag in tags.children:
            if type(tag) == Tag:
                div = tag.div
                if (div):
                    if div.string == '过期时间':
                        expire_time = tag.span.string

        data = re.findall('\d+', expire_time)
        ret = datetime(int(data[0]), int(data[1]), int(data[2])) - datetime.now()
        print('-->days', ret.days)
        return Response('domain_check{info="%s过期"} %s' % (expire_time, ret.days))
    except Exception as e:
        return Response('domain_check{info="%s"} %s' % (e, -1))


if __name__ == "__main__":
    app.run(host="127.0.0.1")
