import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django_celery_results.models import TaskResult

class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.task_group_name = None

    async def disconnect(self, close_code):
        if self.task_group_name:
            await self.channel_layer.group_discard(self.task_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        task_id = data.get('task_id')
        if task_id:
            self.task_group_name = f'task_{task_id}'
            await self.channel_layer.group_add(self.task_group_name, self.channel_name)
            await self.send_task_status(task_id)

    async def task_status(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_task_status(self, task_id):
        try:
            task = TaskResult.objects.get(task_id=task_id)
            return {
                'task_id': task.task_id,
                'status': task.status,
                'result': task.result,
            }
        except TaskResult.DoesNotExist:
            return None

    async def send_task_status(self, task_id):
        status = await self.get_task_status(task_id)
        if status:
            await self.send(text_data=json.dumps(status))
