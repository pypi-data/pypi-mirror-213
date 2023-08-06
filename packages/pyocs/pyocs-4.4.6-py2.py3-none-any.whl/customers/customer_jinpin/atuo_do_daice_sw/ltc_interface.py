import requests


class LtcInterface:

    def ltc_get_order_item(self,payload):
        url = "https://faas.gz.cvte.cn/function/cplm-get-order-item"
        """
        payload = {
            "task_id": "22013505",
            "item": [
                "客户机型",
                "软件工程师",
                "散件类型",
                "需求数量"
            ]
        }
        """
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        return response

    def ltc_search_order_by_advance(self,payload):
        url = "https://faas.gz.cvte.cn/function/cplm-search-order-by-advance"

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response

    def ltc_get_order_software(self,task_id):
        url = "https://faas.gz.cvte.cn/function/cplm-get-order-software"

        payload = {"task_id": task_id}
        headers = {
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        return response

    def ltc_copy_software(self,src_task,dst_task_list):
        url = "https://faas.gz.cvte.cn/function/cplm-copy-software"

        payload = {
        "src_task": src_task,
        "dst_task_list": dst_task_list,
        "modifier": "linxiangna"
        }
        headers = {
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response

    def ltc_set_confirm_by_email(self,task_id,firmware_id='',test_type='',confirmed_status='',cus_confirm_info='',sw_confirm_info=''):
        url = "https://faas.gz.cvte.cn/function/cplm-set-firmware-item"

        payload = {
            "task_id": task_id,
            "modifier": "linxiangna",
            "firmware_id": firmware_id,
            "test_type": test_type,
            "confirmed_status": '邮件已确认',
            "cus_confirm_info": cus_confirm_info,
            "sw_confirm_info": sw_confirm_info,
            "no_confirm_info": None
        }
        headers = {
        'Content-Type': 'application/json',
        'Cookie': 'BIGipServerpool_yp_faas_80=1427180042.20480.0000'
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response        

    def ltc_common_interface(self,view_way, url, headers, json):
        response = requests.request(view_way, url, headers, json)
        print(response.json())
        return response
