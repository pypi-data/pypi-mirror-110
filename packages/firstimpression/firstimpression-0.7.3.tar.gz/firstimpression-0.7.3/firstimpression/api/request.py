import requests
from requests.api import head


def request(url, header=None, params=None, verify=None):
    return requests.get(url, headers=header, params=params, verify=verify)
    # if header is None:
    #     if params is None and verify is None:
    #         return requests.get(url)
    #     elif params is None:
    #         return requests.get(url, verify=verify)
    #     elif verify is None:
    #         return requests.get(url, params=params)
    #     else:
    #         return requests.get(url, params=params, verify=verify)
    # elif params is None:
    #     if verify is None:
    #         return requests.get(url, headers=header)
    #     else:
    #         return requests.get(url, headers=header, verify=verify)
    # elif verify is None:
    #     return requests.get(url, headers=header, params=params)
    # else:
    #     return requests.get(url, headers=header, params=params, verify=verify)


def request_json(url, header=None, params=None, verify=None):
    response = request(url, header, params, verify)
    return response.json()
