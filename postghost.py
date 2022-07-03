
# written by Wei Shuai <cpuwolf@gmail.com> July 1st, 2022

import requests # pip install requests
import jwt	# pip install pyjwt
from datetime import datetime as date
import json

import os
import sys
import re


with open(".config.json", "r") as f:
    ghost_config = json.load(f)
    base_url=ghost_config['base_url']
    admin_key=ghost_config['admin_key']
    

# Admin API key goes here
print(admin_key)

# Split the admin_key into ID and SECRET
id, secret = admin_key.split(':')

# Prepare header and payload
iat = int(date.now().timestamp())

header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
payload = {
    'iat': iat,
    'exp': iat + 5 * 60,
    'aud': '/admin/'
}


# Create the token (including decoding secret)
token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

print(token)

if os.name == 'nt':
    print('Ghost {}'.format(token))
else:
    print('Ghost {}'.format(token.decode("utf-8")))

# Make an authenticated request to create a post
url = base_url + 'ghost/api/admin/posts/'
if os.name == 'nt':
    headers = {'Authorization': 'Ghost {}'.format(token)}
else:
    headers = {'Authorization': 'Ghost {}'.format(token.decode("utf-8"))}


# .md file as an input argument
if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    exit(-1)

print(filepath)
print(os.path.basename(filepath))
print(os.path.splitext(filepath)[0])

image_asset_path = os.path.splitext(filepath)[0]
image_pattern = re.compile(r'\{\%\s*asset_img\s*([0-9a-zA-Z_.]+)\s')

with open(filepath, 'r', encoding="utf8") as fin:
    for line in fin:
        #print(line)
        image_file = image_pattern.findall(line)
        if len(image_file) > 0:
            image_file_path = os.path.join(image_asset_path,image_file[0])
            if os.path.exists(image_file_path):
                print(image_file_path)
            else:
                printf("Cannot find image file: " + image_file_path)

body = {
    "posts": [
        {
            "title": "My test post",
            "mobiledoc": "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[],\"markups\":[],\"sections\":[[1,\"p\",[[0,[],0,\"My post content. Work in progress...\"]]]]}",
        }
    ]
}
#r = requests.post(url, json=body, headers=headers)

#print(r.content)