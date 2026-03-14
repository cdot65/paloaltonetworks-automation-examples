# SSL Certificate Chain Downloader

## Overview

A Python CLI tool and library that connects to a host over TLS, downloads the server's SSL certificate, and recursively walks the certificate chain via Authority Information Access (AIA) extensions to retrieve all intermediate and root CA certificates. Each certificate is saved as a numbered PEM-encoded `.crt` file. Built with the `cryptography` library, it supports custom output directories, optional Mozilla/curl root CA bundle download, and can be used programmatically as a library. Useful for building complete certificate chains for import into Palo Alto Networks firewalls and Panorama.

## Prerequisites

- Python 3.9+
- Poetry (for dependency management) or pip

## Quickstart

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/general/certificate-chain
   ```

2. **Create and activate a virtual environment:**

   ```bash
   poetry install
   poetry shell
   ```

   > **Tip -- What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python. This prevents version conflicts between projects.

3. **Install from PyPI (alternative):**

   ```bash
   pip install get-certificate-chain
   ```

4. **No additional configuration is needed.** The tool connects directly to the target host.

5. **Run the tool:**

   ```bash
   get-certificate-chain --host www.google.com
   ```

## Configuration

This tool does not require configuration files or API keys. All options are passed via CLI arguments:

| Argument | Required | Description |
|---|---|---|
| `--host` | No | Target hostname (default: `www.google.com`). Supports `host:port` format |
| `--output-dir` | No | Directory for certificate files (default: current directory) |
| `--get-ca-cert-pem` | No | Download Mozilla/curl `cacert.pem` root CA bundle |
| `--rm-ca-files` | No | Remove `.crt` and `.pem` files from the output directory |
| `--log-level` | No | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: WARNING) |

## Usage

**Download the certificate chain for a host:**

```bash
get-certificate-chain --host www.example.com
```

**Download chain to a specific output directory:**

```bash
get-certificate-chain --host paloaltonetworks.com --output-dir ./certs
```

**Download the Mozilla root CA bundle first (needed when intermediates lack AIA):**

```bash
get-certificate-chain --host internal.example.com --get-ca-cert-pem
```

**Remove previously downloaded certificate files:**

```bash
get-certificate-chain --rm-ca-files
```

**Use as a Python library:**

```python
from get_certificate_chain.download import SSLCertificateChainDownloader

downloader = SSLCertificateChainDownloader(output_directory="/tmp/certs")
result = downloader.run({"host": "www.google.com"})
print(result["files"])
```

### Expected Output

When downloading the chain for `www.google.com`:

```
$ get-certificate-chain --host www.google.com --log-level INFO
2024-01-15 14:30:22 [INFO] Depth: 1 - AKI: b'...' - SKI: b'...'
2024-01-15 14:30:22 [INFO] Depth: 2 - AKI: b'...' - SKI: b'...'
2024-01-15 14:30:22 [INFO] Certificate chain downloaded and saved.
```

The tool creates numbered `.crt` files in the output directory:

```
0-CN_GlobalSign_Root_CA_-_R2_O_GlobalSign_OU_GlobalSign_Root_CA_-_R2.crt
1-CN_GTS_CA_1C3_O_Google_Trust_Services_LLC.crt
2-CN_www_google_com.crt
```

Files are numbered from root (0) to leaf (highest number). Each file contains a PEM-encoded X.509 certificate.

## Project Structure

```
certificate-chain/
  pyproject.toml                       # Poetry config with CLI entry point and dependencies
  get_certificate_chain/
    download.py                        # SSLCertificateChainDownloader class and CLI main()
    tests/
      test_cert.py                     # Unit tests for subject normalization and cert loading
      test_data/                       # Test certificates and OpenSSL config files
  docs/
    conf.py                            # Sphinx documentation configuration
    index.rst                          # Documentation index
    Makefile                           # Sphinx build targets
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `Connection refused to host:port` | Host not accepting connections on the specified port | Verify the host and port are correct; default port is 443 |
| `SSL error` | TLS handshake failure | Check if the host uses a non-standard TLS configuration or is behind a proxy |
| `ModuleNotFoundError: No module named 'cryptography'` | Dependencies not installed | Run `poetry install` or `pip install cryptography` |
| `Hostname could not be resolved` | DNS resolution failure | Verify the hostname is correct and DNS is functioning |
| Connection timed out | Network issues or firewall blocking | Check network connectivity to the target host on port 443 |
| `Could not retrieve certificate` | AIA URI returned an error | The intermediate CA server may be unreachable; try with `--get-ca-cert-pem` flag |
| `Root CA NOT found` | Root CA not in cacert.pem bundle | Download the latest bundle with `--get-ca-cert-pem` or add the root CA manually |
