
# written by Wei Shuai <cpuwolf@gmail.com> July 1st, 2022

import requests # pip install requests
import jwt	# pip install pyjwt
from datetime import datetime as date
import json

import os
import sys



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


#
if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    exit(-1)

print(filepath)
with open(filepath, 'rU' , encoding="utf8") as fin:
    for line in fin:
        print(line)
body = {
    "posts": [
        {
            "title": "My test post",
            "mobiledoc": "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[],\"markups\":[],\"sections\":[[1,\"p\",[[0,[],0,\"My post content. Work in progress...\"]]]]}",
        }
    ]
}
r = requests.post(url, json=body, headers=headers)

print(r.content)