# django_project/task_results/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("task_status", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("task_status", self.channel_name)

    async def task_status(self, event):
        await self.send(text_data=json.dumps(event))
