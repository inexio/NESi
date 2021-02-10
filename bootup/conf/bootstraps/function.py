import requests


def create_resource(data, entrypoint):
    payload = data
    headers = {'Content-Type': 'application/json'}
    entrypoint = entrypoint

    r = requests.post(entrypoint, json=payload, headers=headers)
    rsp = r.json()
    #print(rsp['id'])
    return str(rsp['id'])


def update_resource(data, entrypoint):
    payload = data
    headers = {'Content-Type': 'application/json'}
    entrypoint = entrypoint

    r = requests.put(entrypoint, json=payload, headers=headers)
    rsp = r.json()
    # print(rsp['id'])
    return str(rsp['id'])
