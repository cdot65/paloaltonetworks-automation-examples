# PAN-OS Firewalls Streaming Telemetry with OpenConfig and gNMI: Comprehensive Research Report

PAN-OS firewalls provide streaming telemetry capabilities through the **OpenConfig plugin**, which implements gRPC Network Management Interface (gNMI) protocol for configuration management and telemetry using OpenConfig YANG data models. This native solution enables real-time network monitoring without requiring third-party software, though it integrates well with modern telemetry stacks.

## Streaming telemetry features and supported OpenConfig modules

The PAN-OS OpenConfig plugin supports a comprehensive set of standard OpenConfig models with Palo Alto-specific augmentations. **Key supported modules include** openconfig-interfaces (v2.4.3) for interface statistics and status, openconfig-bgp for BGP routing telemetry, openconfig-system for system-level monitoring, openconfig-network-instances for virtual router management, and openconfig-platform for hardware component telemetry. Additional models cover VLANs, LLDP, local routing, and link aggregation.

The plugin supports **all standard gNMI subscription modes**: ONCE for single snapshots, POLL for on-demand data, and STREAM with three subtypes - SAMPLE for periodic updates (minimum 5-second intervals), ON_CHANGE for event-driven notifications, and TARGET_DEFINED for server-controlled intervals. Telemetry data encompasses interface counters and operational status, BGP neighbor states, system CPU and memory metrics, hardware component health, and network instance information. Custom PAN-OS models extend functionality with native configuration access, logging queries, and packet capture capabilities.

## Required plugins, licenses, and software components

OpenConfig streaming telemetry on PAN-OS requires **no additional licensing** - the plugin is included with the standard PAN-OS license. The OpenConfig plugin automatically installs on PAN-OS 11.0.4+ (plugin v2.0.1+) and PAN-OS 10.2.11+ (plugin v2.0.2+). For earlier versions, manual installation is required through the Device > Plugins interface.

**System requirements** include PAN-OS 10.1 minimum for basic support, though 11.0+ is recommended for enhanced features. VM-Series deployments require 16GB+ RAM to avoid memory issues. The plugin is fully supported on PA-3000, PA-5000, and PA-7000 series hardware, as well as VM-Series. Notably, PA-400 series firewalls do NOT support plugins. The gNMI server listens on port 9339 on the management interface and requires administrator accounts with XML API access enabled.

## Testing gNMI connectivity with gnmic CLI tool

The gnmic tool provides comprehensive testing capabilities for PAN-OS OpenConfig connectivity. **Authentication setup** supports username/password with XML API access enabled, though certificate-based authentication is recommended for production. By default, PAN-OS uses self-signed certificates on the management interface, requiring the --skip-verify flag for testing.

Essential gnmic commands for PAN-OS include capabilities discovery to verify supported models:

```bash
gnmic -a 10.1.1.1:9339 -u admin -p password --skip-verify capabilities
```

For streaming interface telemetry with 30-second sampling:

```bash
gnmic -a 10.1.1.1:9339 -u admin -p password --skip-verify -e json_ietf \
    sub --path /interfaces/interface[name=*]/state/counters \
    --mode stream --stream-mode sample --sample-interval 30s
```

**Common troubleshooting issues** include certificate validation failures (use --skip-verify for testing), connection refused errors (verify plugin installation and port 9339 accessibility), and authentication failures (ensure XML API access is enabled). For production deployments, proper certificate management with CA validation is essential.

## Step-by-step configuration process

Enabling OpenConfig streaming telemetry follows a straightforward process. First, **verify prerequisites**: PAN-OS 10.1+ (11.0+ recommended), supported hardware platform, and valid licensing. For newer versions, the plugin installs automatically; otherwise, navigate to Device > Plugins, check for available plugins, download and install the OpenConfig plugin, then commit the configuration.

The plugin **automatically starts after installation**, creating the \_\_OpenConfig device administrator user and listening on port 9339. Certificate configuration defaults to the management interface's self-signed certificate, though production deployments should implement proper certificate management. Create dedicated admin accounts with XML API access for gNMI operations. Ensure the management interface is properly configured and accessible from telemetry collectors.

## Supported OpenConfig paths and data models

PAN-OS implements **standard OpenConfig paths** for comprehensive telemetry collection. Interface paths include `/interfaces/interface[name=*]/state/oper-status` for operational status and `/interfaces/interface[name=*]/state/counters` for traffic statistics. System telemetry covers `/system/state/hostname`, `/system/cpus/cpu[index=*]/state`, and `/system/memory/state`. Platform monitoring uses `/components/component[name=*]/state` for hardware health.

The implementation includes **PAN-OS specific deviations and augmentations** through models like pan-if-deviations, pan-plat-devs, and custom models for logging (`/pan/logging/config`), configuration management (`/pan/config/delta_config`), and packet capture (`/pan/pcap/config`). Data encoding supports JSON_IETF as the primary format, with protobuf available for more efficient transmission.

## Performance considerations and scalability

**Recommended polling intervals** vary by metric type: interface counters benefit from 10-30 second sampling, while system metrics can use 30-60 second intervals. ON_CHANGE mode is ideal for operational status monitoring. The plugin enforces a 5-second minimum sampling interval. Scalability limits include 64 maximum concurrent gNMI sessions, 12MB maximum message size, and minimal resource impact when using appropriate intervals.

For **optimal performance**, use focused subscriptions instead of broad wildcards, implement data filtering at the collection point, and monitor collector resource usage. VM-Series deployments require careful memory allocation (16GB+ recommended) to avoid out-of-memory conditions reported with earlier plugin versions.

## Security requirements and authentication

PAN-OS OpenConfig implements **comprehensive security measures**. Certificate management defaults to self-signed certificates but production deployments should use proper CA-signed certificates with regular rotation. Authentication supports username/password (basic), mutual TLS (recommended for production), and integration with PAN-OS role-based access control.

**Security best practices** include creating dedicated service accounts for telemetry with read-only permissions, restricting management interface access to trusted networks, implementing network segmentation for telemetry traffic, and monitoring for authentication failures. Recent security advisory CVE-2025-0110 affecting authenticated administrators was addressed in plugin version 2.1.2, making immediate upgrades critical.

## Example gnmic commands and configurations

**Production-ready gnmic configuration** uses YAML files for consistent deployment:

```yaml
username: admin
password: secure-password
skip-verify: true
encoding: json_ietf
targets:
  panos-fw1:
    address: 10.1.1.1:9339
    timeout: 30s
subscriptions:
  interface-status:
    paths:
      - /interfaces/interface/state/oper-status
    mode: stream
    stream-mode: on_change
  interface-counters:
    paths:
      - /interfaces/interface/state/counters
    mode: stream
    stream-mode: sample
    sample-interval: 30s
```

Common operational commands include interface monitoring for real-time status changes and periodic counter collection. System health monitoring tracks CPU, memory, and component status at appropriate intervals.

## Integration with telemetry collectors

**Telegraf integration** provides a popular collection pattern:

```toml
[[inputs.gnmi]]
  addresses = ["10.1.1.1:9339"]
  username = "telemetry"
  password = "secure-password"
  encoding = "json_ietf"
  enable_tls = true
  insecure_skip_verify = true

  [[inputs.gnmi.subscription]]
    name = "interface_counters"
    origin = "openconfig-interfaces"
    path = "/interfaces/interface/state/counters"
    subscription_mode = "sample"
    sample_interval = "30s"
```

Common **integration stacks** include TIG (Telegraf + InfluxDB + Grafana) for comprehensive monitoring, Prometheus with custom exporters for cloud-native environments, and OpenTelemetry collectors for modern observability platforms. Production deployments benefit from collector redundancy, dedicated monitoring networks, and proper capacity planning.

## Version compatibility matrix

OpenConfig support varies significantly across PAN-OS versions. **Plugin 1.x series** supports PAN-OS 10.1+ with manual installation required, while **Plugin 2.x series** requires PAN-OS 11.0+ (except plugin 2.0.2 which supports 10.2.11+). Automatic installation occurs on PAN-OS 11.0.4+ and 10.2.11+ for appropriate plugin versions.

**Platform-specific considerations** include full support on PA-3000, PA-5000, and PA-7000 series hardware, with PA-400 series notably lacking plugin support. VM-Series requires increased memory allocation (16GB+ for plugin 2.x). The latest recommended configuration uses PAN-OS 11.2+ with OpenConfig plugin 2.1.2 for optimal security and feature support.

## Conclusion

PAN-OS OpenConfig streaming telemetry provides a robust, native solution for real-time network monitoring that balances standard compliance with platform-specific capabilities. While limited to Layer 4 networking features and requiring careful resource management on VM-Series deployments, the implementation offers comprehensive telemetry suitable for modern network operations. Organizations should prioritize upgrading to plugin version 2.1.2 for security fixes, implement proper certificate management, and follow performance optimization guidelines for production deployments. The native integration with standard telemetry stacks like Telegraf, InfluxDB, and Grafana enables seamless adoption into existing monitoring infrastructure.
