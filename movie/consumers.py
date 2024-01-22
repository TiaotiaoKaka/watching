import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

PROGRESS_CACHE = {}
ROOM_CACHE = {}


class ChatConsumer(AsyncWebsocketConsumer):
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
                ROOM_CACHE[token] = [self]
            else:
                ROOM_CACHE[token].append(self)
                # 通知房间内的所有人
                for token in ROOM_CACHE:
                    progress = {'count': len(ROOM_CACHE.get(token, [0]))}
                    for consumer in ROOM_CACHE[token]:
                        await consumer.send(json.dumps(progress))

            await self.send('{"msg": "ok"}')

        elif 'setprogress--' in message['text']:
            token = message['text'].split('--')[1]
            json_data = message['text'].split('--')[2]
            PROGRESS_CACHE[token] = json.loads(json_data)
            # 通知房间内的所有人
            for consumer in ROOM_CACHE[token]:
                if consumer == self:    # 不通知自己
                    continue
                progress = PROGRESS_CACHE[token]
                progress['count'] = len(ROOM_CACHE.get(token, [0]))
                await consumer.send(json.dumps(progress))

        elif 'getprogress--' in message['text']:
            token = message['text'].split('--')[1]
            progress = PROGRESS_CACHE.get(token)
            if not progress:
                progress = {'count': 0}
            else:
                progress['count'] = len(ROOM_CACHE.get(token, [0]))
            await self.send(json.dumps(progress))

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
                progress = PROGRESS_CACHE[token]
                progress['count'] = len(ROOM_CACHE.get(token, [0]))
                for consumer in ROOM_CACHE[token]:
                    await consumer.send(json.dumps(progress))

        raise StopConsumer()
