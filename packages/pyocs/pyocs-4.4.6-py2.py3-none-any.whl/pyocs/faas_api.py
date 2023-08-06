import json
import requests
from pyocs.pyocs_login import PyocsLogin
import base64
import pprint
from pyocs.pyocs_config import PyocsConfig


def common_request(method, url, **kwargs):
    cookies = PyocsLogin().get_login_cookies_str()
    cookies_bs64 = base64.b64encode(cookies.encode())
    headers = {
        "cookies": cookies_bs64
    }
    ret = requests.request(method=method, url=url, headers=headers, **kwargs)
    return ret


def search_software(sw_info):
    config = PyocsConfig.get_config()
    faas_url_prefix = config['FAAS_URL']
    if faas_url_prefix == "DefaultValue":
        faas_url_prefix = "https://faas.gz.cvte.cn/function"
    faas_url = faas_url_prefix + "/order-search-software"
    payload = json.dumps({
        "sw_info": sw_info
    })
    response = common_request("GET", faas_url, data=payload)
    print(response.json())
    return response.json()['data']


def refresh_software_link_by_attachment_id(attachment_id):
    config = PyocsConfig.get_config()
    faas_url_prefix = config['FAAS_URL']
    if faas_url_prefix == "DefaultValue":
        faas_url_prefix = "https://faas.gz.cvte.cn/function"
    url = faas_url_prefix + "/order-refresh-software-link"
    payload = json.dumps({
        "attachment_id": attachment_id
    })
    response = common_request("GET", url, data=payload)
    print(response.json())
    return response.json()['data']


def refresh_software_link_by_sw_info(sw_info):
    config = PyocsConfig.get_config()
    faas_url_prefix = config['FAAS_URL']
    if faas_url_prefix == "DefaultValue":
        faas_url_prefix = "https://faas.gz.cvte.cn/function"
    url = faas_url_prefix + "/order-refresh-software-link"
    payload = json.dumps({
        "sw_info": sw_info
    })
    response = common_request("GET", url, data=payload)
    print(response.json())
    return response.json()['data']


def get_software_list(ocs_number, exclude_disable=True, exclude_bin=True, exclude_lock=True, use_cache=True):
    config = PyocsConfig.get_config()
    faas_url_prefix = config['FAAS_URL']
    if faas_url_prefix == "DefaultValue":
        faas_url_prefix = "https://faas.gz.cvte.cn/function"
    faas_url = faas_url_prefix + "/order-get-software-list"
    exclude_disable = "true" if exclude_disable else "false"
    exclude_bin = "true" if exclude_bin else "false"
    exclude_lock = "true" if exclude_lock else "false"
    use_cache = "true" if use_cache else "false"
    data = json.dumps({
        "ocs": ocs_number,
        "exclude_disable": exclude_disable,
        "exclude_bin": exclude_bin,
        "exclude_lock": exclude_lock,
        "use_cache": use_cache
    })
    ret = common_request("GET", faas_url, data=data)
    return ret.json()["data"]


def copy_software(src, dst):
    config = PyocsConfig.get_config()
    faas_url_prefix = config['FAAS_URL']
    if faas_url_prefix == "DefaultValue":
        faas_url_prefix = "https://faas.gz.cvte.cn/function"
    url = faas_url_prefix + "/order-copy-software"
    payload = json.dumps({
        "src": src,
        "dst": dst
    })
    ret = common_request("GET", url, data=payload)
    pprint.pprint(ret.json()['data'])
    return ret.json()["data"]


def get_order_by_factory_code(factory_code):
    config = PyocsConfig.get_config()
    faas_url_prefix = config['FAAS_URL']
    if faas_url_prefix == "DefaultValue":
        faas_url_prefix = "https://faas.gz.cvte.cn/function"
    url = faas_url_prefix + "/get-order-by-factory-code"
    payload = {
        "factory_code": factory_code
    }
    headers = {
    'Content-Type': 'application/json'
    }
    ret = requests.request("POST", url, headers=headers, json=payload)
    return ret.json()["data"]


def get_gpt_config_sample_order(order_info:dict):
    config = PyocsConfig.get_config()
    url = "http://tsc.gz.cvte.cn/v1/tools/gpt_config_sample_order"
    headers = {
    'Content-Type': 'application/json',
    "Accept-Charset" : "utf-8;q=0.7,*;q=0.7"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(order_info))
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        return None


if __name__ == '__main__':
    # search_software("20201118_195056")
    # refresh_software_link_by_attachment_id("5fb51e9a-13a0-4148-b238-6da6ac11527a")
    ret = get_software_list(ocs_number="641420", exclude_disable=False, exclude_bin=False, exclude_lock=False)
    print(ret)
