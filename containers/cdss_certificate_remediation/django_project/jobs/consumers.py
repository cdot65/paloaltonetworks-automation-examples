# django_project/jobs/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.apps import apps

logger = logging.getLogger(__name__)


class JobsConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribed_tasks = set()

    async def connect(self):
        logger.info(f"WebSocket connection attempt: {self.channel_name}")
        await self.accept()
        logger.info(f"WebSocket connection accepted: {self.channel_name}")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {self.channel_name}, code: {close_code}")
        for job_id in self.subscribed_tasks:
            await self.channel_layer.group_discard(f"job_{job_id}", self.channel_name)
        self.subscribed_tasks.clear()

    async def receive(self, text_data=None, bytes_data=None):
        logger.info(f"Received message: {text_data}")
        data = json.loads(text_data)
        action = data.get("action")
        job_id = data.get("job_id")

        if action == "subscribe" and job_id:
            group_name = f"job_{job_id}"
            logger.info(f"Subscribing to job group: {group_name}")
            await self.channel_layer.group_add(group_name, self.channel_name)
            self.subscribed_tasks.add(job_id)
            logger.info(f"Subscribed to group: {group_name}")
            await self.send_jobs(job_id)

    async def jobs(self, event):
        logger.info(f"Received job status update in consumer: {event}")
        await self.send(text_data=json.dumps(event))
        logger.info(f"Sent job status update to client: {event}")

    @sync_to_async
    def get_jobs(self, job_id):
        job_model = apps.get_model("django_celery_results", "TaskResult")
        try:
            job = job_model.objects.get(task_id=job_id)
            status = {
                "job_id": job.task_id,
                "status": job.status,
                "result": job.result,
            }
            logger.info(f"Retrieved job status: {status}")
            return status
        except job_model.DoesNotExist:
            logger.warning(f"Job not found: {job_id}")
            return None

    async def send_jobs(self, job_id):
        status = await self.get_jobs(job_id)
        if status:
            logger.info(f"Sending initial job status: {status}")
            await self.send(text_data=json.dumps(status))
        else:
            logger.warning(f"No status found for job: {job_id}")
