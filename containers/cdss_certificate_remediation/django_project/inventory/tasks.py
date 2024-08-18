# django_project/inventory/tasks.py
from celery import shared_task
from .models import Inventory
from ..task_results.models import TaskResult
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import importlib.util
import sys


@shared_task
def run_inventory_script(inventory_id):
    task_result = TaskResult.objects.create(
        task_id=run_inventory_script.request.id, status="STARTED"
    )
    try:
        inventory = Inventory.objects.get(id=inventory_id)

        # Dynamically import the script
        spec = importlib.util.spec_from_file_location(
            "inventory_script", "django_project/scripts/inventory_script.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules["inventory_script"] = module
        spec.loader.exec_module(module)

        # Run the script with inventory data
        result = module.run_script(
            {
                "device_type": inventory.device_type,
                "hostname": inventory.hostname,
                "username": inventory.username,
                "connection_address": inventory.get_connection_address(),
            }
        )
        task_result.status = "SUCCESS"
        task_result.result = result
    except Exception as e:
        task_result.status = "FAILURE"
        task_result.result = {"error": str(e)}
    finally:
        task_result.save()

    # Send update via WebSocket
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "task_status",
            {
                "type": "task_status",
                "task_id": run_inventory_script.request.id,
                "status": task_result.status,
                "result": task_result.result,
            },
        )
    except Exception as e:
        print(f"Error sending WebSocket message: {str(e)}")

    return task_result.result
