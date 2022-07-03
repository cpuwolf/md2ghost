
# written by Wei Shuai <cpuwolf@gmail.com> July 1st, 2022

import requests # pip install requests
import jwt	# pip install pyjwt
from datetime import datetime as date, tzinfo
import json

import os
import sys
import re
import pytz


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
image_pattern = re.compile(r'\{\%\s*asset_img\s*([0-9a-zA-Z_.]+)')
title_pattern = re.compile(r'^title:\s*(.*)')
date_pattern = re.compile(r'^date:\s*(.*)')
header_pattern = re.compile(r'^---')
title_line = "My test post"
with open(filepath, 'r', encoding="utf8") as fin:
    header_pattern_count = 0
    for line in fin:
        #print(line)
        #extract asset_img
        image_file = image_pattern.findall(line)
        if len(image_file) > 0:
            image_file_path = os.path.join(image_asset_path,image_file[0])
            if os.path.exists(image_file_path):
                print(image_file_path)
            else:
                print("Cannot find image file: " + image_file_path)
        #extract header in .md
        header_line = header_pattern.findall(line)
        if len(header_line) > 0:
            header_pattern_count = header_pattern_count + 1
            print("header")
        #inside headers content
        if header_pattern_count <= 2:
            # find tile
            title_lin = title_pattern.findall(line)
            if len(title_lin) > 0:
                title_line = title_lin[0]
                print(title_lin[0])
            # find date
            date_lin = date_pattern.findall(line)
            if len(date_lin) > 0:
                date_line = date_lin[0]
                print(date_lin[0])


body = {
    "posts": [
        {
            "title": title_line,
            "mobiledoc": "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[],\"markups\":[],\"sections\":[[1,\"p\",[[0,[],0,\"My post content. Work in progress...\"]]]]}",
        }
    ]
}

if 'date_line' in globals():
    date_tz_8 = date.strptime(date_line,'%Y-%m-%d %H:%M:%S')
    tz = pytz.timezone('Asia/Shanghai')
    obj = tz.localize(date_tz_8)
    print(obj)
    newobj = obj.astimezone(pytz.UTC)
    date_pub = newobj.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(date_pub)
    body['posts'][0]['published_at'] = date_pub

print(body)

r = requests.post(url, json=body, headers=headers)
print(r.content)