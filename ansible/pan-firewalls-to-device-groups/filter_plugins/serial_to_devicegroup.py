def find_device_group(data, serial_number):
    device_groups = (
        data.get("response", {})
        .get("result", {})
        .get("devicegroups", {})
        .get("entry", [])
    )

    for group in device_groups:
        devices_entry = group.get("devices", {}).get("entry", {})
        # Check if 'devices_entry' is a list and iterate through it
        if isinstance(devices_entry, list):
            for device in devices_entry:
                if device.get("@name") == serial_number:
                    return group.get("@name")
        # If 'devices_entry' is a dictionary, directly compare the serial number
        elif devices_entry.get("@name") == serial_number:
            return group.get("@name")

    return "Device group not found"


class FilterModule(object):
    """Custom filter to find device group"""

    def filters(self):
        return {"find_device_group": find_device_group}
