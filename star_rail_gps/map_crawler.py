import json
import time

import requests

from star_rail_gps.utils.resources import resource_path

response = requests.get(
    "https://api-static.mihoyo.com/common/srmap/sr_map/v1/map/tree?map_id=38&app_sn=sr_map&lang=zh-cn")

tree = response.json()['data']['tree']

with open(resource_path('maps/tree.json'), 'w', encoding='utf-8') as f:
    json.dump(tree, f, indent=4, ensure_ascii=False)

name_id = {}

for parent in tree:
    for child in parent['children']:
        map_id = child['id']
        map_name = child['name']

        name_id[map_name] = map_id
        detail_url = 'https://api-static.mihoyo.com/common/srmap/sr_map/v1/map/info?map_id={}&app_sn=sr_map&lang=zh-cn'.format(
            map_id)
        detail_resp = requests.get(detail_url)

        detail_str = detail_resp.json()['data']['info']['detail']

        detail = json.loads(detail_str)
        img_url = detail['slices'][0][0]['url']

        img_resp = requests.get(img_url)
        with open(resource_path('maps/{}.png'.format(map_id)), 'wb') as f:
            f.write(img_resp.content)

        time.sleep(1)

with open(resource_path('maps/name_id.json'), 'w', encoding='utf-8') as f:
    json.dump(name_id, f, indent=4, ensure_ascii=False)
