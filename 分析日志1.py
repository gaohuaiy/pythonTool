import os  
import json  
import re  
import csv  
from concurrent.futures import ThreadPoolExecutor  
  
# 假设JSON数据以这种形式出现在日志中（每行一个完整的JSON对象）  
json_pattern = re.compile(r'^{.*}$')  # 只匹配完整的JSON对象（以{}开头和结尾）  
  
# 设置日志文件夹路径和CSV文件输出路径  
log_folder = 'C:\\Users\\02445\\Desktop\\0513\\0513'  
csv_output_file = 'output.csv'  
  
# 处理单个日志文件的函数  
def process_log_file(file_path, csv_queue):  
    with open(file_path, 'r', encoding='utf-8') as f:  
        for line in f:  
            if json_pattern.match(line):  
                try:  
                    json_obj = json.loads(line)  
                    # 假设我们将整个JSON对象作为字符串写入CSV（或者你可以选择特定的字段）  
                    csv_queue.append(json.dumps(json_obj))  
                except json.JSONDecodeError:  
                    # 处理JSON解析错误（可选：记录日志、跳过等）  
                    pass  
  
# 将数据写入CSV的函数（应该在单独的线程中运行）  
def write_to_csv(csv_queue, csv_file):  
    fieldnames = ['LogEntry']  # 假设我们只写入整个日志条目  
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  
        writer.writeheader()  
        while True:  
            item = csv_queue.get()  
            if item is None:  # 队列中的结束信号  
                break  
            writer.writerow({'LogEntry': item})  
        csv_queue.task_done()  # 告诉队列处理已完成  
  
# 主函数  
def main():  
    # 创建一个线程安全的队列来存储CSV数据  
    from queue import Queue  
    csv_queue = Queue()  
  
    # 启动CSV写入线程  
    with ThreadPoolExecutor(max_workers=1) as executor:  
        csv_writing_future = executor.submit(write_to_csv, csv_queue, csv_output_file)  
  
        # 遍历日志文件夹中的所有文件并处理它们  
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:  
            futures = []  
            for root, dirs, files in os.walk(log_folder):  
                for file in files:  
                    if file.endswith('.log'):  
                        print(file)
                        file_path = os.path.join(root, file)  
                        futures.append(executor.submit(process_log_file, file_path, csv_queue))  
  
            # 等待所有文件处理完成  
            for future in concurrent.futures.as_completed(futures):  
                pass  # 如果有需要，可以在这里处理future.exception()或future.result()  
  
        # 当所有文件都处理完后，向队列中添加一个结束信号  
        csv_queue.put(None)  
  
    # 等待CSV写入完成  
    csv_writing_future.result()  
  
if __name__ == '__main__':  
    main()