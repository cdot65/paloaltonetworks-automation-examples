"""Data models for the PAN-OS address object and tunnel interface configuration."""

from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network
from typing import List, Optional, Union

from pydantic import BaseModel, Field, validator


class AddressObject(BaseModel):
    """Model for an address object.

    Attributes:
        name (str): Name of the address object (1-63 chars, alphanumeric, _, -, .)
        value (IPvAnyNetwork): IP address with netmask (e.g., "192.168.1.1/32")
        description (str): Optional description (max 255 chars)
        tags (List[str]): Optional list of tags to apply to the address object
    """

    name: str = Field(..., min_length=1, max_length=63, pattern=r"^[a-zA-Z0-9_.-]+$")
    value: Union[IPv4Network, IPv6Network, IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]
    description: str = Field(default="", max_length=255)
    tags: List[str] = Field(default_factory=list)


class TunnelInterface(BaseModel):
    """
    Model for tunnel interface configuration.

    Attributes:
        name (str): Name of the tunnel interface
        subinterface (str): Subinterface number
        ip (Union[str, List[str]]): IP address of the interface (can be string or list from YAML)
        comment (str): Comment for the interface
        security_zone (str): Name of the security zone to associate the interface with
    """

    name: str = Field(..., min_length=1, max_length=63, pattern=r"^[a-zA-Z0-9_.-]+$")
    subinterface: str = Field(..., min_length=1, pattern=r"^\d+$")
    ip: Union[str, List[str]]  # Allow string or list format to support both formats
    comment: str = Field(default="", max_length=255)
    security_zone: str = Field(..., min_length=1)

    @validator("ip")
    def validate_ip_or_special_value(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Validate that the IP address is either a valid IP address,
        a special value, or a list containing such values.
        Special values start with '$'.
        """
        # If it's a list, check the first item
        if isinstance(v, list):
            if not v:
                raise ValueError("IP address list cannot be empty")
            # Just return the list for now, we'll extract the first item in app.py
            return v

        # If it's a string that starts with $, it's a special value
        if isinstance(v, str) and v.startswith("$"):
            return v

        # For regular IPs, we would validate them, but currently we're just accepting them
        # If needed, add IP validation logic here
        return v


class LoopbackInterface(BaseModel):
    """
    Model for loopback interface configuration based on PAN-OS SDK LoopbackInterface.

    Attributes:
        name (str): Name of the loopback interface (1-63 chars, alphanumeric, _, -, .)
        ip (Union[str, List[str]]): IP address of the interface (can be a single string or list)
        ipv6_enabled (bool): Whether IPv6 is enabled on this interface
        management_profile (str): Management profile name
        mtu (int): Maximum Transmission Unit
        adjust_tcp_mss (bool): Whether to adjust TCP MSS
        netflow_profile (str): Netflow profile name
        comment (str): Comment for the interface
        ipv4_mss_adjust (int): IPv4 MSS adjustment value
        ipv6_mss_adjust (int): IPv6 MSS adjustment value
    """

    name: str = Field(..., min_length=1, max_length=63, pattern=r"^[a-zA-Z0-9_.-]+$")
    ip: Union[str, List[str]]  # Allow string or list format
    ipv6_enabled: bool = False
    management_profile: Optional[str] = None
    mtu: Optional[int] = None
    adjust_tcp_mss: bool = False
    netflow_profile: Optional[str] = None
    comment: str = Field(default="", max_length=255)
    ipv4_mss_adjust: Optional[int] = None
    ipv6_mss_adjust: Optional[int] = None

    @validator("ip")
    def validate_ip_or_special_value(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Validate that the IP address is either a valid IP address,
        a special value, or a list containing such values.
        Special values start with '$'.
        """
        # If it's a list, check the first item
        if isinstance(v, list):
            if not v:
                raise ValueError("IP address list cannot be empty")
            # Just return the list for now, we'll extract the first item in app.py
            return v

        # If it's a string that starts with $, it's a special value
        if isinstance(v, str) and v.startswith("$"):
            return v

        # For regular IPs, we would validate them, but currently we're just accepting them
        # If needed, add IP validation logic here
        return v


class TemplateEntry(BaseModel):
    """Model for a template entry."""

    template: str
    entries: List[TunnelInterface]


class TemplateStackEntry(BaseModel):
    """Model for a template stack entry."""

    template_stack: str
    entries: List[LoopbackInterface]


class TunnelConfig(BaseModel):
    """Model for the tunnel interface YAML configuration."""

    tunnel_interfaces: List[TemplateEntry]


class LoopbackConfig(BaseModel):
    """Model for the loopback interface YAML configuration."""

    loopback_interfaces: List[TemplateStackEntry]


class DeviceGroupEntry(BaseModel):
    """Model for a device group entry."""

    device_group: str
    entries: List[AddressObject]


class Config(BaseModel):
    """Model for the YAML configuration."""

    address_objects: Optional[List[DeviceGroupEntry]] = None
    tunnel_interfaces: Optional[List[TemplateEntry]] = None
    loopback_interfaces: Optional[List[TemplateStackEntry]] = None
