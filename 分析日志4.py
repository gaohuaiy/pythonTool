import os  
import re  
import json
import concurrent.futures 
def check_json_field(json_str, field_name):  
    try:  
        # 解析JSON字符串  
        data = json.loads(json_str)  
          
        # 检查字段是否存在  
        if field_name in data:  
            field_value = data[field_name]  
            print(field_value)  
            # 检查字段值是否为字符串且长度为6  
            if isinstance(field_value, str) or len(field_value) == 6:  
                # 检查字段值是否包含特定的字符串序列  
                if any(sub_str in field_value for sub_str in ["sn", "ta", "ag", "au"]):  
                    return True  
    except json.JSONDecodeError:  
        # 如果JSON字符串无效，返回False或抛出异常  
        return False  
      
    return False    
def extract_json_from_file(file_path, output_dir):  
    with open(file_path, 'r', encoding='utf-8') as file:  
        content = file.read()  
  
    # 使用正则表达式匹配JSON字符串  
    json_pattern = r'({.*?})'  
    matches = re.findall(json_pattern, content, re.DOTALL)  # 使用re.DOTALL来匹配多行  
  
    # 写入匹配的JSON字符串到txt文件  
    base_name = os.path.splitext(os.path.basename(file_path))[0]  
    output_file_path = os.path.join(output_dir, base_name + '.txt')  
    with open(output_file_path, 'w', encoding='utf-8') as output_file:  
        for match in matches:
            if  check_json_field(match,'iCode'):
                output_file.write(match + '\n')  # 直接写入匹配的JSON字符串，每个后面添加换行符  
  
def process_logs_concurrently(log_folder, output_dir):  
    os.makedirs(output_dir, exist_ok=True)  
    log_files = [os.path.join(log_folder, f) for f in os.listdir(log_folder) if f.endswith('.log')]  
  
    with concurrent.futures.ThreadPoolExecutor() as executor:  
        futures = [executor.submit(extract_json_from_file, file_path, output_dir) for file_path in log_files]  
        for future in concurrent.futures.as_completed(futures):  
            future.result()  # 如果出现异常，这里会抛出  
  
# 示例使用  
log_folder = 'C:\\Users\\02445\\Desktop\\0513\\0513'  
output_dir = 'C:\\Users\\02445\\Desktop\\log'  
process_logs_concurrently(log_folder, output_dir)