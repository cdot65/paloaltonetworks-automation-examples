"""Data models for the PAN-OS address object configuration."""

from typing import List

from pydantic import BaseModel, Field, IPvAnyNetwork


class AddressObject(BaseModel):
    """Model for an address object.

    Attributes:
        name (str): Name of the address object (1-63 chars, alphanumeric, _, -, .)
        value (IPvAnyNetwork): IP address with netmask (e.g., "192.168.1.1/32")
        description (str): Optional description (max 255 chars)
        tags (List[str]): Optional list of tags to apply to the address object
    """

    name: str = Field(..., min_length=1, max_length=63, pattern=r"^[a-zA-Z0-9_.-]+$")
    value: IPvAnyNetwork
    description: str = Field(default="", max_length=255)
    tags: List[str] = Field(default_factory=list)


class DeviceGroupEntry(BaseModel):
    """Model for a device group entry."""

    device_group: str
    entries: List[AddressObject]


class Config(BaseModel):
    """Model for the YAML configuration."""

    address_objects: List[DeviceGroupEntry]
