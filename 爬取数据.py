import requests  
import pandas as pd  
from bs4 import BeautifulSoup  

cTypeInfo = [{ "id": 1, "name": "发动机/电动机", "value": "A", "zf": "z", "items": [{ "id": 9, "title": "异响" }, { "id": 11, "title": "电子油门延迟" }, { "id": 12, "title": "漏油" }, { "id": 13, "title": "机油乳化" }, { "id": 14, "title": "熄火" }, { "id": 18, "title": "爆震" }, { "id": 24, "title": "抖动" }, { "id": 34, "title": "故障灯亮" }, { "id": 35, "title": "怠速不稳" }, { "id": 37, "title": "漏防冻液" }, { "id": 38, "title": "噪音大" }, { "id": 44, "title": "无法启动" }, { "id": 45, "title": "正时链条及齿轮故障" }, { "id": 53, "title": "喷油嘴故障" }, { "id": 63, "title": "烧机油" }, { "id": 85, "title": "油耗高" }, { "id": 91, "title": "点火线圈故障" }, { "id": 114, "title": "排气故障" }, { "id": 128, "title": "连杆断裂" }, { "id": 129, "title": "曲轴故障" }, { "id": 136, "title": "缸体破损" }, { "id": 137, "title": "喷气嘴故障" }, { "id": 145, "title": "固定螺栓断裂" }, { "id": 160, "title": "无法提速" }, { "id": 163, "title": "功率不足" }, { "id": 173, "title": "火花塞故障" }, { "id": 174, "title": "油门故障" }, { "id": 178, "title": "漏气" }, { "id": 189, "title": "涡轮增压器故障" }, { "id": 191, "title": "冷却系统故障" }, { "id": 198, "title": "正时皮带断裂" }, { "id": 221, "title": "水泵故障" }, { "id": 222, "title": "皮带断裂" }, { "id": 235, "title": "发动机壳体破裂" }, { "id": 241, "title": "发动机下沉" }, { "id": 247, "title": "缸体生锈" }, { "id": 251, "title": "气门故障" }, { "id": 255, "title": "动力消失" }, { "id": 328, "title": "抱瓦" }, { "id": 329, "title": "拉缸" }, { "id": 336, "title": "缸内有异物" }, { "id": 339, "title": "机油增多" }, { "id": 341, "title": "电动机故障" }, { "id": 342, "title": "电动机异响" }, { "id": 346, "title": "电驱动控制器故障" }, { "id": 359, "title": "驱动电机故障" }, { "id": 360, "title": "混动模式转换故障" }, { "id": 368, "title": "增程器故障" }] }, { "id": 2, "name": "变速器", "value": "B", "zf": "z", "items": [{ "id": 19, "title": "顿挫" }, { "id": 20, "title": "无法换挡" }, { "id": 22, "title": "漏油" }, { "id": 27, "title": "跳挡" }, { "id": 33, "title": "异响" }, { "id": 69, "title": "拖挡" }, { "id": 77, "title": "机械部件故障" }, { "id": 84, "title": "滑阀箱故障" }, { "id": 95, "title": "抖动" }, { "id": 96, "title": "故障灯亮" }, { "id": 98, "title": "低温保护" }, { "id": 115, "title": "电脑板故障" }, { "id": 184, "title": "挡把总成故障" }, { "id": 208, "title": "共振" }, { "id": 246, "title": "脱挡" }, { "id": 332, "title": "加压泵故障" }, { "id": 334, "title": "无法加速" }] }, { "id": 3, "name": "离合器", "value": "C", "zf": "z", "items": [{ "id": 16, "title": "打滑" }, { "id": 17, "title": "烧毁" }, { "id": 65, "title": "异响" }, { "id": 87, "title": "抖动" }, { "id": 166, "title": "松动" }, { "id": 181, "title": "沉重" }, { "id": 207, "title": "漏油" }, { "id": 267, "title": "离合器失效" }] }, { "id": 4, "name": "转向系统", "value": "D", "zf": "z", "items": [{ "id": 57, "title": "失灵" }, { "id": 58, "title": "漏油" }, { "id": 59, "title": "异响" }, { "id": 80, "title": "抖动" }, { "id": 106, "title": "平衡杆故障" }, { "id": 112, "title": "助力泵故障" }, { "id": 123, "title": "卡滞" }, { "id": 154, "title": "方向盘不正" }, { "id": 156, "title": "打方向沉重" }, { "id": 265, "title": "转向机故障" }, { "id": 291, "title": "故障灯亮" }, { "id": 337, "title": "方向盘自由间隙过大" }, { "id": 356, "title": "管柱机构故障" }] }, { "id": 5, "name": "制动系统", "value": "E", "zf": "z", "items": [{ "id": 29, "title": "刹车失灵" }, { "id": 42, "title": "生锈" }, { "id": 43, "title": "异响" }, { "id": 47, "title": "异常磨损" }, { "id": 62, "title": "故障灯亮" }, { "id": 74, "title": "ABS故障" }, { "id": 99, "title": "漏油" }, { "id": 111, "title": "抖动" }, { "id": 159, "title": "手刹故障" }, { "id": 196, "title": "刹车泵故障" }, { "id": 231, "title": "刹车鼓爆裂" }, { "id": 239, "title": "刹车盘问题" }, { "id": 250, "title": "无法兰盘" }, { "id": 269, "title": "刹车偏软" }, { "id": 270, "title": "刹车片移位" }, { "id": 333, "title": "刹车变硬" }] }, { "id": 6, "name": "轮胎", "value": "F", "zf": "z", "items": [{ "id": 10, "title": "磨损" }, { "id": 39, "title": "鼓包" }, { "id": 41, "title": "胎压偏低" }, { "id": 92, "title": "凹陷" }, { "id": 100, "title": "开裂" }, { "id": 130, "title": "爆胎" }, { "id": 138, "title": "胎面变形" }, { "id": 142, "title": "胎面变色" }, { "id": 186, "title": "起皮" }, { "id": 257, "title": "其他问题" }] }, { "id": 7, "name": "前后桥及悬挂系统", "value": "G", "zf": "z", "items": [{ "id": 25, "title": "减震器漏油" }, { "id": 51, "title": "半轴渗油" }, { "id": 52, "title": "减震器异响" }, { "id": 56, "title": "底盘异响" }, { "id": 83, "title": "后桥塌陷" }, { "id": 86, "title": "四驱系统故障" }, { "id": 105, "title": "压力轴承故障" }, { "id": 117, "title": "跑偏" }, { "id": 124, "title": "差速器漏油" }, { "id": 125, "title": "车轮异响" }, { "id": 127, "title": "差速器异响" }, { "id": 132, "title": "车轮脱落" }, { "id": 158, "title": "前后桥异响" }, { "id": 161, "title": "球笼套漏油" }, { "id": 162, "title": "行驶中颠簸" }, { "id": 171, "title": "减震器过硬" }, { "id": 180, "title": "减震器生锈" }, { "id": 188, "title": "车轮松动" }, { "id": 200, "title": "轮毂螺丝断裂" }, { "id": 204, "title": "悬挂故障" }, { "id": 210, "title": "下摆臂故障" }, { "id": 225, "title": "四轮定位偏差" }, { "id": 227, "title": "半轴脱落" }, { "id": 230, "title": "前后桥断裂" }, { "id": 245, "title": "吃胎偏磨" }, { "id": 252, "title": "平衡杆异响" }, { "id": 261, "title": "后轴纵臂断裂隐患" }, { "id": 364, "title": "传动轴异响" }, { "id": 365, "title": "减震器断裂" }] }, { "id": 8, "name": "车身附件及电器", "value": "H", "zf": "z", "items": [{ "id": 15, "title": "车身异响" }, { "id": 21, "title": "导航问题" }, { "id": 23, "title": "无发动机防盗" }, { "id": 30, "title": "排气管锈蚀" }, { "id": 31, "title": "排气管异响" }, { "id": 40, "title": "车辆自燃" }, { "id": 48, "title": "密封条损坏" }, { "id": 49, "title": "车身模块故障" }, { "id": 50, "title": "油箱锁故障" }, { "id": 54, "title": "三元催化器故障" }, { "id": 55, "title": "气囊未弹开" }, { "id": 60, "title": "雨刮器故障" }, { "id": 64, "title": "车灯模块故障" }, { "id": 67, "title": "车窗升降故障" }, { "id": 68, "title": "后备厢故障" }, { "id": 71, "title": "灯组开关故障" }, { "id": 72, "title": "门窗异响" }, { "id": 73, "title": "发电机故障" }, { "id": 75, "title": "汽油箱漏油" }, { "id": 78, "title": "汽油泵故障" }, { "id": 79, "title": "车身生锈" }, { "id": 81, "title": "漆面起泡开裂" }, { "id": 82, "title": "车灯不亮" }, { "id": 88, "title": "车灯进水" }, { "id": 89, "title": "天窗异响" }, { "id": 90, "title": "天窗漏水" }, { "id": 93, "title": "中控台异响" }, { "id": 101, "title": "空调问题" }, { "id": 103, "title": "气囊故障" }, { "id": 104, "title": "行车电脑故障" }, { "id": 109, "title": "车身漏水" }, { "id": 110, "title": "电路故障" }, { "id": 113, "title": "玻璃开裂" }, { "id": 118, "title": "安全带故障" }, { "id": 119, "title": "车钥匙故障" }, { "id": 121, "title": "空调异味" }, { "id": 134, "title": "影音系统故障" }, { "id": 144, "title": "门窗漏风" }, { "id": 146, "title": "电瓶故障" }, { "id": 147, "title": "汽油箱异响" }, { "id": 149, "title": "车门故障" }, { "id": 150, "title": "排放系统故障" }, { "id": 151, "title": "喇叭故障" }, { "id": 152, "title": "中控台故障" }, { "id": 155, "title": "车载互联故障" }, { "id": 157, "title": "部件异常磨损" }, { "id": 164, "title": "车内异响" }, { "id": 168, "title": "部件开裂" }, { "id": 169, "title": "座椅故障" }, { "id": 170, "title": "行车安全辅助系统故障" }, { "id": 176, "title": "仪表台开裂" }, { "id": 179, "title": "车身装饰脱落" }, { "id": 185, "title": "车内异味" }, { "id": 192, "title": "天窗开关异常" }, { "id": 195, "title": "自动大灯延迟" }, { "id": 197, "title": "中控锁故障" }, { "id": 201, "title": "车身有色差" }, { "id": 202, "title": "仪表故障" }, { "id": 203, "title": "胎压监测故障" }, { "id": 209, "title": "车身不平整" }, { "id": 211, "title": "后视镜故障" }, { "id": 215, "title": "防侧滑功能未启动" }, { "id": 220, "title": "灯罩裂纹或变形" }, { "id": 233, "title": "车门把手故障" }, { "id": 234, "title": "传感器故障" }, { "id": 240, "title": "点火开关故障" }, { "id": 243, "title": "轮毂问题" }, { "id": 244, "title": "没有后防撞钢梁" }, { "id": 253, "title": "定速巡航故障" }, { "id": 263, "title": "发动机启停系统故障" }, { "id": 264, "title": "同款不同配置" }, { "id": 266, "title": "部件老化" }, { "id": 268, "title": "车身共振" }, { "id": 271, "title": "油箱有缺陷" }, { "id": 289, "title": "倒车雷达失灵" }, { "id": 335, "title": "中控台凹陷" }, { "id": 340, "title": "充电故障" }, { "id": 343, "title": "动力电池故障" }, { "id": 344, "title": "续航里程不准" }, { "id": 345, "title": "电池组冷却系统故障" }, { "id": 358, "title": "防盗系统故障" }, { "id": 361, "title": "电压转换器故障" }, { "id": 362, "title": "能量回收系统故障" }, { "id": 363, "title": "电源管理模块故障" }] }, { "id": 272, "name": "服务态度", "value": "I", "zf": "f", "items": [{ "id": 281, "title": "互相推诿" }, { "id": 282, "title": "故意拖延" }, { "id": 292, "title": "否认质量问题" }, { "id": 293, "title": "态度蛮横" }, { "id": 294, "title": "厂家不回复" }, { "id": 295, "title": "不解决问题" }, { "id": 297, "title": "不予索赔" }, { "id": 357, "title": "处理方案不合理" }, { "id": 369, "title": "隐瞒问题原因" }] }, { "id": 273, "name": "人员技术", "value": "J", "zf": "f", "items": [{ "id": 298, "title": "多次返修" }, { "id": 299, "title": "操作不规范" }, { "id": 300, "title": "修出新问题" }, { "id": 301, "title": "查不出原因" }, { "id": 302, "title": "无专用工具" }, { "id": 303, "title": "维修技术差" }, { "id": 304, "title": "粗心大意" }, { "id": 306, "title": "过度维修" }] }, { "id": 274, "name": "服务收费", "value": "K", "zf": "f", "items": [{ "id": 307, "title": "变相收费" }, { "id": 308, "title": "价格不透明" }, { "id": 309, "title": "定（订）金纠纷" }, { "id": 315, "title": "变更价格" }, { "id": 325, "title": "强制购买" }] }, { "id": 275, "name": "承诺不兑现", "value": "L", "zf": "f", "items": [{ "id": 310, "title": "不履行三包" }, { "id": 311, "title": "服务未按时交付" }, { "id": 312, "title": "不按约交车" }, { "id": 313, "title": "销售承诺不兑现" }, { "id": 314, "title": "服务承诺不兑现" }] }, { "id": 276, "name": "销售欺诈", "value": "M", "zf": "f", "items": [{ "id": 279, "title": "与宣传不符" }, { "id": 280, "title": "低配当高配卖" }, { "id": 283, "title": "出售库存车" }, { "id": 284, "title": "出售问题车" }, { "id": 355, "title": "隐瞒相关信息" }] }, { "id": 277, "name": "配件争议", "value": "N", "zf": "f", "items": [{ "id": 316, "title": "使用旧件" }, { "id": 317, "title": "配件质量差" }, { "id": 318, "title": "无零配件" }, { "id": 319, "title": "使用非原厂件" }, { "id": 320, "title": "未按时到货" }, { "id": 321, "title": "未更换定损配件" }] }, { "id": 278, "name": "服务流程不完善", "value": "O", "zf": "f", "items": [{ "id": 296, "title": "活动不通知" }, { "id": 305, "title": "未经同意维修" }, { "id": 324, "title": "无维修工单" }, { "id": 326, "title": "服务网点少" }, { "id": 347, "title": "充电桩少" }, { "id": 348, "title": "系统升级问题" }, { "id": 353, "title": "手续不齐" }, { "id": 354, "title": "原车配套不全" }] }, { "id": 351, "name": "其他服务问题", "value": "P", "zf": "f", "items": [{ "id": 327, "title": "其他" }] }, { "id": 352, "name": "其他", "value": "Q", "zf": "q", "items": [{ "id": 290, "title": "厂家不召回" }, { "id": 322, "title": "疑似设计缺陷" }, { "id": 323, "title": "召回方案不合理" }, { "id": 349, "title": "使用说明书不准确" }, { "id": 350, "title": "疑似减配" }, { "id": 366, "title": "政策变动" }, { "id": 367, "title": "价格变动" }] }]

def getDesc(keystr):
    keys = keystr.split(',')
    descStr = []
    for key in keys:
              subject = [obj for obj in  cTypeInfo if obj["value"] == key[0]] 
              desc = ''
              if not subject:
                    desc = key 
                    return keystr       
              else:
                    desc = [obj for obj in  subject[0]["items"] if obj["id"] == int(key[1:])] 
                    descStr .append(str(subject[0]["name"])+":"+ desc[0]["title"]) 
    return descStr
def download_tables_from_urls(url_table_classes, output_file):  
    """  
    从多个指定网页下载表格，并将所有表格数据合并保存到一个CSV文件中。  
  
    参数:  
    url_table_classes (list of dict): 包含URL和对应表格class名的字典列表，例如：  
        [  
            {'url': 'http://example.com/page1', 'table_class': 'table1'},  
            {'url': 'http://example.com/page2', 'table_class': 'table2'},  
            # ...  
        ]  
    output_file (str): 保存合并表格数据的CSV文件名。  
    """  
    all_tables_data = []  
  
    for item in url_table_classes:  
        url = item['url']  
        table_class = item['table_class']  
     
        # 发送GET请求获取网页内容  
        response = requests.get(url)  
        response.raise_for_status()  # 检查请求是否成功  
  
        # 使用BeautifulSoup解析网页内容  
        soup = BeautifulSoup(response.text, 'html.parser')  
  
        # 找到指定class的表格  
        tables = soup.find_all('table', {'class': table_class})  
        if not tables:  
            print(f"在URL {url} 中未找到class为'{table_class}'的表格。")  
            continue  
        table = tables[0]  
  
        # 将表格转换为pandas DataFrame并添加到列表中  
        df_list = []  
        for row in table.find_all('tr'):  
            cells = row.find_all(['th', 'td'])  
            if cells:  
                df_list.append([cell.get_text(strip=True) for cell in cells])  
        df = pd.DataFrame(df_list) 
        df[5] = df[5].apply(lambda x: getDesc(str(x)))   
        print(df[5])
         
        
        all_tables_data.append(df)  
  
    # 将所有表格数据合并到一个DataFrame中  
    if not all_tables_data:  
        raise ValueError("未找到任何表格数据。")  
    merged_df = pd.concat(all_tables_data, ignore_index=True)  
  
    # 保存合并后的DataFrame到CSV文件  
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')  
    print(f"所有表格数据已合并并保存到 {output_file}")  
  
# 使用示例：  
url_table_classes = [  
    

    # 添加更多URL和对应的表格class名...  
]
# range(页数)
for i in range(17):
    #print("https://www.12365auto.com/zlts/525-0-0-0-0-0_0-0-0-0-0-0-0-"+str(i)+".shtml")
    url_table_classes.append({'url': 'https://www.12365auto.com/zlts/532-0-0-0-0-0_0-0-0-0-0-0-0-'+str(i)+'.shtml', 'table_class':'ar_c ar_c1'})

output_file = "理想汽车质检投诉.csv"  # 输出的CSV文件名  

  
download_tables_from_urls(url_table_classes, output_file)


