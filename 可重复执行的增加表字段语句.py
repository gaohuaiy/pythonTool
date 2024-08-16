def oracle_alter_table_add_columns(table_name, columns_defs, file_name='alter_table_add_columns.sql'):  
    """  
    生成一个或多个PL/SQL匿名块，用于向Oracle表中添加不存在的列。  
      
    参数:  
    - table_name: 表名（大写）  
    - columns_defs: 一个列表，包含要添加的列的定义。每个定义可以是一个(列名, 数据类型, [其他属性])的元组或字典。  
    - file_name: 输出文件的名称，默认为'alter_table_add_columns.sql'  
    """  
    # 构建PL/SQL脚本  
    plsql_script = ""  
    for column_def in columns_defs:  
        # 假设column_def是一个(列名, 数据类型, ...)的元组或包含'name'和'type'键的字典  
        if isinstance(column_def, tuple):  
            column_name, column_type = column_def[:2]  
            additional_attributes = column_def[2:] if len(column_def) > 2 else []  
        elif isinstance(column_def, dict):  
            column_name = column_def['name']  
            column_type = column_def['type']  
            additional_attributes = [f"{k} {v}" for k, v in column_def.items() if k not in ['name', 'type']]  
        else:  
            raise ValueError("字段定义必须是元组或字典")  
  
        # 构建ALTER TABLE语句的剩余部分  
        alter_statement = f"ALTER TABLE {table_name} ADD ({column_name} {column_type}"  
        if additional_attributes:  
            alter_statement += " " + ", ".join(additional_attributes)  
        alter_statement += ")"  
  
        # 生成PL/SQL匿名块  
        plsql_block = f"""  
DECLARE  
    v_count NUMBER;  
BEGIN  
    SELECT COUNT(*)  
    INTO v_count  
    FROM user_tab_columns  
    WHERE table_name = '{table_name}'  
    AND column_name = '{column_name}';  
  
    IF v_count = 0 THEN  
        EXECUTE IMMEDIATE '{alter_statement}';  
        DBMS_OUTPUT.PUT_LINE('列 {column_name} 已添加到表 {table_name} 中。');  
    ELSE  
        DBMS_OUTPUT.PUT_LINE('列 {column_name} 已存在于表 {table_name} 中，无需添加。');  
    END IF;  
END;  
/  
"""  
        plsql_script += plsql_block  
  
    # 将PL/SQL脚本写入文件  
    with open(file_name, 'w', encoding='ANSI') as file:  
        file.write(plsql_script)  
  
    print(f"PL/SQL脚本已写入到 {file_name}")  
  
# 示例  
table_name = 'XIR_EQ.TSYS_USER'  
columns_defs = [  
    ('TIME_ZONE', 'VARCHAR2(8)'),  
      # 使用字典添加默认值  
]  
# LOG_ID


 
# 调用函数并生成脚本  
oracle_alter_table_add_columns(table_name, columns_defs,"404_EQ_TSYS_USER_DDL.sql")