import os
import pytest
from download import (
    SSLCertificateChainDownloader,
)


@pytest.fixture
def root_ca_cert():
    with open(
        os.path.join(os.path.dirname(__file__), "test_data/root_ca_cert.pem"), "r"
    ) as f:
        cert = f.read()
    return cert


@pytest.fixture
def server_cert():
    with open(
        os.path.join(os.path.dirname(__file__), "test_data/server_cert.pem"), "r"
    ) as f:
        cert = f.read()
    return cert


@pytest.fixture
def cert_data(root_ca_cert, server_cert):
    return {
        "ca_cert_text": root_ca_cert,
        "cert_text": server_cert,
    }


def test_normalize_subject():
    downloader = SSLCertificateChainDownloader()

    subject = "/C=US/ST=California/L=Mountain View/O=Google LLC/CN=www.google.com"
    assert (
        downloader.normalize_subject(subject)
        == "C_US_ST_California_L_Mountain_View_O_Google_LLC_CN_www_google_com"
    )
