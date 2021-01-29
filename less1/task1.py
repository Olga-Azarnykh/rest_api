# https://docs.github.com/rest/reference/repos#list-repositories-for-the-authenticated-user
# repos = requests.get('https://api.github.com/user/repos', auth=(username, password))
import requests

username = "xshadowx2@ya.ru"
password = "password"
url = f'https://api.github.com/users/Olga-Azarnykh/repos'
response = requests.get(url, auth=(username, password))
j_data = response.json()

# print(response.text)
# print(j_data)

for resp in response.json():
    print(resp['name'])
