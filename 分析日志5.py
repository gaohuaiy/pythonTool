import os  
import json  
import pandas as pd  
import concurrent.futures  
from concurrent.futures import ThreadPoolExecutor  
  

# 设置txt文件和Excel文件的文件夹路径  
txt_folder_path = 'C:\\Users\\02445\\Desktop\\log'  
csv_folder_path = 'C:\\Users\\02445\\Desktop\\excel'  
  
# 确保CSV输出文件夹存在  
os.makedirs(csv_folder_path, exist_ok=True)  
  
def process_txt_file(txt_file_path, csv_folder_path):  
    # 获取文件名（不包括扩展名）作为CSV文件名  
    base_name = os.path.splitext(os.path.basename(txt_file_path))[0]  
    csv_file_path = os.path.join(csv_folder_path, f"{base_name}.csv")  
      
    # 创建一个空列表来存储解析后的JSON数据  
    json_data = []  
      
    # 读取txt文件并解析每行的JSON数据  
    with open(txt_file_path, 'r', encoding='utf-8') as file:  
        for line in file:  
            json_obj = json.loads(line.strip())  
            json_data.append(json_obj)  
      
    # 将json_data转换为pandas DataFrame  
    df = pd.DataFrame(json_data)  
      
    # 如果DataFrame的列名不是很有用，你可能需要设置更有意义的列名  
    # 例如：df.columns = ['col1', 'col2', ...]  
      
    # 将DataFrame写入CSV文件  
    df.to_csv(csv_file_path, index=False, encoding='utf-8')  
  
# 使用ThreadPoolExecutor并发处理txt文件  
def process_txt_files_concurrently(txt_folder_path, csv_folder_path):  
    txt_files = [os.path.join(txt_folder_path, f) for f in os.listdir(txt_folder_path) if f.endswith('.txt')]  
      
    with ThreadPoolExecutor() as executor:  
        futures = [executor.submit(process_txt_file, txt_file, csv_folder_path) for txt_file in txt_files]  
        for future in concurrent.futures.as_completed(futures):  
            try:  
                future.result()  
            except Exception as e:  
                print(f"Error processing {future.args[0]}: {e}")  
  
# 调用并发处理函数  
process_txt_files_concurrently(txt_folder_path, csv_folder_path)  
print('所有txt文件的数据已写入到同名CSV文件中。')