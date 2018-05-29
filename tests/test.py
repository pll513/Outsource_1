# coding=utf-8
import os
import json
#
# f = file('new_intro', 'r')
# results = []
# count = 0
# sight = {
#     'imgs': [],
#     'name': "无",
#     'impression': "无",
#     "introduction": "无",
#     "arrive_leave": "无",
#     "type": "无",
#     'season': "无",
#     'advice_time': "无",
#     'ticket': "无",
#     "open_time": "无"
# }
# for readline in f.readlines():
#     if readline.strip() == '#':
#         results.append(sight)
#         sight = {
#             'imgs': [],
#             'name': "无",
#             'impression': "无",
#             "introduction": "无",
#             "arrive_leave": "无",
#             "type": "无",
#             'season': "无",
#             'advice_time': "无",
#             'ticket': "无",
#             "open_time": "无"
#         }
#         count = 0
#     else:
#         if count == 0:
#             sight['name'] = readline.strip()
#             count = 0.5
#             continue
#         if readline.strip() == '大家印象':
#             count = 1
#             continue
#         if count == 1:
#             sight['impression'] = readline.strip()
#             count = 1.5
#         if readline.strip() == sight['name']:
#             count = 2
#             continue
#         if count == 2:
#             sight['introduction'] = readline.strip()
#             count = 2.5
#         if readline.find('到达与离开') != -1:
#             sight['arrive_leave'] = readline[18:].strip()
#         if readline.find('景点类型') != -1:
#             sight['type'] = readline[15:].strip()
#         if readline.find('最佳季节') != -1:
#             sight['season'] = readline[15:].strip()
#         if readline.find('建议游玩') != -1:
#             sight['advice_time'] = readline[15:].strip()
#         if readline.find('门票') != -1:
#             sight['ticket'] = readline[9:].strip()
#         if readline.find('开放时间') != -1:
#             sight['open_time'] = readline[15:].strip()
#
# sights = []
# photos = []
#
# for result in results:
#     sight = {
#         "name": result['name'],
#         "des": {
#             "impression": result['impression'],
#             "introduction": result['introduction'],
#             "arrive_leave": result['arrive_leave'],
#             "type": result['type'],
#             "season": result['season'],
#             "advice_time": result['advice_time'],
#             "ticket": result['ticket'],
#             "open_time": result['open_time']
#         },
#         "photo": os.listdir("../../../../photos/" + result['name'])
#     }
#     sights.append(sight)
command = "curl -i -X GET [2001:da8:270:2018:f816:3eff:fe25:2463]:8080/api/v1.0/count"
#command = "curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTUyMjA3OTE1NCwiaWF0IjoxNTIyMDc4NTU0fQ.eyJpZCI6IjE4NDI4MzU5NTY5In0.VD453q0ZYORHhdj095ZoP4l_DesJ1SV_RvHJl_YVg4g:unused -i -X GET http://www.erhii.com/api/v1.0/find"
#
# for sight in sights:
#     command = """curl -u 18428359569:224930 -i -X POST -H "Content-Type: application/json" -d '%s' http://www.erhii.com/api/v1.0/sight""" % json.dumps(sight, ensure_ascii=False)
#     print command

location_num = {
    "location_num": [
        {"name": "诺日朗瀑布", "sight_location": [103.913843, 33.169227]},
        {"name": "五彩池", "sight_location": [103.939441, 33.052034]},
        {"name": "五花海", "sight_location": [103.887532, 33.164984]},
        {"name": "树正群海", "sight_location": [103.904356, 33.204395]},
        {"name": "犀牛海", "sight_location": [103.899479, 33.194024]},
        {"name": "日则沟", "sight_location": [103.915974, 33.167468]},
        {"name": "珍珠滩", "sight_location": [103.893739, 33.171808]},
        {"name": "神仙池", "sight_location": [103.780543, 33.312335]},
        {"name": "则查洼沟", "sight_location": [103.918243, 33.164697]},
        {"name": "树正寨", "sight_location": [103.902578, 33.204003]},
        {"name": "中查沟", "sight_location": [103.824643, 33.301861]},
        {"name": "箭竹海", "sight_location": [103.880902, 33.138717]},
        {"name": "芦苇海", "sight_location": [103.917335, 33.222641]},
        {"name": "熊猫海", "sight_location": [103.882833, 33.153832]},
        {"name": "镜海", "sight_location": [103.907353, 33.165706]},
        {"name": "长海", "sight_location": [103.889331, 33.176126]},
        {"name": "天鹅海", "sight_location": [103.871677, 33.091894]},
        {"name": "火花海", "sight_location": [103.908074, 33.209732]},
        {"name": "盆景滩", "sight_location": [103.919445, 33.22838]},
        {"name": "藏谜", "sight_location": [103.885439,33.293066]},
        {"name": "老虎海", "sight_location": [103.901571, 33.198526]},
        {"name": "树正瀑布", "sight_location": [103.901797, 33.199881]},
        {"name": "熊猫海瀑布", "sight_location": [103.882977, 33.154714]},
        {"name": "羌寨", "sight_location": [103.468219, 31.562553]},
        {"name": "卧龙海", "sight_location": [103.907089, 33.206953]},
        {"name": "金铃海", "sight_location": [103.887246, 33.163974]},
        {"name": "宝镜岩", "sight_location": [103.93887, 33.263173]},
        {"name": "上季节海", "sight_location": [103.936191, 33.059493]},
        {"name": "黄龙古寺", "sight_location": [103.836729, 32.725987]},
        {"name": "季节海", "sight_location": [103.926967, 33.126111]},
        {"name": "荷叶寨", "sight_location": [103.921249, 33.231178]},
        {"name": "孔雀河道", "sight_location": [103.889732, 33.166253]},
        {"name": "二道海", "sight_location": [103.509627, 32.665756]},
        {"name": "甘海子", "sight_location": [103.875651, 33.289385]},
        {"name": "争艳池", "sight_location": [103.840011, 32.744748]},
        {"name": "丹云峡", "sight_location": [104.070557, 32.695522]},
        {"name": "扎如沟", "sight_location": [103.989786, 33.224843]},
        {"name": "扎如寺", "sight_location": [103.938033,33.262503]},
        {"name": "剑岩", "sight_location": [103.865702, 33.078302]},
        {"name": "勿角大熊猫自然保护区", "sight_location": [104.234422, 33.042695]},
        {"name": "宝镜崖", "sight_location": [103.931511, 33.261784]},
        {"name": "扎如马道", "sight_location": [103.989785, 33.224842]},
        {"name": "黑角桥", "sight_location": [103.912896, 33.218025]},
        {"name": "边边街", "sight_location": [103.930628, 33.279655]},
        {"name": "九座塔", "sight_location": [103.824643, 33.301861]},
        {"name": "红星岩", "sight_location": [103.785427, 32.861727]},
        {"name": "九寨沟喜来登国际大剧院", "sight_location": [103.937521, 33.284064]},
        {"name": "九寨高原红演出中心", "sight_location": [103.871131, 33.290902]},
        {"name": "红军长征纪念碑", "sight_location": [103.626066, 32.775485]},
        {"name": "扎依扎嘎神山", "sight_location": [103.973212, 33.236721]},
        {"name": "鹰爪洞", "sight_location": [103.874308, 33.09447]},
        {"name": "四沟", "sight_location": [103.925447, 32.826525]},
        {"name": "草海", "sight_location": [103.867553, 33.085282]},
        {"name": "红池", "sight_location": [104.033537, 33.262132]},
        {"name": "九寨千古情景区", "sight_location": [103.865324, 33.302063]}]}

#command = """curl -u 18101039331:123456 -i -X POST -H "Content-Type: application/json" -d '%s' http://www.erhii.com/api/v1.0/location_num""" % json.dumps(location_num, ensure_ascii=False)
# article = {
#     "name": "九寨沟藏族文化",
#     "type": "特色藏风",
#     "content": ["title:藏族的历史",
#                 "藏族主要聚居在我国的高原地区，那里幅员辽阔，雪峰连绵，山峦起伏，风光神奇而壮美。传说中藏族最初是由“神猴”和“岩魔女” 结合而产生的。另据汉文史料记载，藏族源于我国古代游牧民族西羌人，他们与当地土著民族融合而发展成今天的藏族。",
#                 "photo:/static/image/article/article1.png",
#                 "title:藏式建筑",
#                 """九寨沟因沟内有九个藏族村寨而得名。原始古朴的村寨散落在绿树环抱的群山之中，显得更加古老、宁静。一个民族的建筑文化总是和它的生存环境、生命繁衍息息相关，显示着人类文化学和地域文化学的色彩。九寨沟，平均海拔在 2500 米 左右，属于寒温带地区，所以冬无严寒，夏无酷暑，在这里的传统的建筑大都为木结构。
# 按藏族的传统习惯，藏寨木楼一般为三层，底层关牲畜(也有另外设计土房的)及储藏土豆、萝卜等根类蔬菜。第二层为家人和神灵菩萨共同居住用，重要物品也存放在第二层。第三层为储藏粮食、草料及竹、木质农具等。随着生活的改善，人畜共居的建筑已被淘汰。代之而起的是一楼一底的建筑，卫生环境也大大改善了。
# """,
#                 "photo:/static/image/article/article2.png",
#                 "photo:/static/image/article/article3.png",
#                 "photo:/static/image/article/article4.png",
#                 "photo:/static/image/article/article5.png"],
#     "photos": ["/static/image/article/article1.png", "/static/image/article/article2.png"]
# }


#command = """curl -i -X POST -H "Content-Type: application/json" -d '{"phone":"18101039331","name":"cpz", "password":"123456"}' http://www.erhii.com/api/v1.0/users"""
print(os.system(command))