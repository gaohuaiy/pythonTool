from xiaoaitts import XiaoAi

# 输入小米账户名，密码
client = XiaoAi('18829878412', 'ghy409424')
# 朗读文本
#client.say('你好，我是小爱')
# 获取所有在线设备
#online_devices = client.get_device()
# 获取单个设备，未找到时返回 null
#room_device = client.get_device('小爱音箱Play')
# 获取歌单列表
#my_playlist = client.get_my_playlist()
# 获取歌单内的歌曲列表
#song_list = client.get_my_playlist('1054845530396148925')
#print(my_playlist)
#client.play()
client.next()