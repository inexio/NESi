import requests
from nesi import exceptions


def create_resource(data, entrypoint):
    payload = data
    headers = {'Content-Type': 'application/json'}
    entrypoint = entrypoint

    r = requests.post(entrypoint, json=payload, headers=headers)
    if r.status_code != 201:
        raise exceptions.BadRequestError('create_resource', entrypoint, r)
    else:
        rsp = r.json()
        return str(rsp['id'])


def update_resource(data, entrypoint):
    payload = data
    headers = {'Content-Type': 'application/json'}
    entrypoint = entrypoint

    r = requests.put(entrypoint, json=payload, headers=headers)
    rsp = r.json()
    return str(rsp['id'])
