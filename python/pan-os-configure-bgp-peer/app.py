from panos.firewall import Firewall
from panos.network import VirtualRouter, Bgp, BgpPeer, BgpPeerGroup
from config import settings

firewall = Firewall(
    settings.hostname,
    api_username=settings.username,
    api_password=settings.password,
)

dc_vr = VirtualRouter(name=settings.vr_name)
firewall.add(dc_vr)

dc_bgp = Bgp(
    enable=True,
    router_id=settings.router_id,
    local_as=settings.local_as,
)
dc_vr.add(dc_bgp)
dc_bgp.apply()

dc_bgp_peer_group = BgpPeerGroup(
    enable=True,
    soft_reset_with_stored_info=True,
    type="ebgp",
    name=settings.bgp_name,
)
dc_bgp.add(dc_bgp_peer_group)

for each in settings.neighbors:
    each_bgp_peer = BgpPeer(
        name=each.name,
        enable=True,
        peer_as=each.asn,
        address_family_identifier="ipv4",
        local_interface=each.iface,
        local_interface_ip=each.local_ip,
        peer_address_ip=each.peer_ip,
    )
    dc_bgp_peer_group.add(each_bgp_peer)

    each_bgp_peer.apply()
