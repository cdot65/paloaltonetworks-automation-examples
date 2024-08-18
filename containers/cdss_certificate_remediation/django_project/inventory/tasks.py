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
    channel_layer = get_channel_layer()
    task_id = run_inventory_script.request.id

    def send_status_update(status, result=None):
        async_to_sync(channel_layer.group_send)(
            f'task_{task_id}',
            {
                'type': 'task_status',
                'task_id': task_id,
                'status': status,
                'result': result,
            }
        )

    send_status_update('STARTED')


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
        result = module.run_script({
            "device_type": inventory.device_type,
            "hostname": inventory.hostname,
            "username": inventory.username,
            "connection_address": inventory.get_connection_address(),
        })
        send_status_update('SUCCESS', result)
        return result
    except Exception as e:
        error_result = {'error': str(e)}
        send_status_update('FAILURE', error_result)
        return error_result
