# django_project/scripts/inventory_script.py


def run_script(inventory_data):
    # This function will be called with the inventory data
    print(f"Processing inventory: {inventory_data}")

    # Perform actions with the data
    device_type = inventory_data.get("device_type")
    hostname = inventory_data.get("hostname")

    # Example processing
    result = f"Processed {device_type} device with hostname {hostname}"

    # You can perform more complex operations here

    return result
