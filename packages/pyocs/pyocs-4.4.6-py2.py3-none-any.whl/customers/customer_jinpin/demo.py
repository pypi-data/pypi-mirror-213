import requests
import json

url = "https://faas.gz.cvte.cn/function/cplm-copy-software"

payload = {
  "src_task": "ST20804198",
  "dst_task_list": ["ST20804197"],
  "modifier": "yinze"
}
headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.json())