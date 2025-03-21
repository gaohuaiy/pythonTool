import os
import pandas as pd  
from bs4 import BeautifulSoup  
# 读取 HTML 文件  
# with open('table.html', 'r') as f:  
#html = open('table.html', encoding='utf8')  
  
# 解析 HTML  
#soup = BeautifulSoup(html, 'html.parser')  
  
# 查找表格标签  
#table = soup.find('table')  
  
# 获取表格行和列数据  
#rows = table.find_all('tr')  
#columns = [th.text for th in rows[0].find_all('th')]  # 假设第一行是列名  
#data = [[td.text for td in tr.find_all('td')] for tr in rows[1:]]  # 忽略表头行  
  
# 将数据转换为 DataFrame  
#df = pd.DataFrame(data, columns=columns)  
  
# 打印 DataFrame   x: str(x).replace('\n', '')
# print(df)
#arr = df[["\n关键字\n","\n概要\n"]].apply(lambda row: ' '.join(str(cell).replace('\n', '') for cell in row), axis=1).tolist()

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
    folder_path = "F:\\xeq项目\\宏源恒利EQ版本发布\\2.0.3\\文档\\发布内容"  
    with open(os.path.join(folder_path,filename.replace("*","").replace(" ","_高怀玉_")+".txt"), "w") as f:  
        # 向文件中写入内容  
        s = content.replace("/fileName/",filename)
        f.write(s)  

    # 输出提示信息  
    print("文件已创建并写入内容。")

arr = [
'P008XIR-104076_XIR产品-XOTC支持三元雪球簿记',
'P008XIR-102720_XIR产品-XOTC支持二元期权簿记',
'P008XIR-104071_XIR产品-XOTC支持亚式期权簿记',
'P008XIR-104073_XIR产品-XOTC支持保本价差雪球簿记',
'P008XIR-104072_XIR产品-XOTC支持保本雪球簿记',
'P008XIR-104081_XIR产品-XOTC支持保股型敲出累计期权簿记',
'P008XIR-102721_XIR产品-XOTC支持区间累计期权簿记',
'P008XIR-104077_XIR产品-XOTC支持区间累计期权簿记',
'P008XIR-104078_XIR产品-XOTC支持单障碍敲出累计期权簿记',
'P008XIR-104065_XIR产品-XOTC支持单障碍期权簿记',
'P008XIR-104069_XIR产品-XOTC支持单鲨期权簿记',
'P008XIR-104063_XIR产品-XOTC支持双层二元期权簿记',
'P008XIR-104070_XIR产品-XOTC支持双鲨期权簿记',
'P008XIR-104079_XIR产品-XOTC支持固定收益累计期权簿记',
'P008XIR-102717_XIR产品-XOTC支持场外期权交易查询',
'P008XIR-102718_XIR产品-XOTC支持场外期权持仓查询',
'P008XIR-104064_XIR产品-XOTC支持多层二元期权簿记',
'P008XIR-104080_XIR产品-XOTC支持敲出终止累计期权簿记',
'P008XIR-104075_XIR产品-XOTC支持限亏型雪球簿记',
'P008XIR-104074_XIR产品-XOTC支持非保本返息雪球簿记',
'P008XIR-104291_XIR产品-场外期权标的下拉框性能优化'
]
for i in arr:
    wirteDoc(i,i)
