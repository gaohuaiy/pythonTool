def oracle_create_table_to_file(create_statement, file_name='repeatable_create_table.sql'):  
    """  
    将Oracle建表语句转换为可重复执行的SQL脚本，并将结果写入到文件中。  
    忽略表名的大小写。  
      
    参数:  
    - create_statement: 原始Oracle建表语句的字符串。  
    - file_name: 输出文件的名称，默认为'repeatable_create_table.sql'。  
    """  
    # 正则表达式匹配表名，忽略大小写  
    import re  
    parts = create_statement.split("-- Add comments to ", 1) 
    first_part, second_part = parts 
    table_name_match = re.search(r'create table\s+(\w+)', first_part, re.IGNORECASE)  
    if not table_name_match:  
        raise ValueError("无法从建表语句中提取表名")  
      
    table_name = table_name_match.group(1).upper()  # Oracle中的表名通常是大写的，所以这里仍然转换为大写  
      
    # 生成包含条件创建表逻辑的SQL脚本（注意：这里的SQL脚本实际上是一个PL/SQL匿名块）  
    sql_template = """  
call tryaddtable( '{}' ,'{}')
{}
"""  
    repeatable_sql = sql_template.format(table_name, first_part.strip(),second_part)  
      
    # 将SQL脚本写入文件  
    with open(file_name, 'a', encoding='ANSI') as file:  
        file.write(repeatable_sql)  
  
# 示例  
create_table_sql = """  



"""  
  
# 调用函数并写入文件  
oracle_create_table_to_file(create_table_sql,"F:\\xeq项目\\宏源恒利EQ版本发布\\2.0.0\脚本\\xir_eq\\405_EQ_TCALC_MONITOR_DDL.sql")  
  
# print(f"SQL脚本已写入到 {file_name}")