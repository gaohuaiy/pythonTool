import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 目标网站的URL
url = 'http://software.xquant.com/'

# 创建一个文件夹来保存图片
if not os.path.exists('images'):
    os.makedirs('images')

# 发送HTTP请求获取网页内容
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 查找所有图片标签
img_tags = soup.find_all('img')

# 遍历所有图片标签并下载图片
for img in img_tags:
    # 获取图片的URL
    img_url = img.get('src')
    
    # 如果图片URL是相对路径，则将其转换为绝对路径
    img_url = urljoin(url, img_url)
    
    # 获取图片的文件名
    img_name = os.path.basename(img_url)
    
    # 下载图片并保存到本地
    img_data = requests.get(img_url).content
    with open(f'images/{img_name}', 'wb') as img_file:
        img_file.write(img_data)
    
    print(f'Downloaded: {img_name}')

print('All images downloaded.')