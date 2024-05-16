import os  
import json  
import sqlite3  
import re    
# 文件夹路径  
log_folder = 'C:\\Users\\02445\\Desktop\\0513\\0513'  
# SQLite数据库文件路径  
db_path = 'data.db'  
  
# 定义要存储的字段列表（基于JSON的key）  
fields = [  
    'exchangeID', 'productID', 'instrumentID', 'maxMarketOrderVolume',  
    'minMarketOrderVolume', 'positionDateType', 'maxMarginSideAlgorithm',  
    'startDelivDate', 'shortMarginRatio', 'combinationType', 'minLimitOrderVolume',  
    'instrumentName', 'volumeMultiple', 'underlyingMultiple', 'underlyingInstrID',  
    'longMarginRatio', 'maxLimitOrderVolume', 'priceTick', 'createDate',  
    'openDate', 'productClass', 'endDelivDate', 'optionsType', 'instLifePhase',  
    'expireDate', 'isTrading', 'deliveryMonth', 'deliveryYear', 'positionType',  
    'strikePrice', 'exchangeInstID'  
]  
  
# 连接到SQLite数据库（如果不存在则创建）  
conn = sqlite3.connect(db_path)  
c = conn.cursor()  
  
# 创建表（基于定义的字段列表）  
create_table_sql = 'CREATE TABLE IF NOT EXISTS Logs ('  
create_table_sql += ', '.join(f'{field} TEXT' for field in fields)  
create_table_sql += ');'  
c.execute(create_table_sql)  
# 假设JSON数据以这种形式出现在日志中（每行一个完整的JSON对象）  
json_pattern = re.compile(r'^{.*}$')  # 只匹配完整的JSON对象（以{}开头和结尾）    
# 遍历文件夹中的所有文件  
for root, dirs, files in os.walk(log_folder):  
    for file in files:  
        if file.endswith('.log'):  
            file_path = os.path.join(root, file)  
            with open(file_path, 'r', encoding='utf-8') as f:  
                for line in f:
                    if json_pattern.match(line):    
                            try:  
                                          # 使用正则表达式查找JSON字符串  
                                          matches = re.findall(json_pattern, line)  
                                          
                                          # 对每个匹配的JSON字符串进行解析  
                                          for match in matches:  
                                                        # 解析JSON 
                                                        # 去除可能的转义字符和多余的引号  
                                                        json_str = match.replace('\\"', '"')   
                                                        json_obj = json.loads(json_str)  
                                                        # 准备插入语句的参数（使用占位符）  
                                                        params = [json_obj.get(field, '') for field in fields]  
                                                        # 插入数据到表中  
                                                        insert_sql = 'INSERT INTO Logs ({}) VALUES ({})'.format(  
                                                                      ', '.join(fields),  
                                                                      ', '.join(['?'] * len(fields))  
                                                        ) 
                                                        print(insert_sql) 
                                                        c.execute(insert_sql, params)  
                            except json.JSONDecodeError:  
                                          # 处理解析错误（可选：记录日志、跳过等）  
                                          pass  
  
# 提交事务并关闭连接  
conn.commit()  
conn.close()