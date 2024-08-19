# django_project/inventory/utils.py
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


def send_task_update(task_id, status, result):
    channel_layer = get_channel_layer()
    group_name = f"task_{task_id}"
    message = {
        "type": "task_status",
        "task_id": task_id,
        "status": status,
        "result": result,
    }
    logger.info(f"Attempting to send task update to group {group_name}: {message}")
    try:
        async_to_sync(channel_layer.group_send)(group_name, message)
        logger.info(f"Successfully sent task update to group {group_name}")
    except Exception as e:
        logger.error(f"Failed to send task update to group {group_name}: {str(e)}")
