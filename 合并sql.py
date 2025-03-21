import os
import glob
import chardet
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']
def merge_sql_files(directory, output_file):
    # 打开输出文件，准备写入
    with open(output_file, 'w', encoding=detect_file_encoding(output_file)) as outfile:
        # 使用glob模块递归查找所有.sql文件
        for sql_file in glob.glob(os.path.join(directory, '**', '*.sql'), recursive=True):
              # 检测文件编码
            encoding = detect_file_encoding(sql_file)
            with open(sql_file, 'r', encoding=encoding) as infile:
                # 将每个SQL文件的内容写入输出文件
                outfile.write(infile.read())
                # 可选：在每个文件内容之间添加分隔符
                outfile.write('\n\n-- End of file: {} --\n\n'.format(sql_file))

# 使用示例
directory = 'F://xeq项目//xEQ综合版版本发布//2.0.3//脚本//宏源恒利//2.0.0//xir_eq'  # 替换为你的文件夹路径
output_file = 'F://xeq项目//xEQ综合版版本发布//2.0.3//脚本//综合版//2.0.0_eq.sql'  # 合并后的输出文件名
merge_sql_files(directory, output_file)

print(f"All SQL files in {directory} have been merged into {output_file}")