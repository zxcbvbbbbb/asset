import requests

host_data = {
    'status':True,
    'data':{
        'hostname': 'c1.com',
        'disk':{'status':True,'data':'xxx'},
        'mem':{'status':True,'data':'xxx'},
        'nic':{'status':True,'data':'xxx'}
    }
}

# requests.get('http://192.168.10.146/api/asset/',params={'name':'alex'})
requests.post('http://192.168.10.146/api/asset/',
              json=host_data,
              headers={'authkey':'aaaaaaaa'})