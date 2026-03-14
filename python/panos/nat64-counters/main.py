"""
Fetch PAN-OS global counter entries whose <name> contains any of the given patterns.

Requires:
    pip install httpx[lz4] lxml
"""

from __future__ import annotations
from typing import List, Dict, Tuple
from lxml import etree
import httpx


def fetch_counters(
    firewall_host: str,
    api_key: str,
    *,
    patterns: Tuple[str, ...] = ("nat64",),
    verify_ssl: bool = False,  # set True if you have the PAN-OS CA chain
    timeout: float = 60.0,
) -> List[Dict[str, str]]:
    """Return a list of dicts for every <entry> whose <name> contains *any*
    of the given *patterns*.

    Parameters
    ----------
    firewall_host : str
        FQDN or IP of the PAN-OS firewall.
    api_key : str
        API key with *X-PAN-KEY* authentication.
    patterns : tuple[str, ...], default ("nat64",)
        Sub-strings to search for inside the <name> element.  The match is
        case-sensitive, mirroring the on-device counter names.

    Examples
    --------
    >>> fetch_counters("fw.example.com", "MY_API_KEY", patterns=("nat64", "nptv6"))[0]["name"]
    'flow_nat64_icmp_6to4_no_xlat'
    """
    cmd_xml = (
        "<show>"
        "<counter>"
        "<global>"
        "<filter><value>all</value></filter>"
        "</global>"
        "</counter>"
        "</show>"
    )

    url = f"https://{firewall_host}/api"
    headers = {"X-PAN-KEY": api_key}
    params = {"type": "op", "cmd": cmd_xml}

    with httpx.Client(verify=verify_ssl, timeout=timeout) as client:
        resp = client.get(url, headers=headers, params=params)
        resp.raise_for_status()

    root = etree.fromstring(resp.content)  # type: etree._Element
    # Build dynamic XPath: contains(name, "p1") or contains(name, "p2") ...
    cond = " or ".join(f'contains(name, "{p}")' for p in patterns)
    xpath_expr = f".//entry[{cond}]"

    matched_entries = root.xpath(xpath_expr)

    results: List[Dict[str, str]] = []
    for entry in matched_entries:
        results.append({child.tag: child.text for child in entry})

    return results


if __name__ == "__main__":
    # TODO: load from env vars
    FIREWALL = "firewall.example.io"
    API_KEY = "api-key-was-here"

    for c in fetch_counters(FIREWALL, API_KEY, patterns=("nat64", "nptv6")):
        print(
            f"{c['name']:<35} value={c['value']:<5} "
            f"rate={c['rate']:<4} severity={c['severity']}"
        )
