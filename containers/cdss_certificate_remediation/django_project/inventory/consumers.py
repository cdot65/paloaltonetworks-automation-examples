import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.apps import apps

logger = logging.getLogger(__name__)


class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket connection attempt: {self.channel_name}")
        await self.accept()
        logger.info(f"WebSocket connection accepted: {self.channel_name}")
        self.subscribed_tasks = set()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {self.channel_name}, code: {close_code}")
        for task_id in self.subscribed_tasks:
            await self.channel_layer.group_discard(f"task_{task_id}", self.channel_name)
        self.subscribed_tasks.clear()

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        data = json.loads(text_data)
        action = data.get("action")
        task_id = data.get("task_id")

        if action == "subscribe" and task_id:
            group_name = f"task_{task_id}"
            logger.info(f"Subscribing to task group: {group_name}")
            await self.channel_layer.group_add(group_name, self.channel_name)
            self.subscribed_tasks.add(task_id)
            logger.info(f"Subscribed to group: {group_name}")
            await self.send_task_status(task_id)

    async def task_status(self, event):
        logger.info(f"Received task status update in consumer: {event}")
        await self.send(text_data=json.dumps(event))
        logger.info(f"Sent task status update to client: {event}")

    @sync_to_async
    def get_task_status(self, task_id):
        TaskResult = apps.get_model("django_celery_results", "TaskResult")
        try:
            task = TaskResult.objects.get(task_id=task_id)
            status = {
                "task_id": task.task_id,
                "status": task.status,
                "result": task.result,
            }
            logger.info(f"Retrieved task status: {status}")
            return status
        except TaskResult.DoesNotExist:
            logger.warning(f"Task not found: {task_id}")
            return None

    async def send_task_status(self, task_id):
        status = await self.get_task_status(task_id)
        if status:
            logger.info(f"Sending initial task status: {status}")
            await self.send(text_data=json.dumps(status))
        else:
            logger.warning(f"No status found for task: {task_id}")
