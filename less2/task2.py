import requests
import json
import pprint
import time

import sys

sys.stdout.encoding

url = 'https://api.vk.com/method/'
urlquery = url + 'groups.get'
iduser = 'user_id'
token = 'token'

response = requests.get(urlquery, {'user_id': iduser, 'access_token': token, 'v': '5.52'})

j_data = response.json()

urlquery = url + 'groups.getById'

out_list = []
out_dict = {}
cur_dict = {}

groups_usr = j_data.get('response').get('items')
# trx=0
for group_usr in groups_usr:
    currgroup = requests.get(urlquery,
                             {'user_id': iduser, 'group_ids': group_usr, 'access_token': token, 'fields': 'name',
                              'v': '5.52'})
    j_group = currgroup.json()
    try:
        usergroup = j_group.get('response')[0].get('name')
        cur_dict['name'] = usergroup
        out_list.append(cur_dict)
        cur_dict = {}
        print(group_usr)
    except TypeError:
        print(f'ошибка определения типа для группы с id ={group_usr}')


    time.sleep(3)

out_dict['response'] = out_list
out_json1 = json.dumps(out_dict, indent=1, ensure_ascii=False)

print(out_list)
print(out_json1)
