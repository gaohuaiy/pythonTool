import os  
import pandas as pd  
  
# 指定输入文件夹和输出文件夹  
input_folder = 'C:\\Users\\02445\\Desktop\\excel'  # 例如: 'C:/Users/username/input_folder'  
output_folder = 'C:\\Users\\02445\\Desktop\\merge'  # 例如: 'C:/Users/username/output_folder'  
output_filename = 'merged_file.csv'  # 合并后的CSV文件名  
  
# 确保输出文件夹存在  
if not os.path.exists(output_folder):  
    os.makedirs(output_folder)  
  
# 初始化一个空的DataFrame来存储合并后的数据  
merged_df = pd.DataFrame()  
  
# 遍历输入文件夹中的所有CSV文件  
for filename in os.listdir(input_folder):  
    if filename.endswith('.csv'):  
        file_path = os.path.join(input_folder, filename)
        try:  
            # 读取CSV文件  
            df = pd.read_csv(file_path)
            if (df.empty):  # 如果数据框是空的（即没有行），也可以视为“空文件”  
                print(f"Skipping empty file or file with no data: {file_path}")  
                
            else:   
                # 追加到合并的DataFrame中  
                merged_df = pd.concat([merged_df, df], ignore_index=True)  
        except Exception as e:
            print(e)
  
# 将合并后的DataFrame保存到指定的CSV文件中  
output_path = os.path.join(output_folder, output_filename)  
merged_df.to_csv(output_path, index=False)  
  
print(f'Merged CSV file saved to {output_path}')