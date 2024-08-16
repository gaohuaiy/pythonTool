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
    table_name_match = re.search(r'create table\s+(\w+)', create_statement, re.IGNORECASE)  
    if not table_name_match:  
        raise ValueError("无法从建表语句中提取表名")  
      
    table_name = table_name_match.group(1).upper()  # Oracle中的表名通常是大写的，所以这里仍然转换为大写  
      
    # 生成包含条件创建表逻辑的SQL脚本（注意：这里的SQL脚本实际上是一个PL/SQL匿名块）  
    sql_template = """  
DECLARE  
    v_count NUMBER;  
BEGIN  
    SELECT COUNT(*)  
    INTO v_count  
    FROM all_tables  
    WHERE table_name = '{}' ;  -- 假设我们在当前用户的模式下工作  
  
    IF v_count > 0 THEN  
        DBMS_OUTPUT.PUT_LINE('表 {} 已存在，跳过创建。');  
    ELSE  
        EXECUTE IMMEDIATE '{}';  
    END IF;  
END;  
/  
"""  
    repeatable_sql = sql_template.format(table_name, table_name, create_statement.strip())  
      
    # 将SQL脚本写入文件  
    with open(file_name, 'a', encoding='GBK') as file:  
        file.write(repeatable_sql)  
  
# 示例  
create_table_sql = """  

create table TTRS_TRADE_XIRPUSH_RECORD
(
  id                          NUMBER(20) not null,
  sysordid                    NUMBER(17) default 0,
  trs_bnd_id                  NUMBER(20) not null,
  trs_trade_id                VARCHAR2(50) not null,
  trader_id                   VARCHAR2(50) not null,
  trader                      VARCHAR2(50),
  party_id                    NUMBER(20) not null,
  party_name                  VARCHAR2(500),
  trdtype                     VARCHAR2(10) not null,
  orddate                     CHAR(10) not null,
  i_code                      VARCHAR2(100) not null,
  i_name                      VARCHAR2(100),
  a_type                      VARCHAR2(20) not null,
  m_type                      VARCHAR2(20) not null,
  b_par_value                 NUMBER(20,3),
  ordamount                   NUMBER(38,4) not null,
  ordprice                    NUMBER(20,12) not null,
  margin_used                 NUMBER(38,4) not null,
  push_type                   INTEGER not null,
  push_status                 INTEGER not null,
  push_result_id              INTEGER not null,
  push_result_msg             VARCHAR2(128) default '',
  push_time                   TIMESTAMP(6) not null,
  push_param_text             CLOB,
  create_time                 TIMESTAMP(6) not null,
  creator                     VARCHAR2(32) not null,
  update_time                 TIMESTAMP(6),
  updater                     VARCHAR2(32),
  interest_base               INTEGER,
  coupon_type                 INTEGER,
  irc_code                    VARCHAR2(100),
  spread                      INTEGER,
  calendar                    VARCHAR2(12),
  daycounter                  VARCHAR2(32),
  interest_calculation_method VARCHAR2(1),
  interest_type               VARCHAR2(1),
  start_date                  VARCHAR2(10),
  end_date                    VARCHAR2(10),
  reset_frequency             VARCHAR2(5),
  pay_frequency               VARCHAR2(10),
  margin_guarantee_ratio      NUMBER(20,12),
  market_mode                 INTEGER,
  cash_direction              INTEGER,
  transfer_date               VARCHAR2(10),
  interest_flag               INTEGER,
  margin_rate                 NUMBER(12,8),
  margin_daycounter           VARCHAR2(32),
  mark_p_class                VARCHAR2(32),
  market_instrument_name      VARCHAR2(32),
  append_ratio                NUMBER(12,6),
  keep_ratio                  NUMBER(12,6),
  close_ratio                 NUMBER(12,6),
  draw_ratio                  NUMBER(12,6),
  after_draw_ratio            NUMBER(12,6),
  conversion_ratio            NUMBER(12,6),
  inst_rate                   NUMBER(12,8),
  merge_id                    NUMBER(20)
)
tablespace XIR_EQ
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Add comments to the table 
comment on table TTRS_TRADE_XIRPUSH_RECORD
  is '衡泰推送记录表';
-- Add comments to the columns 
comment on column TTRS_TRADE_XIRPUSH_RECORD.sysordid
  is '交易编号';
comment on column TTRS_TRADE_XIRPUSH_RECORD.trs_bnd_id
  is '收益互换现券交易id';
comment on column TTRS_TRADE_XIRPUSH_RECORD.trs_trade_id
  is '合约编号';
comment on column TTRS_TRADE_XIRPUSH_RECORD.trader_id
  is '交易员ID';
comment on column TTRS_TRADE_XIRPUSH_RECORD.trader
  is '交易员';
comment on column TTRS_TRADE_XIRPUSH_RECORD.party_id
  is '交易对手ID';
comment on column TTRS_TRADE_XIRPUSH_RECORD.party_name
  is '交易对手名称';
comment on column TTRS_TRADE_XIRPUSH_RECORD.trdtype
  is '交易方向';
comment on column TTRS_TRADE_XIRPUSH_RECORD.orddate
  is '交易日期';
comment on column TTRS_TRADE_XIRPUSH_RECORD.i_code
  is '债券代码';
comment on column TTRS_TRADE_XIRPUSH_RECORD.i_name
  is '债券名称';
comment on column TTRS_TRADE_XIRPUSH_RECORD.a_type
  is '债券类型';
comment on column TTRS_TRADE_XIRPUSH_RECORD.m_type
  is '市场类型';
comment on column TTRS_TRADE_XIRPUSH_RECORD.b_par_value
  is '交易面额';
comment on column TTRS_TRADE_XIRPUSH_RECORD.ordamount
  is '结算金额';
comment on column TTRS_TRADE_XIRPUSH_RECORD.ordprice
  is '交易价格，全价不含费';
comment on column TTRS_TRADE_XIRPUSH_RECORD.margin_used
  is '占用保证金';
comment on column TTRS_TRADE_XIRPUSH_RECORD.push_type
  is '推送类型，1-互换交易；2-资产交易；3-保证金交易；';
comment on column TTRS_TRADE_XIRPUSH_RECORD.push_status
  is '推送状态，0-未推送；1-已推送；';
comment on column TTRS_TRADE_XIRPUSH_RECORD.push_result_id
  is '推送结果id，0-成功；else_失败，存储xIR的结果';
comment on column TTRS_TRADE_XIRPUSH_RECORD.push_result_msg
  is '推送结果详情';
comment on column TTRS_TRADE_XIRPUSH_RECORD.push_time
  is '推送时间';
comment on column TTRS_TRADE_XIRPUSH_RECORD.push_param_text
  is '推送报文';
comment on column TTRS_TRADE_XIRPUSH_RECORD.create_time
  is '创建时间';
comment on column TTRS_TRADE_XIRPUSH_RECORD.creator
  is '创建人';
comment on column TTRS_TRADE_XIRPUSH_RECORD.update_time
  is '修改时间';
comment on column TTRS_TRADE_XIRPUSH_RECORD.updater
  is '修改人';
comment on column TTRS_TRADE_XIRPUSH_RECORD.interest_base
  is '计息基数 1-名义本金 2-资产成本';
comment on column TTRS_TRADE_XIRPUSH_RECORD.coupon_type
  is '息票类型 1-固定利率 2-浮动利率';
comment on column TTRS_TRADE_XIRPUSH_RECORD.irc_code
  is '利率基准曲线代码';
comment on column TTRS_TRADE_XIRPUSH_RECORD.spread
  is '利差';
comment on column TTRS_TRADE_XIRPUSH_RECORD.calendar
  is '付息日历';
comment on column TTRS_TRADE_XIRPUSH_RECORD.daycounter
  is '计息基准';
comment on column TTRS_TRADE_XIRPUSH_RECORD.interest_calculation_method
  is '计息方式0-算头不算尾  2-算头且算尾';
comment on column TTRS_TRADE_XIRPUSH_RECORD.interest_type
  is '利息计算方式 0-单利  2-复利';
comment on column TTRS_TRADE_XIRPUSH_RECORD.start_date
  is '计息开始日';
comment on column TTRS_TRADE_XIRPUSH_RECORD.end_date
  is '计息结束日';
comment on column TTRS_TRADE_XIRPUSH_RECORD.reset_frequency
  is '重置频率 1D\1W\1M\W\1Y';
comment on column TTRS_TRADE_XIRPUSH_RECORD.pay_frequency
  is '支付时机 Deferred到期 Immediate触发';
comment on column TTRS_TRADE_XIRPUSH_RECORD.margin_guarantee_ratio
  is '期初保证金比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.market_mode
  is '盯市类型 0-对手模式 1-合约模式';
comment on column TTRS_TRADE_XIRPUSH_RECORD.cash_direction
  is '资金方向 1-划入 -1-划出';
comment on column TTRS_TRADE_XIRPUSH_RECORD.transfer_date
  is '划拨日期';
comment on column TTRS_TRADE_XIRPUSH_RECORD.interest_flag
  is '是否计息标志';
comment on column TTRS_TRADE_XIRPUSH_RECORD.margin_rate
  is '保证金利率';
comment on column TTRS_TRADE_XIRPUSH_RECORD.margin_daycounter
  is '保证金计息基准';
comment on column TTRS_TRADE_XIRPUSH_RECORD.mark_p_class
  is '盯市参数挂钩品种';
comment on column TTRS_TRADE_XIRPUSH_RECORD.market_instrument_name
  is '盯市参数挂钩标的';
comment on column TTRS_TRADE_XIRPUSH_RECORD.append_ratio
  is '追保比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.keep_ratio
  is '维持比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.close_ratio
  is '平仓比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.draw_ratio
  is '提取比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.after_draw_ratio
  is '提取后比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.conversion_ratio
  is '折算比例';
comment on column TTRS_TRADE_XIRPUSH_RECORD.inst_rate
  is '标的利率';
comment on column TTRS_TRADE_XIRPUSH_RECORD.merge_id
  is '合并后的TRS交易ID';
-- Create/Recreate indexes 
create index INDEX_TRS_RECORD_BND_ID on TTRS_TRADE_XIRPUSH_RECORD (TRS_BND_ID)
  tablespace XIR_EQ
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate primary, unique and foreign key constraints 
alter table TTRS_TRADE_XIRPUSH_RECORD
  add constraint TTRS_TRADE_XIRPUSH_RECORD_PK primary key (ID)
  using index 
  tablespace XIR_EQ
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );



"""  
  
# 调用函数并写入文件  
oracle_create_table_to_file(create_table_sql,"F:\\xeq项目\\宏源恒利EQ版本发布\\2.0.0\脚本\\xir_eq\\403_EQ_trs_db_init.sql")  
  
# print(f"SQL脚本已写入到 {file_name}")