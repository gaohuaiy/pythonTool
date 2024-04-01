import os
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

# 定义文件名和要写入的内容  
  
def wirteDoc(filename,content):
    # 打开文件，如果文件不存在则创建它
    # 
    content = """
一、问题描述
   /fileName/
二、方案
   

三、自测场景
    
四、测试建议
  
    

五、相关脚本
  无

"""    
    # 指定文件夹路径  
    folder_path = "F:\\xeq项目\\宏源恒利EQ版本发布\\1.0.6\\文档\\发布内容"  
    with open(os.path.join(folder_path,filename.replace("*","").replace(" ","_高怀玉_")+".txt"), "w") as f:  
        # 向文件中写入内容  
        s = content.replace("/fileName/",filename)
        f.write(s)  

    # 输出提示信息  
    print("文件已创建并写入内容。")

arr = ['P013XEQ-4699 宏源恒利-多腿香草导出明细支持勾选功能']
for i in arr:
    wirteDoc(i,i)
