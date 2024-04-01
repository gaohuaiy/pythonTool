import pandas as pd  
from bs4 import BeautifulSoup  
  
# 读取 HTML 文件  
# with open('table.html', 'r') as f:  
html = open('table.html', encoding='utf8')  
  
# 解析 HTML  
soup = BeautifulSoup(html, 'html.parser')  
  
# 查找表格标签  
table = soup.find('table')  
  
# 获取表格行和列数据  
rows = table.find_all('tr')  
columns = [th.text for th in rows[0].find_all('th')]  # 假设第一行是列名  
data = [[td.text for td in tr.find_all('td')] for tr in rows[1:]]  # 忽略表头行  
  
# 将数据转换为 DataFrame  
df = pd.DataFrame(data, columns=columns)  
  
# 打印 DataFrame   x: str(x).replace('\n', '')
# print(df)
arr = df[["\n关键字\n","\n概要\n"]].apply(lambda row: ' '.join(str(cell).replace('\n', '') for cell in row), axis=1).tolist()
print(arr)