import oracledb
import json
# 若未安装 oracledb 执行 命令 pip install oracledb
# Oracle数据库连接信息（建议使用环境变量或配置文件来管理这些信息）
db_user = 'xir_eq'
db_password = 'xpar'
db_dsn = '172.19.4.28:1521/hlht'
cursor = None
connection = None
#设置一下 本机Oracle客户端路径
oracledb.init_oracle_client(lib_dir="C:\\devsoft\\oracle\\client\\instantclient_11_2")

try:
    # 连接到数据库
    connection = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)
 
    # 创建一个游标对象
    cursor = connection.cursor()
 
    # 查询包含JSON数据的表
    query = "SELECT id, s_data FROM xir_eq.OPTION_STRATEGY"
    cursor.execute(query)
 
    # 遍历查询结果并处理JSON数据
    for row in cursor:
        record_id = row[0]
        # 使用 getlob() 读取 CLOB 数据（如果可用），否则直接获取字节串并解码
        # 注意：getlob() 可能不是 python-oracledb 的标准方法，具体取决于版本
        # 如果 getlob() 不可用，row[1] 将是一个 bytes 对象，您可以直接使用它（跳过解码步骤）
        # 这里我们假设 getlob() 不可用，直接处理 bytes
        json_data_bytes = row[1]  # 这应该是 bytes 类型
        #json_data = json_data_bytes.decode('utf-8')  # 解码为字符串（如果 getlob() 不可用，则跳过此步）
        
        # 将JSON字符串转换为Python字典
        clobstr = json_data_bytes.read()
        clobstr.encode('utf-8')
        data_dict = json.loads(clobstr)
        
        # 检查并修改JSON数据（根据您的逻辑）
        if 'calcPriceParam' in data_dict[0] and 'valueDate' not in data_dict[0]['calcPriceParam']:
            if 'Issue_Date' in data_dict:
                data_dict[0]['calcPriceParam']['valueDate'] = data_dict[0]['vm']['Issue_Date']
                # 将修改后的Python字典转换回JSON字符串，并编码为字节串
                new_clob_data = json.dumps(data_dict).encode('utf-8')
                            
                            # 更新数据库中的记录
                            # 注意：这里我们使用绑定变量，并将 JSON 数据作为字节串传递

                            # 要更新的表名和字段
                table_name = 'xir_eq.OPTION_STRATEGY'
                clob_column = 's_data'
                condition = 'id'  # 用于唯一标识要更新的行的列
                            
                            # 要更新的行的 ID 和新的 CLOB 数据
                            # 1. 查找要更新的行的现有 CLOB 定位器（如果需要的话，通常不需要这一步来写入新数据）
                            #    但在这里，我们直接插入新数据，所以不需要定位器。
                            #    不过，为了演示如何使用定位器，我们可以先查询它（如果它已经存在的话）。
                            
                            # 2. 使用 PL/SQL 块和 DBMS_LOB.WRITE 过程更新 CLOB 字段
                            #    注意：这里我们假设 CLOB 字段是空的或者可以覆盖。如果需要追加数据，请使用 DBMS_LOB.APPEND。
                            # 使用DBMS_LOB包更新CLOB字段
                sql = f"""
                                          DECLARE
                                          lobLocator CLOB;
                                          BEGIN
                                          SELECT {clob_column} INTO lobLocator FROM {table_name} WHERE {condition} = {record_id} FOR UPDATE;
                                          DBMS_LOB.WRITE(lobLocator, LENGTH(:new_data), 1, :new_data);
                                          END;
                                          """
                cursor.execute(sql, [new_clob_data])
                print(f"处理了数据 编号为:{record_id}") 
        else: 
              print(record_id,'含有计算日期',data_dict[0]['calcPriceParam']['valueDate'])
 
        
        
 
    # 提交事务
    connection.commit()
 
except oracledb.Error as e:
    # 捕获数据库错误并回滚事务
    print(f"Database error occurred: {e}")
    connection.rollback()
except json.JSONDecodeError as e:
    print(f"JSON 解码错误: {e} 编号为:{record_id}") 
finally:
    # 确保游标和连接被关闭
    if cursor:
        cursor.close()
    if connection:
        connection.close()