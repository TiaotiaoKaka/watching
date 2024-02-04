import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

PROGRESS_CACHE = {}
ROOM_CACHE = {}


class ChatConsumer(AsyncWebsocketConsumer):
    async def announce_msg(self, token, msg):
        count = len(ROOM_CACHE.get(token, []))
        # 通知房间内的所有人
        ip = self.scope['client'][0]
        progress = {'count': count, 'chatmsg': ip + '：' + msg}

        for consumer in ROOM_CACHE[token]:
            # 不需要通知自己
            if consumer == self:
                continue
            await consumer.send(json.dumps(progress))

    async def update_count(self, token, announce_self=True):
        """
        更新房间内人数
        :param announce_self:
        :param token:
        :return:
        """
        count = len(ROOM_CACHE.get(token, []))
        # 通知房间内的所有人
        progress = {'count': count}
        for consumer in ROOM_CACHE[token]:
            # 不需要通知自己
            if not announce_self and consumer == self:
                continue
            await consumer.send(json.dumps(progress))

    async def setprogress(self, token, json_data, announce_self=False):
        """
        通知更新进度
        :param json_data:
        :param announce_self:
        :param token:
        :return:
        """
        progress = json.loads(json_data)
        PROGRESS_CACHE[token] = progress
        progress['count'] = len(ROOM_CACHE.get(token, [0]))
        # 通知房间内的所有人
        for consumer in ROOM_CACHE[token]:
            # 不需要通知自己
            if not announce_self and consumer == self: continue
            await consumer.send(json.dumps(progress))

    async def websocket_connect(self, message):
        """
        当有客户端向后端发送websocket连接请求时，自动触发该函数
        :param message:
        :return:
        """
        # 服务器允许客户端创建连接
        await self.accept()

    async def websocket_receive(self, message):
        """
        浏览器基于websocket向后端发送数据，自动触发接受消息，并且处理信息
        :param message:
        :return:
        """
        # 输出消息
        if 'setroom--' in message['text']:
            token = message['text'].split('--')[1]
            room = ROOM_CACHE.get(token)
            # 如果房间不存在，就创建房间
            if not room:
                ROOM_CACHE[token] = []

            ROOM_CACHE[token].append(self)
            # 初始化进度情况
            await self.send(json.dumps(PROGRESS_CACHE.get(token, {'count': 1})))
            # 通知房间内的所有人
            await self.update_count(token)
            await self.announce_msg(token, '进入房间')

        elif 'setprogress--' in message['text']:
            token = message['text'].split('--')[1]
            json_data = message['text'].split('--')[2]

            await self.setprogress(token, json_data)  # 同步进度
            await self.update_count(token)  # 计算人数

        elif 'getprogress--' in message['text']:
            token = message['text'].split('--')[1]
            progress = PROGRESS_CACHE.get(token, None)
            if not progress:
                progress = {'count': 0}
            else:
                progress['count'] = len(ROOM_CACHE.get(token, [0]))
            await self.send(json.dumps(progress))
        elif 'chatmsg' in message['text']:
            token = message['text'].split('--')[1]
            msg = message['text'].split('--')[2]
            await self.announce_msg(token, msg)

    async def websocket_disconnect(self, message):
        """
        客户端与服务端断开连接时，自动触发该函数
        :param message:
        :return:
        """
        print('断开连接')
        # 删除房间中的用户
        for token in ROOM_CACHE:
            if self in ROOM_CACHE[token]:
                ROOM_CACHE[token].remove(self)
                break
        # 如果房间内没有用户了，就删除房间， 否则通知所有人现在有多少人
        for token in ROOM_CACHE:
            if len(ROOM_CACHE[token]) == 0:
                del ROOM_CACHE[token]
                break
            else:
                await self.update_count(token, announce_self=False)  # 通知房间内的所有人，除了自己
                await self.announce_msg(token, '退出房间')
        raise StopConsumer()
