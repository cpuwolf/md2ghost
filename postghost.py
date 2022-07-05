
# written by Wei Shuai <cpuwolf@gmail.com> July 1st, 2022

from asyncio import sleep
import requests # pip install requests
import jwt	# pip install pyjwt
from datetime import datetime as date, tzinfo
import json
import mimetypes
import os
import sys
import re
import pytz
from io import BytesIO


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

if os.name == 'nt':
    headers = {'Authorization': 'Ghost {}'.format(token)}
else:
    headers = {'Authorization': 'Ghost {}'.format(token.decode("utf-8"))}





class Md2Ghost:
    def __init__(self):
        self.title_line = "My test post"
        self.ctags_line = []
        self.all_images = []
        self.all_images_url = []
        self.html = ""
    def handle_md_file(self, filepath):

        self.ctags_line.clear()
        
        print(filepath)
        print(os.path.dirname(filepath))
        print(os.path.splitext(filepath)[0])

        image_asset_path = os.path.splitext(filepath)[0]
        image_pattern = re.compile(r'\{\%\s*asset_img\s*([0-9a-zA-Z_.]+)')
        adv_image_pattern = re.compile(r'^\!\[(.*?)\]\((.*?)\)')
        title_pattern = re.compile(r'^title:\s*(.*)')
        date_pattern = re.compile(r'^date:\s*(.*)')
        tags_header_pattern = re.compile(r'^tags:')
        tags_pattern = re.compile(r'^\s*-\s*(.*)')
        header_pattern = re.compile(r'^---')
        weblink_pattern = re.compile(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
        adv_weblink_pattern = re.compile(r'^\[(.*?)\]\((.*?)\)')
        h1_pattern = re.compile(r'^#\s*(.*?)#')
        h2_pattern = re.compile(r'^##\s*(.*?)#')
        h3_pattern = re.compile(r'^###\s*(.*?)#')


        with open(filepath, 'r', encoding="utf8") as fin:
            header_pattern_count = 0
            tags_count = 0
            for line in fin:
                #print(line)

                #extract header in .md
                header_line = header_pattern.findall(line)
                if len(header_line) > 0:
                    header_pattern_count = header_pattern_count + 1
                    print("header")
                    if header_pattern_count == 2:
                        continue
                #inside headers content
                if header_pattern_count < 2:
                    # find tile
                    title_lin = title_pattern.findall(line)
                    if len(title_lin) > 0:
                        self.title_line = title_lin[0]
                        print(title_lin[0])
                    # find date
                    date_lin = date_pattern.findall(line)
                    if len(date_lin) > 0:
                        self.date_line = date_lin[0]
                        print(date_lin[0])
                    # find tags
                    tags_header_line = tags_header_pattern.match(line)
                    if tags_header_line != None: 
                        tags_count = tags_count + 1
                        print("tags")
                    if tags_count > 0:
                        tag_lin = tags_pattern.findall(line)
                        if len(tag_lin) > 0:
                            print("\t"+tag_lin[0])
                            self.ctags_line.append(tag_lin[0])
                #
                if header_pattern_count >= 2:
                    #markdown content
                    #extract asset_img
                    image_file = image_pattern.findall(line)
                    adv_image_file = adv_image_pattern.findall(line)
                    if len(image_file) > 0:
                        image_file_path = os.path.join(image_asset_path,image_file[0])
                        if os.path.exists(image_file_path):
                            #print(image_file_path)
                            
                            dirname=os.path.dirname
                            useless_base_path = dirname(dirname(image_file_path))
                            print(useless_base_path)
                            ref_path = os.path.relpath(image_file_path, useless_base_path)
                            print(ref_path)
                            img_obj = [ image_file_path, ref_path]
                            self.all_images.append(img_obj)
                            url_path = self.upload_image(img_obj)
                            url_path = url_path.replace("\\", "/")
                            img_str= "<figure class=\"kg-card kg-image-card\"><img src=\"__GHOST_URL__/content/images/" + url_path + "\" class=\"kg-image\" alt loading=\"lazy\"></figure>"
                            print(img_str)
                            self.all_images_url.append("__GHOST_URL__/content/images/" + url_path)
                            self.html = self.html + img_str
                        else:
                            print("Cannot find image file: " + image_file_path)
                            
                    elif len(adv_image_file) > 0:
                        image_file_path_tmp = os.path.join(os.path.dirname(filepath),".."+adv_image_file[0][1])
                        print(image_file_path_tmp)
                        image_file_path = os.path.abspath(image_file_path_tmp)
                        if os.path.exists(image_file_path):
                            print(image_file_path)
                            
                            dirname=os.path.dirname
                            useless_base_path = dirname(dirname(image_file_path))
                            print(useless_base_path)
                            ref_path = os.path.relpath(image_file_path, useless_base_path)
                            print(ref_path)
                            img_obj = [ image_file_path, ref_path]
                            self.all_images.append(img_obj)
                            url_path = self.upload_image(img_obj)
                            url_path = url_path.replace("\\", "/")
                            img_str= "<figure class=\"kg-card kg-image-card\"><img src=\"__GHOST_URL__/content/images/" + url_path + "\" class=\"kg-image\" alt loading=\"lazy\"></figure>"
                            print(img_str)
                            self.all_images_url.append("__GHOST_URL__/content/images/" + url_path)
                            self.html = self.html + img_str
                        else:
                            print("Cannot find adv image file: " + image_file_path)
                            return
                    else:
                        #html convert
                        if len(line) > 1:
                            is_weblink = weblink_pattern.match(line)
                            is_adv_weblink = adv_weblink_pattern.findall(line)
                            is_h1 = h1_pattern.findall(line)
                            is_h2 = h2_pattern.findall(line)
                            is_h3 = h3_pattern.findall(line)
                            if is_weblink != None:
                                print("weblink "+line)
                                self.html = self.html + "<p><a href=\""+line+"\">"+line+"</a></p>"
                            elif len(is_adv_weblink) > 0:
                                print("adv weblink "+line)
                                self.html = self.html + "<p><a href=\""+is_adv_weblink[0][1]+"\">"+is_adv_weblink[0][0]+"</a></p>"
                            elif len(is_h3) > 0:
                                print("h3 "+line)
                                self.html = self.html + "<h3>"+is_h3[0] +"</h3>"
                            elif len(is_h2) > 0:
                                print("h2 "+line)
                                self.html = self.html + "<h2>"+is_h2[0] +"</h2>"
                            elif len(is_h1) > 0:
                                print("h1 "+line)
                                self.html = self.html + "<h1>"+is_h1[0] +"</h1>"
                            else:
                                print(is_adv_weblink)
                                print("<p>"+line +"</p>")
                                self.html = self.html + "<p>"+line +"</p>"
                        else:
                            print("<hr>")
                            #self.html = self.html + "<hr>"

    def upload_image(self, simg_file_obj):
        #upload images
        url = base_url + 'ghost/api/admin/images/upload/'
        #for idx, simg_file_obj in enumerate(self.all_images):
        print(simg_file_obj[0])
        with open(simg_file_obj[0], "rb") as image:
            img_content = BytesIO(image.read())
            content_type, _ = mimetypes.guess_type(simg_file_obj[0])
            
            _files = {"file": (simg_file_obj[0], img_content, content_type)}
            values = {"purpose": "image","rel": simg_file_obj[1]}
            print(url)
            r = requests.post(url, files=_files, headers=headers, params=values)
            #print(r.content)
            rj = r.json()
            url_image = rj["images"][0]["url"]
            print(url_image)
            url_ref_path = os.path.relpath(url_image, base_url+"content/images")
            print(url_ref_path)
            
            return url_ref_path

    def post_blog(self):
        # .md file as an input argument
        #post blog
        url = base_url + 'ghost/api/admin/posts/?source=html'
        body = {
            "posts": [
                {
                    "title": self.title_line,
                    "html": self.html,
                    #"status": "published"
                }
            ]
        }

        #<figure class="kg-card kg-image-card"><img src="__GHOST_URL__/content/images/2022/07/Quic.png" class="kg-image" alt loading="lazy" width="593" height="593"></figure>

        if hasattr(self, 'date_line'):
            date_tz_8 = date.strptime(self.date_line,'%Y-%m-%d %H:%M:%S')
            tz = pytz.timezone('Asia/Shanghai')
            obj = tz.localize(date_tz_8)
            print(obj)
            newobj = obj.astimezone(pytz.UTC)
            date_pub = newobj.strftime('%Y-%m-%dT%H:%M:%SZ')
            print(date_pub)
            body['posts'][0]['published_at'] = date_pub
        #tags
        if len(self.ctags_line) > 0:
            body['posts'][0]['tags'] = self.ctags_line

        #feature_image
        if len(self.all_images_url) > 0:
            body['posts'][0]['feature_image'] = self.all_images_url[0]
        print(body)

        r = requests.post(url, json=body, headers=headers)
        print(r.content)



if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    exit(-1)
md2ghost=Md2Ghost()
md2ghost.handle_md_file(filepath)
md2ghost.post_blog()