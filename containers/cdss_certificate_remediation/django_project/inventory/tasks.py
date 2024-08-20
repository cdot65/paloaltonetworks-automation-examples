# django_project/inventory/tasks.py
import importlib.util
import sys

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Inventory
from ..jobs.models import Job
import json
import logging

logger = logging.getLogger(__name__)


@shared_task
def run_inventory_script(inventory_id):
    channel_layer = get_channel_layer()
    job_id = run_inventory_script.request.id

    def send_status_update(status, result=None):
        group_name = f"job_{job_id}"
        message = {
            "type": "jobs",
            "job_id": job_id,
            "status": status,
            "result": result,
        }
        logger.info(f"Sending job update to group {group_name}: {message}")
        async_to_sync(channel_layer.group_send)(group_name, message)

        Job.objects.update_or_create(
            job_id=job_id,
            defaults={
                "status": status,
                "result": json.dumps(result) if result else None,
            },
        )

    send_status_update("STARTED")

    try:
        inventory = Inventory.objects.get(id=inventory_id)
        logger.info(f"Retrieved inventory: {inventory}")

        # Dynamically import the script
        script_path = "django_project/scripts/inventory_script.py"
        logger.info(f"Importing script from {script_path}")
        spec = importlib.util.spec_from_file_location("inventory_script", script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["inventory_script"] = module
        spec.loader.exec_module(module)

        # Run the script with inventory data
        send_status_update("PROGRESS", "Running inventory script")
        script_data = {
            "device_type": inventory.device_type,
            "hostname": inventory.hostname,
            "username": inventory.username,
            "connection_address": inventory.get_connection_address(),
        }
        logger.info(f"Running script with data: {script_data}")
        result = module.run_script(script_data)
        logger.info(f"Script result: {result}")
        send_status_update("SUCCESS", result)
        logger.info(f"Sent SUCCESS status for job {job_id}")
        return result
    except Exception as e:
        logger.exception(f"Error in run_inventory_script: {str(e)}")
        error_result = {"error": str(e)}
        send_status_update("FAILURE", error_result)
        logger.info(f"Sent FAILURE status for job {job_id}")
        return error_result
