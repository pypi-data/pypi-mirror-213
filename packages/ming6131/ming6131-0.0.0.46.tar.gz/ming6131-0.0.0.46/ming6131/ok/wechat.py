import requests
import datetime
import time
import re
import json
from xml.dom.minidom import parseString
import xml.dom.minidom
from flask import Flask, request


class obj:
    def __init__(
            self,
            port1=8089,
            port2=8055,
    ):
        self.url = f'http://127.0.0.1:{port2}/DaenWxHook/client/'

        # 获取所有群组    {群ID:群名,...}, {群名:群ID,...}
        self.wxid2nick_group, self.nick2wxid_group = self.fetch_group(True)
        # 获取所有好友    {wxid:(昵称,微信号),...}
        self.wxid2nick = self.fetch_firends(True)
        self.port1 = port1

    def run(self,
            wxfunc  # 函数，处理接收到的数据
            ):
        app = Flask(__name__)

        @app.route('/wechat/', methods=['get', 'post'])
        def wechat():
            data = request.stream.read()
            data = data.decode('utf-8')
            data = json.loads(data, strict=False)
            #data = json.loads(request.data.decode('u8'))
            # date = datetime.datetime.fromtimestamp(int(data["timestamp"]) // 1000)

            rs_data = self.receive_msg(data)
            wxfunc(rs_data)
            # 需要任意返回点东西
            return ""
            # return jsonify({"code": 200, "msg": "ok", "timestamp": str(int(time.time()))})

        app.run(port=self.port1)

    # 接收分析事件
    def receive_msg(self, data):
        '''
            用途：通过data['type']判断是属于什么事件 D0001 注入成功;D0002 登录成功;D0003 收到消息;D0004 转账事件;D0005 撤回事件;D0006 好友请求
                根据不同的事件，返回不同的参数
            返回：dic 所有事件的所有参数，只有真实的事件才有真实的数据，其它的事件参数都为None
                返回的参数都是后面接口要用到的
        '''

        data0 = data.get("data")
        if not data0:
            return data

        # 获取公共参数-时间戳
        timestamp = data.get('timestamp')
        timestamp = timestamp if timestamp else data0.get('timeStamp')
        if not timestamp:
            return data

        # 时间戳转格式
        tm = float(timestamp) / 1000
        tm = time.localtime(tm)
        tm = time.strftime("%H:%M:%S", tm)
        # 获取公共变量 wxid
        wxid = data['wxid']

        # 获取事件类型
        type = data['type']  # 原事件类型，待细分

        data = data0

        # 定义细分事件类型
        '''
            D01 等待登录
            D02 登录成功
        '''
        retn_data = False
        if type == 'D0001':  # 注入成功
            retn_data = self.get_d0001(data, tm)
        elif type == 'D0002':  # 登录成功
            retn_data = self.get_d0002(data, tm)
            # 获取所有群组    {群ID:群名,...}, {群名:群ID,...}
            self.wxid2nick_group, self.nick2wxid_group = self.fetch_group(True)
            # 获取所有好友    {wxid:(昵称,微信号),...}
            self.wxid2nick = self.fetch_firends(True)

        elif type == 'D0003':  # 收到消息
            retn_data = self.get_d0003(data, tm)
        elif type == 'D0004':  # 转账
            retn_data = self.get_d0004(data, tm)
        elif type == 'D0005':  # 撤回
            retn_data = self.get_d0005(data, tm)

        elif type == 'D0006':  # 好友请求
            retn_data = self.get_d0006(data, tm)
        else:
            return False

        if not retn_data:
            return None
        retn_data["wxid"] = wxid
        retn_data["timestamp"] = timestamp
        return retn_data

    # 获取群聊列表
    def fetch_group(self, flush=False):
        '''
        获取群聊列表
        :param flush:
        :return:
        '''
        payload = {"type": "Q0006", "data": {"type": "2" if flush else "1"}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        wxid2nick = {}  # {群ID:群名,...}
        nick2wxid = {}  # {群名:群ID,...}
        for row in data["result"]:
            wxid2nick[row["wxid"]] = row["nick"]
            nick2wxid[row["nick"]] = row["wxid"]
        return wxid2nick, nick2wxid

    # 获取好友列表
    def fetch_firends(self, flush=False):
        payload = {"type": "Q0005", "data": {"type": "2" if flush else "1"}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        wxid2nick = {}
        for row in data["result"]:
            if not row["wxNum"]:
                row["wxNum"] = row["wxid"]
            wxid2nick[row["wxid"]] = (row["nick"], row["wxNum"])
        return wxid2nick  # {wxid:(昵称,微信号),...}

    # 获取所有群成员
    def fetch_group_member(self, wxid):
        payload = {"type": "Q0008", "data": {"wxid": wxid}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        return data["result"]

    # 查询对象信息
    def fetch_obj_info(self, wxid):
        payload = {"type": "Q0004", "data": {"wxid": wxid}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        return data["result"]

    # 发送文本消息
    def send_mag(self, wxid, msg):
        if not msg:
            msg = "无内容"
        msgs = []
        imsg = msg.split("\n")
        msg = []
        for itm in imsg:
            itm = f"{itm}\n"
            itm = itm.split("\r")
            for itm0 in itm:
                msg.append(f"{itm0}\r")

        itxt = ""
        for item in msg:
            ict = len(item.encode('gbk'))
            count = len(itxt.encode('gbk'))
            if count + ict > 2000:
                msgs.append(itxt)
                itxt = ""
                if ict > 2000:
                    imsg = ''
                    imsg0 = ''
                    for char in item:
                        imsg0 += char
                        if len(imsg0.encode('gbk')) > 2046:
                            msgs.append(imsg)
                            imsg = ''
                            imsg0 = ''
                        imsg += char
                    itxt = imsg
            else:
                itxt = f"{itxt}{item}"
        if itxt:
            msgs.append(itxt)
        for msg in msgs:
            msg = msg.strip()
            if not msg:
                continue
            payload = {"type": "Q0001", "data": {"wxid": wxid, "msg": msg}}
            res = requests.post(self.url, json=payload)

            time.sleep(0.5)
        data = res.json()
        return data["result"]

    def getXmlTxt(self, xmlCode, tagNames, attrs=None):
        '''

        :param xmlCode: xml代码
        :param tagNames: 标签名,可以是字符串，也可以是列表
        :param attrs: []标签的子项，列表
        :return: 返回所有标签或者子项的内容字典
        '''
        vDic = {}
        try:
            # 打开xml文档
            xmlItem = xml.dom.minidom.parseString(xmlCode)
            # 得到文档元素对象
            xmlItem = xmlItem.documentElement
        except:
            return vDic

        if type(tagNames) == str:
            tagNames = [tagNames]

        for tagName in tagNames:
            v = False
            try:
                tagItem = xmlItem.getElementsByTagName(tagName)[0]  # 按标签名获取对象
                if not attrs:
                    v = tagItem.childNodes[0].data  # 获取标签的内容数据
            except:
                pass
            if v:
                vDic[tagName] = v

        if not attrs:
            return vDic

        for attr in attrs:
            try:
                v = tagItem.getAttribute(attr)
            except:
                v = False
            if v:
                vDic[attr] = v
        return vDic

    def decXml(self, dicData, xmlCode):
        xmlType = dicData.get('xmlType', None)
        dicData['内容'] = None

        # 这是游戏 石头剪刀布 掷骰子
        if xmlType == 1:
            rs = self.getXmlTxt(xmlCode, "gameext", ["type", "content", ])

            gameType = int(rs.get("type", 0))
            gameContent = int(rs.get("content", 3))

            dicData['gameType'] = gameType
            dicData['gameContent'] = gameContent

            if gameType == 1:  # 这是石头剪刀布
                itemDic = {1: "剪刀", 2: "石头", 3: "布", }
                dicData['内容'] = f"游戏[石头剪刀布：{itemDic.get(gameContent, None)}]"
            elif gameType == 2:  # 这是 掷骰子
                dicData['内容'] = f"游戏[掷骰子：{gameContent - 3}点]"
        # 这是聊天记录
        elif xmlType == 19:
            rs = self.getXmlTxt(xmlCode, ["title", "des", ])

            title = rs.get("title", None)
            des = rs.get("des", None)

            dicData['title'] = title
            dicData['des'] = des

            dicData['内容'] = f"{title}[{des}]"
        # 这是发起位置共享
        elif xmlType == 17:
            dicData['内容'] = "发起位置共享"
        # 这是表情图片
        elif xmlType == 2:
            rs = self.getXmlTxt(xmlCode, "emoji", ["cdnurl", ])
            rs = rs.get("cdnurl", None)

            if "&" in rs:
                rs = f"<非官方表情包>{rs.split('&')[0]}"
            dicData['内容'] = rs
        # 这是分享链接
        elif xmlType == 5:
            rs = self.getXmlTxt(xmlCode, ["title", "des", "url"])

            title = rs.get("title", None)
            des = rs.get("des", None)
            url = rs.get("url", None)

            dicData["title"] = title
            dicData["des"] = des
            dicData["url"] = url

            dicData['内容'] = f"<{title}>[{des}][{url}]"

        # 这是收藏-笔记
        elif xmlType == 24:
            rs = self.getXmlTxt(xmlCode, "des")

            des = rs.get("des", None)

            dicData["des"] = des

            dicData['内容'] = f"{des}"

        # 未知数据
        else:
            dicData['内容'] = "未知数据"

        return dicData

    def getXmlTxt(self, xmlCode, tagNames, attrs=None):
        '''

        :param xmlCode: xml代码
        :param tagNames: 标签名,可以是字符串，也可以是列表
        :param attrs: []标签的子项，列表
        :return: 返回所有标签或者子项的内容字典
        '''
        vDic = {}
        try:
            # 打开xml文档
            xmlItem = xml.dom.minidom.parseString(xmlCode)
            # 得到文档元素对象
            xmlItem = xmlItem.documentElement
        except:
            return vDic

        if type(tagNames) == str:
            tagNames = [tagNames]

        for tagName in tagNames:
            v = False
            try:
                tagItem = xmlItem.getElementsByTagName(tagName)[0]  # 按标签名获取对象
                if not attrs:
                    v = tagItem.childNodes[0].data  # 获取标签的内容数据
            except:
                pass
            if v:
                vDic[tagName] = v

        if not attrs:
            return vDic

        for attr in attrs:
            try:
                v = tagItem.getAttribute(attr)
            except:
                v = False
            if v:
                vDic[attr] = v
        return vDic

    def getMsg(self, dicData):
        msgType = dicData['msgType']
        msg = dicData["msg"]
        try:
            xmlCode = re.findall(r'<msg>[\d\D]*?</msg>', msg)[0]
        except:
            xmlCode = dicData["msg"]

        # 获取msg中xml中type元素的值，如果没有，则取默认值 99
        rs = self.getXmlTxt(xmlCode, "type")
        if not rs:
            rs = self.getXmlTxt(xmlCode, "emoji", ["type", ])
        xmlType = rs.get("type", 99)

        dicData["xmlType"] = int(xmlType)

        dicData["内容"] = dicData["msg"]
        if msgType == 47:  # 这是动态表情
            dicData = self.decXml(dicData, xmlCode)  # 解析xml

        elif msgType == 34:  # 语音消息
            dicData["内容"] = "语音消息"
        elif msgType == 3:  # 这是图片
            dicData["内容"] = "图片"
        elif msgType == 43:  # 这是视频
            dicData["内容"] = '▶ 视频'
        # 这是分享链接或附件
        elif msgType == 49:
            # 这是文件
            if "file=" in dicData["msg"]:
                dicData["xmlType"] = 96
                msg = dicData["msg"]
                msg = re.findall(r"\[file=(.*?)\]", msg)
                if msg:
                    msg = msg[0]
                dicData["内容"] = msg
            # 其它
            else:
                dicData = self.decXml(dicData, xmlCode)
        # 这是名片
        elif msgType == 42:
            rs = self.getXmlTxt(xmlCode, "msg",
                                ["username", 'nickname', "antispamticket", 'province', 'city', 'openimdesc'])
            v3 = rs.get("username", None)
            nickname = rs.get("nickname", None)  # 昵称
            v4 = rs.get("antispamticket", None)
            province = rs.get("province", None)  # 省份
            city = rs.get("city", None)  # 城市
            openimdesc = rs.get("openimdesc", None)  # 企业微信-企业账号

            dicData['v3'] = v3
            dicData['nickname'] = nickname
            dicData['v4'] = v4
            dicData['province'] = province
            dicData['city'] = city
            dicData['openimdesc'] = openimdesc

            if 'gh_' in v3:
                dicData['xmlType'] = 95
                dicData["内容"] = f"公众号[{nickname}]"
            elif '@openim' in v3:
                dicData['xmlType'] = 94
                dicData["内容"] = f"企业微信号[{openimdesc}[{nickname}]]"
            else:
                dicData['xmlType'] = 93
                dicData["内容"] = f"个人号[{nickname}]]"


        # 这是地理位置
        elif msgType == 48:
            rs = self.getXmlTxt(xmlCode, "location", ["poiname", "label", "x", "y"])
            x = rs["x"]
            y = rs["y"]
            label = rs["label"]
            poiname = rs["poiname"]
            dicData[x] = x
            dicData[y] = y
            dicData[label] = label

            dicData["内容"] = f"x,{x} y,{y} {poiname}[{label}]"
        elif msgType == 10000:

            if '位置共享' in dicData['msg']:
                dicData["xmlType"] = 98
            if '收到红包' in dicData['msg']:
                dicData["xmlType"] = 97
        return dicData

    # D0001 事件分析————注入成功
    def get_d0001(self, data, tm):
        dic = {
            "type": "D01",
            "info": f"{tm} <D01>检测到微信启动，等待登录...",
            "data": {
                "port": data["port"],
                "pid": data["pid"]
            }
        }
        return dic

    # D0002 事件分析————登录成功
    def get_d0002(self, data, tm):
        # 获取所有群组    {群ID:群名,...}, {群名:群ID,...}
        self.wxid2nick_group, self.nick2wxid_group = self.fetch_group(True)
        # 获取所有好友    {wxid:(昵称,微信号),...}
        self.wxid2nick = self.fetch_firends(True)
        self.wxNum = data['wxNum']
        self.nick = data['nick']
        self.wxid = data['wxid']
        dic = {
            "type": "D02",
            "info": f"{tm} <D02>登录成功，微信账号[{self.wxNum}]上线，昵称[{self.nick}]",
            "data": {
                'wxid': data['wxid'],  # wxid
                'wxNum': data['wxNum'],  # 微信号
                'nick': data['nick'],  # 微信昵称
                'device': data['device'],  # 登录设备
                'phone': data['phone'],  # 手机号
                'avatarUrl': data['avatarUrl'],  # 头像地址
                'country': data['country'],  # 国家
                'province': data['province'],  # 省
                'city': data['city'],  # 城市
                'email': data['email'],  # 邮箱
                'qq': data['qq']  # QQ
            }
        }
        return dic

    # D0003 事件分析————收到消息
    def get_d0003(self, data, tm):
        fromType = data["fromType"]  # 来源类型：1|私聊 2|群聊 3|公众号
        msgType = data[
            "msgType"]  # 消息类型：1|文本 3|图片 34|语音 42|名片 43|视频 47|动态表情 48|地理位置 49|分享链接或附件 2001|红包 2002|小程序 2003|群邀请 10000|系统消息
        msgSource = data["msgSource"]  # 消息来源：0|别人发送 1|自己手机发送
        fromWxid = data["fromWxid"]  # fromType=1时为好友wxid，fromType=2时为群wxid，fromType=3时公众号wxid
        finalFromWxid = data["finalFromWxid"]  # 仅fromType=2时有效，为群内发言人wxid
        atWxidList = data["atWxidList"]  # 仅fromType=2，且msgSource=0时有效，为消息中艾特人wxid列表
        silence = data["silence"]  # 仅fromType=2时有效，0
        membercount = data["membercount"]  # 仅fromType=2时有效，群成员数量
        signature = data["signature"]  # 消息签名
        msg = data["msg"]  # 消息内容
        msgBase64 = data["msgBase64"]  # 消息内容的Base64编码

        dic = {
            "type": "",
            "data": {
                "fromType": fromType,
                "msgType": msgType,
                "msgSource": msgSource,
                "fromWxid": fromWxid,
                "finalFromWxid": finalFromWxid,
                "atWxidList": atWxidList,
                "silence": silence,
                "membercount": membercount,
                "signature": signature,
                "msg": msg,
                "msgBase64": msgBase64,
            }
        }
        if fromType == 2:
            nick = self.wxid2nick_group[fromWxid]
        elif fromType == 1:
            if fromWxid == "newsapp":
                nick = "腾讯新闻"
            else:
                nick = self.wxid2nick[fromWxid][1]

        dic来源 = {1: f"好友[{nick}]", 2: f"群[{nick}]->成员[{finalFromWxid}]", 3: f'公众号[{fromWxid}]'}
        dic类型 = {  # 最后两位是99 ，说明没有获取到细分类型，统一设置成默认值
            199: '文本', 399: '图片', 3499: '语音', 4299: '名片', 4399: '视频', 4799: '动态表情', 4899: '地理位置', 4999: '分享链接或附件',
            200199: '红包', 200299: '小程序', 200399: '群邀请', 1000099: '系统消息',
            # 以下是获取到msg消息体中xml中type元素值的细分消息类型
            # 以下，最后两位是99的，说明没有type，但消息类型与原类型不符，所以另外取了一个编号
            4701: "游戏", 4702: "动态表情",
            4917: '位置共享', 4919: "聊天记录", 4905: "分享链接", 4924: "收藏笔记", 4996: "文件",
            100098: "位置共享已经结束", 1000097: "红包",
        }  # 最后一行是程序需要，另外添加的编号，根据原类型细分，前几位数是原类型，后2位数是细分类型

        来源 = dic来源[fromType] if msgSource == 0 else "自己手机发送"
        dicMsg = self.getMsg(dic["data"])
        dic["data"] = dicMsg

        # 统一所有类型都加上xmlType
        index = dicMsg['msgType']
        消息类型 = dic类型[index * 100 + dicMsg['xmlType']]

        dic["type"] = f"D03{msgSource}{fromType}{msgType}{dicMsg['msgType']}"
        dic["info"] = f'{tm} <{dic["type"]}>收到 @{来源}的 {消息类型}：[{dicMsg["内容"]}]'
        return dic

    # D0004 事件分析————转账
    def get_d0004(self, data, tm):
        fromWxid = data['fromWxid']  # 对方wxid
        msgSource = data['msgSource']  # 1|收到转账 2|对方接收转账 3|发出转账 4|自己接收转账 5|对方退还 6|自己退还
        transType = data['transType']  # 1|即时到账 2|延时到账
        money = data['money']  # 金额，单位元
        memo = data['memo']  # 转账备注
        transferid = data['transferid']  # 转账ID
        invalidtime = data['invalidtime']  # 10位时间戳
        ls1 = ["收到转账", "对方接收转账", "发出转账", "自己接收转账", "对方退还", "自己退还"]
        ls2 = ["即时到账", "延时到账"]
        nick = self.wxid2nick[fromWxid][0]
        wxnum = self.wxid2nick[fromWxid][1]
        type = f"D04{msgSource}{transType}"
        info = f'{tm} <{type}>{ls1[msgSource - 1]}|{ls2[transType - 1]}->{nick}[{wxnum}]：{money}元，id:{transferid} 备注：{memo}'
        dic = {
            "type": type,
            "info": info,
            "data": {
                "fromWxid": fromWxid,
                "msgSource": msgSource,
                "transType": transType,
                "money": money,
                "memo": memo,
                "transferid": transferid,
                "invalidtime": invalidtime,
            }
        }
        return dic

    # D0005 事件分析————撤回
    def get_d0005(self, data, tm):
        pass
        '''
        dic = {
            "type": "D00",
            "timestamp": data["timestamp"],
            "data": {

            }
        }
        infoShow(f"{tm} 撤回事件")
        return dic

                wxid = data['wxid']

                fromWxid = data['data']['fromWxid']  # fromType=1时为好友wxid，fromType=2时为群wxid
                finalFromWxid = data['data']['finalFromWxid']  # 仅fromType=2时有效，为群内撤回消息人的wxid

                fromType = data['data']['fromType']            # 来源类型：1|好友 2|群聊
                if fromType == 1:
                    消息来源 = f"好友：[{fromWxid}]"
                else:
                    消息来源 = f"群：[{fromWxid}]->成员[{finalFromWxid}]"

                dic = {1:'别人', 2:'自己使用手机', 3:'自己使用电脑'}
                msgSource = data['data']['msgSource']          # 消息来源：1|别人撤回 2|自己使用手机撤回 3|自己使用电脑撤回




                msg = data['data']['msg']                      # 撤回的消息内容
                if msgSource != 1:
                    消息来源 = dic[msgSource]

                if '<msg><emoji' in msg:
                    msg = '[表情图片]'
                elif '<img aeskey=' in msg:
                    msg = '[图片]'
                elif '<videomsg aeskey=' in msg:
                    msg = '[▶ 视频]'
                elif '<msg><voicemsg' in msg:
                    msg = '[语音]'
                elif '<location x="' in msg:  # 这是地理位置
                    msg0 = re.findall(r'label="(.*?)"',msg)
                    if msg0:
                        msg0 = f"[{msg0[0]}]"
                    else:
                        msg0 = f'[{msg[:20]}]'
                    msg = f" 地理位置{msg0}"

                infoShow(f'{tm} {消息来源} 撤回了：{msg}')
        '''

    # D0006 事件分析————好友请求
    def get_d0006(self, data, tm):
        pass
        '''
        dic = {
            "type": "D00",
            "timestamp": data["timestamp"],
            "data": {

            }
        }
        infoShow(f"{tm} 好友请求")
        return dic
        '''

    # 待完善
    def Xpost(self, url, type):
        '''
        获取微信列表（X0000）           POST微信状态检测（Q0000）   POST发送文本消息（Q0001）    POST修改下载图片（Q0002）    POST获取个人信息（Q0003）
        POST查询对象信息（Q0004）       POST获取好友列表（Q0005）   POST获取群聊列表（Q0006）    POST获取公众号列表（Q0007）    POST获取群成员列表（Q0008）
        POST发送聊天记录（Q0009）       POST发送图片（Q0010）      POST发送本地文件（Q0011）    POST发送分享链接（Q0012）    POST发送小程序（Q0013）
        POST发送音乐分享（Q0014）       POST发送XML（Q0015）      POST确认收款（Q0016）       POST同意好友请求（Q0017）    POST添加好友_通过v3（Q0018）
        POST添加好友_通过wxid（Q0019）  POST查询陌生人信息（Q0020） POST邀请进群（Q0021）       POST删除好友（Q0022）    POST修改对象备注（Q0023）
        POST修改群聊名称（Q0024）       POST发送名片（Q0025）

        '''

        payload = json.dumps({
            "type": type,
            "data": {}
        })
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    # 待完善
    def Qpost(self, wxid, type, msg=None, uWxid=None, picType=None, title=None, dataList=None, path=None, content=None,
              jumpUrl=None, app=None, jumpPath=None,
              gh=None, name=None, author=None, musicUrl=None, imageUrl=None, xml=None, transferid=None, scene=None,
              v3=None, v4=None, pq=None, objWxid=None, remark=None, nick=None):
        url = f"http://127.0.0.1:7777/DaenWxHook/httpapi/?wxid={wxid}"

        payload = json.dumps({
            "type": type,  # POST 类型
            "data": {
                "type": picType,  # 类型：       修改下载图片-     “23:30-23:30”为全天下载，“00:01-23:59”为全天不下载
                #             添加好友_通过V3-  (1=新朋友，2=互删朋友（2:此时来源将固定死为3）)
                #             邀请进群-         1=直接拉，2=发送邀请链接）
                "wxid": uWxid,  # 好友Id    邀请进群-群组ID|删除好友|修改对象备注-支持好友wxid、群ID
                #           修改群聊名称|发送名片-要发给谁
                "msg": msg,  # 内容：       发送消息
                "title": title,  # 标题：        发送聊天记录|发送分享链接|发送小程序
                "dataList": dataList,  # []内容列表：   发送聊天记录
                "path": path,  # 路径：        发送图片|发送本地文件|发送分享链接-缩略图|发送小程序-缩略图
                "content": content,  # 副标题：      发送分享链接|发送小程序|添加好友-请求内容|添加好友_通过wxid
                "jumpUrl": jumpUrl,  # 跳转链接：     发送分享链接
                "app": app,  # 跳转APP：    发送分享链接-跳转APP(可空，例如QQ浏览器为：wx64f9cf5b17af074d)
                "jumpPath": jumpPath,  # 跳转地址      发送小程序-点击跳转地址，例如饿了么首页为：pages/index/index.html
                "gh": gh,  # 小程序地址     发送小程序-例如饿了么为：gh_6506303a12bb
                "name": name,  # 歌名            发送音乐分享
                "author": author,  # 作者            发送音乐分享
                "musicUrl": musicUrl,  # 网络歌曲直链    发送音乐分享
                "imageUrl": imageUrl,  # 网络图片直链    发送音乐分享
                "xml": xml,  # xml           发送xml
                "transferid": transferid,  # 转账ID          同意收款
                "scene": scene,
                # 来源            同意好友请求|添加好友|添加好友_通过wxid     (1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫)
                "v3": v3,  # v3            同意好友请求|添加好友_通过V3
                "v4": v4,  # v4            同意好友请求
                "pq": pq,  # 手机号或者QQ
                "objWxid": objWxid,  # 好友wxid       邀请进群
                "remark": remark,  # 备注：          修改对象备注-支持emoji、微信表情
                "nick": nick,  # 群名称 支持emoji、微信表情
                #               修改群聊名称

            }
        })

        if type == 'Q0025':  # 发送名片
            # 待完善
            payload = rf'{{\r\n    \"type\": \"{type}\",\r\n    \"data\": {{\r\n        \"wxid\": \"21257217892@chatroom\",\r\n        \"xml\": \"<?xml version=\\\"1.0\\\"?>\r\n<msg bigheadimgurl=\\\"http://wx.qlogo.cn/mmhead/ver_1/qYAC6GgTX4cAqTmzB5Ep8nzeB9RjufAMT02q7PLLEURuLbHlyjibria2LMLBsvqIiaZQmeZPicbRSMQY28zKQGxHTXHz5tg5RQe1UCJkGPVbXSI/0\\\" smallheadimgurl=\\\"http://wx.qlogo.cn/mmhead/ver_1/qYAC6GgTX4cAqTmzB5Ep8nzeB9RjufAMT02q7PLLEURuLbHlyjibria2LMLBsvqIiaZQmeZPicbRSMQY28zKQGxHTXHz5tg5RQe1UCJkGPVbXSI/132\\\" username=\\\"wxid_jah3fozezery22\\\" nickname=\\\"〆无所不能。\\\" fullpy=\\\"wusuobuneng\\\" shortpy=\\\"\\\" alias=\\\"PQAPQB\\\" imagestatus=\\\"3\\\" scene=\\\"17\\\" province=\\\"云南\\\" city=\\\"中国大陆\\\" sign=\\\"\\\" sex=\\\"2\\\" certflag=\\\"0\\\" certinfo=\\\"\\\" brandIconUrl=\\\"\\\" brandHomeUrl=\\\"\\\" brandSubscriptConfigUrl=\\\"\\\" brandFlags=\\\"0\\\" regionCode=\\\"CN_Yunnan_Kunming\\\" biznamecardinfo=\\\"\\\" />\"\r\n    }}\r\n}}'
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


'''
调用示例

def func(data):
    type = data["type"]
    timestamp = data["timestamp"]
    wxid = data["wxid"]
    info = data["info"]
    data = data["data"]
    # 文本消息
    if type == "D030111":

if __name__ == '__main__':
    wx = wechat(func)

'''
