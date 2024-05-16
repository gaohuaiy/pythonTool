import re  
import os  
import json  
import pandas as pd  
  
# 假设你的日志文件内容如下，存储在一个名为'logfile.txt'的文件中  
# ...  
# 2024-05-13 09:01:14.667 [Thread-103632] DEBUG ... 收到CTP行情:{"..."} ...  
# ...  
# 其他非JSON的日志行  
# ...  
  
# 正则表达式，用于匹配JSON字符串  
json_pattern = r'({.*?})'  
  
  
# 文件夹路径和Excel文件名  
folder_path = 'C:\\Users\\02445\\Desktop\\0513\\0513'  
excel_file = 'output.xlsx' 
# 遍历文件夹中的所有文件  
for filename in os.listdir(folder_path):  
    if filename.endswith('.log'):
              print(filename)  
              # 创建一个空的DataFrame来存储解析后的数据  
              df_list = []   
              # 读取日志文件  
              with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:  
                            for line in file:  
                                          # 使用正则表达式查找JSON字符串  
                                          matches = re.findall(json_pattern, line)  
                                          
                                          # 对每个匹配的JSON字符串进行解析  
                                          for match in matches:  
                                                        # 去除可能的转义字符和多余的引号  
                                                        json_str = match.replace('\\"', '"')  
                                                                      
                                                        try:  
                                                                      # 解析JSON字符串为Python字典  
                                                                      data = json.loads(json_str)  
                                                                      
                                                                      # 创建一个Series，将JSON数据作为一行添加到DataFrame列表中  
                                                                      # 注意：这里假设所有JSON具有相同的结构，如果不是，你需要做适当的处理  
                                                                      series = pd.Series(data)  
                                                                      df_list.append(series)  
                                                                      
                                                        except json.JSONDecodeError as e:  
                                                                      # 打印解码错误（可选）  
                                                                      print(f"解析JSON时出错: {e}")  
                            # 将Series列表转换为DataFrame  
                            df = pd.DataFrame(df_list)  
                            
                            # 如果DataFrame为空，则不进行后续操作  
                            if not df.empty:  
                                # 将DataFrame写入Excel文件
                                excelFile = filename+'.xlsx'
                                print(excelFile)
                                df.to_excel(excelFile, index=False, engine='openpyxl')  
                                print("数据已成功写入Excel文件。")  
                            else:  
                                print("日志文件中没有找到有效的JSON数据。")