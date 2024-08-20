# django_project/inventory/utils.py
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


def send_job_update(job_id, status, result):
    channel_layer = get_channel_layer()
    group_name = f"job_{job_id}"
    message = {
        "type": "jobs",
        "job_id": job_id,
        "status": status,
        "result": result,
    }
    logger.info(f"Attempting to send job update to group {group_name}: {message}")
    try:
        async_to_sync(channel_layer.group_send)(group_name, message)
        logger.info(f"Successfully sent job update to group {group_name}")
    except Exception as e:
        logger.error(f"Failed to send job update to group {group_name}: {str(e)}")
