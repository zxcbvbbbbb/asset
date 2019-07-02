#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re, requests, json

data = ((3, 5001, '{"1":"美人捕鱼","3":"Beauty Fishing","4":"美人捕魚"}', 7, 'wss://hunter01.eliteaide.com', '443'), (16, 5002, '{"1":"雷霆战警","3":"X-Men","4":"雷霆戰警"}', 7, 'wss://hunter02.eliteaide.com', '443'), (17, 5003, '{"1":"捕鸟达人","3":"Birds Hunter","4":"捕鳥達人"}', 7, 'wss://hunter03.eliteaide.com', '443'), (18, 6003, '{"1":"百人牛牛","3":"Hundreds Of Bull","4":"百人牛牛"}', 6, 'wss://chess16.eliteaide.com', '443'), (43, 5004, '{"1":"欢乐捕鱼","3":"Fish Reef","4":"歡樂捕魚"}', 7, 'wss://hunter04.eliteaide.com', '443'), (44, 5005, '{"1":"天天捕鱼","3":"Daily Fishing","4":"天天捕魚"}', 7, 'wss://hunter05.eliteaide.com', '443'), (49, 6005, '{"1":"骰宝","3":"Sic Bo","4":"骰寶"}', 6, 'wss://chess15.eliteaide.com', '443'), (50, 6006, '{"1":"百家乐","3":"Baccarat","4":"百家樂"}', 6, 'wss://chess16.eliteaide.com', '443'), (157, 5006, '{"1":"捕鱼来了3D","3":"Fishing Carnival 3D","4":"捕魚嘉年華3D"}', 7, 'wss://hunter06.eliteaide.com', '443'), (165, 6501, '{"1":"抢庄牛牛","3":"Rob Banker Of Bull","4":"搶莊牛牛"}', 6, 'wss://chess02.eliteaide.com', '443'), (166, 6502, '{"1":"三公","3":"San Gong","4":"三公"}', 6, 'wss://chess02.eliteaide.com', '443'), (170, 6301, '{"1":"斗地主","3":"斗地主","4":"斗地主"}', 6, 'wss://chess03.eliteaide.com', '443'), (171, 6303, '{"1":"梭哈","3":"ShowHand","4":"梭哈"}', 6, 'wss://chess09.eliteaide.com', '443'), (173, 6666, '{"1":"欢乐德州","3":"iPoker","4":"欢乐德州"}', 6, 'wss://chess06.eliteaide.com', '443'), (175, 6011, '{"1":"十三水","3":"十三水","4":"十三水"}', 6, 'wss://chess02.eliteaide.com', '443'), (177, 6302, '{"1":"经典炸金花","3":"Classical Win Three Cards","4":"经典炸金花"}', 6, 'wss://chess04.eliteaide.com', '443'), (180, 6013, '{"1":"抢庄牌九","3":"抢庄牌九","4":"抢庄牌九"}', 6, 'wss://chess02.eliteaide.com', '443'), (181, 6012, '{"1":"二八杠","3":"二八杠","4":"二八杠"}', 6, 'wss://chess02.eliteaide.com', '443'))
ws = {}
for item in data:
    ip_port = item[4] + ':' + item[5]
    if ip_port in ws:
        ws[ip_port].append(eval(item[2])['1'])
        ws[ip_port].append(item[1])
    else:

        ws[ip_port] = (ip_port).split()
        ws[ip_port].append(eval(item[2])['1'])
        ws[ip_port].append(item[1])

print(ws)
services = {}

for service in ws:
    v1 = re.compile('.*(hunter).*')
    v2 = re.compile('.*(chess).*')
    v3 = re.compile('[\d]')
    services["Name"] = 'WS_WL'
    # services["Tags"] = ["ws_exporter",','.join(ws[service][1:]),'正式玩']
    service_ids = [item for item in ws[service] if isinstance(item, int)]
    service_names = set(ws[service][1:]) - set(service_ids)
    # print('-->service_names', service_names)
    service_names = ','.join(service_names)
    service_ids = ','.join(map(lambda x: str(x), service_ids))
    services["Tags"] = ["ws_exporter", service_ids, service_names, '正式玩']
    Address = service.replace('wss://', '').replace(':443', '')
    Port = service.split(':', 2)[-1]
    services["Address"] = Address
    services['Port'] = int(Port)
    if v1.match(service):
        services["ID"] = "prod_%s_%s_%s" % ('hunter', Address, Port)
        # print('-->services', services)

    elif v2.match(service):
        services['ID'] = 'prod_%s_%s_%s' % ('chess', Address, Port)

    headers = {"X-Consul-Token": "blizzmi.us007"}
    # res = requests.put('http://192.168.200.60:8500/v1/agent/service/register', json=services,
    #                    headers=headers)  # 入库200.60需要headers，入库200.201不需要
    # print(res.text)
    print(services)

# {'Name': 'WS_WL', 'Tags': ['ws_exporter', '6501,6502,6011,6013,6012', '抢庄牛牛,十三水,抢庄牌九,三公,二八杠', '正式玩'], 'Address': 'chess02.eliteaide.com', 'Port': 443, 'ID': 'prod_chess_chess02.eliteaide.com_443'}
# {'Name': 'WS_WL', 'Tags': ['ws_exporter', '6302', '经典炸金花', '正式玩'], 'Address': 'chess04.eliteaide.com', 'Port': 443, 'ID': 'prod_chess_chess04.eliteaide.com_443'}
#
# test = {'Name': 'test', 'Tags': ['ws_exporter', 'xx', 'yy', '正式玩'], 'Address': 'a.bc.com', 'Port': 443,
#        'ID': 'prod_swf_swf.fgfg0606.com_443'}

# requests.put('http://192.168.200.201:8500/v1/agent/service/register', json=test)  # swf入库
