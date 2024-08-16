# standard library imports
import os

# pulumi imports
import pulumi
from pulumi import Config, export

# pan-os imports
from panos.firewall import Firewall
from panos.network import VirtualRouter, Bgp, BgpPeer, BgpPeerGroup


# Load configuration settings
config = Config()

hostname = config.require("hostname")
username = config.require("username")
vr_name = config.require("vr_name")
router_id = config.require("router_id")
local_as = config.require("local_as")
bgp_name = config.require("bgp_name")
neighbors = config.require_object("neighbors")

# Load password from environment variable
password = os.environ.get("PANOS_PASSWORD")


# Function to configure BGP on the firewall
def configure_bgp(firewall):
    dc_vr = VirtualRouter(name=vr_name)
    firewall.add(dc_vr)

    dc_bgp = Bgp(
        enable=True,
        router_id=router_id,
        local_as=local_as,
    )
    dc_vr.add(dc_bgp)
    dc_bgp.apply()

    dc_bgp_peer_group = BgpPeerGroup(
        enable=True,
        soft_reset_with_stored_info=True,
        type="ebgp",
        name=bgp_name,
    )
    dc_bgp.add(dc_bgp_peer_group)

    for each in neighbors:
        each_bgp_peer = BgpPeer(
            name=each["name"],
            enable=True,
            peer_as=each["asn"],
            address_family_identifier="ipv4",
            local_interface=each["iface"],
            local_interface_ip=each["local_ip"],
            peer_address_ip=each["peer_ip"],
        )
        dc_bgp_peer_group.add(each_bgp_peer)
        each_bgp_peer.apply()

    return dc_bgp


# Define the Pulumi program
def pulumi_program():
    firewall = Firewall(
        hostname,
        api_username=username,
        api_password=password,
    )

    bgp_resource = configure_bgp(firewall)
    pulumi.export("BGP Resource", bgp_resource)


# Run the Pulumi program
pulumi_program()