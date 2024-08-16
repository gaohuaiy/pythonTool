def oracle_rename_table_columns(table_name, columns_to_rename, db_connection, file_name='rename_columns.sql'):  
    """  
    生成SQL脚本，用于在Oracle表中重命名多个列（支持可重复执行）。  
      
    注意：这个函数假设你有一个名为'db_connection'的数据库连接对象，用于执行检查列存在性的查询。  
    但在实际应用中，你可能需要在执行SQL脚本之前或之中使用此连接。  
  
    参数:  
    - table_name: 表名（大写）  
    - columns_to_rename: 一个包含(旧列名, 新列名)元组的列表  
    - db_connection: 数据库连接对象（用于潜在的列存在性检查，但在此示例中未直接使用）  
    - file_name: 输出文件的名称，默认为'rename_columns.sql'  
    """  
    # 假设的列存在性检查函数（在实际应用中，你需要实现这个函数）  
    def check_column_exists(conn, table, column):  
        # 这里应该是执行数据库查询的代码，但为了简化，我们直接返回True（假设列存在）  
        # 在实际应用中，你应该替换为真实的查询逻辑  
        return True  # 假设列存在，但你需要实现真实的检查  
  
    # 构建包含所有RENAME COLUMN语句的SQL脚本  
    sql_script = ""  
    for old_column_name, new_column_name in columns_to_rename:  
        # 在这里，你应该使用db_connection来检查old_column_name是否存在  
        # 但为了简化，我们直接跳过这个检查（在实际应用中不要这样做！）  
        # if check_column_exists(db_connection, table_name, old_column_name):  
            # 生成PL/SQL匿名块  
        plsql_block = f"""  
DECLARE  
    v_count NUMBER;  
BEGIN  
    SELECT COUNT(*)  
    INTO v_count  
    FROM user_tab_columns  
    WHERE table_name = '{table_name}'  
    AND column_name = '{old_column_name}';  
  
    IF v_count = 0 THEN  

        DBMS_OUTPUT.PUT_LINE('列 {old_column_name} 不存在于 {table_name} 中。');  
    ELSE  
        EXECUTE IMMEDIATE 'ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};'; 
        
    END IF;  
END;  
/  
"""  
       
        sql_script += plsql_block + "\n"  
  
    # 注意：这里没有包含真实的列存在性检查，因为它依赖于外部数据库连接和查询  
  
    # 将SQL脚本写入文件  
    with open(file_name, 'w', encoding='ANSI') as file:  
        file.write(sql_script)  
  
    print(f"SQL脚本已写入到 {file_name}")  
  
# 注意：在实际应用中，你需要提供一个有效的数据库连接对象给这个函数  
# 例如，使用cx_Oracle库来创建和管理Oracle数据库连接  
  
# 示例（不包括实际的数据库连接）  
table_name = 'XIR_EQ.TSYS_TASK_LOG'  
columns_to_rename = [  
    ('ID', 'LOG_ID'),  
    # 假设OLD_COLUMN2已经被重命名或不存在，但在这个示例中我们仍然尝试添加它  
    # ('OLD_COLUMN2', 'NEW_COLUMN2'),  
]  
  
# 假设的数据库连接对象（在实际应用中需要替换为真实的连接）  
db_connection = None  # 这里应该是你的数据库连接对象  
  
# 调用函数并生成脚本（注意：这里不会执行列存在性检查！）  
oracle_rename_table_columns(table_name, columns_to_rename, db_connection)  
  
# 警告：上面的代码没有执行真正的列存在性检查！  
# 在实际部署之前，请确保你有一个有效的方法来检查列名是否仍然需要更改。