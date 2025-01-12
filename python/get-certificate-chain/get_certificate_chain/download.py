"""
Download SSL certificate chain and save as PEM files.

This script connects to a given website, downloads its SSL certificate,
and saves it as a PEM file. If the certificate has an Authority Information
Access (AIA) extension, the script will download each certificate in the chain
and save them as PEM files as well.

"""

# Standard library imports
import os
import logging
import re
import ssl
import socket
import sys
from typing import Any, Dict, List, Optional, Union
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Third-party library imports
import argparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import ExtensionOID

VERSION = "0.1.7"
CERT_CHAIN = []


def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args (Optional[List[str]]): List of arguments to parse. If None, defaults to sys.argv.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Export security rules and associated Security Profile Groups to a CSV file."
    )
    parser.add_argument(
        "--get-ca-cert-pem",
        dest="get_ca_cert_pem",
        action="store_true",
        help="Get cacert.pem from curl.se website to help find Root CA.",
    )
    parser.add_argument(
        "--host",
        dest="host",
        default="www.google.com",
        help="The host to connect to. (default: %(default)s)",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Set the logging level. (default: %(default)s)",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=".",
        help="The output directory for the certificate chain files. (default: current directory)",
    )
    parser.add_argument(
        "--rm-ca-files",
        dest="remove_ca_files",
        action="store_true",
        help="Remove the cert files in current directory (*.crt, *.pem).",
    )
    return parser.parse_args()


class SSLCertificateChainDownloader:
    def __init__(self, output_directory: str = None):
        """
        Initialize the SSLCertificateChainDownloader.

        Args:
            output_directory (str, optional): Directory to save the certificate files. Defaults to None.
        """
        self.cert_chain = []
        self._output_directory = output_directory

    @property
    def output_directory(self) -> str:
        """Get the output directory for saving certificates."""
        return self._output_directory if self._output_directory else "."

    def remove_cacert_pem(self):
        """
        Remove certificate files from the current directory.
        """
        logging.info("Removing certificate files from current directory.")
        output_directory = self.output_directory

        for filename in os.listdir(output_directory):
            if filename.endswith(".crt") or filename == "cacert.pem":
                filepath = os.path.join(output_directory, filename)
                os.remove(filepath)
                logging.info(f"Removed {filename}")

    def get_cacert_pem(self):
        """
        Download the cacert.pem file from the curl.se website.
        """
        cacert_pem_url = "https://curl.se/ca/cacert.pem"
        cacert_pem_file = "cacert.pem"
        logging.info("Downloading %s to %s", cacert_pem_url, cacert_pem_file)
        with urlopen(cacert_pem_url) as response, open(
            cacert_pem_file, "wb"
        ) as out_file:
            if response.getcode() != 200:
                logging.error(
                    "Error downloading %s. HTTP status code: %s",
                    cacert_pem_url,
                    response.getcode(),
                )
                sys.exit(1)
            data = response.read()
            out_file.write(data)
        logging.info("Downloaded %s to %s", cacert_pem_url, cacert_pem_file)

    @staticmethod
    def check_url(host: str) -> Dict[str, Any]:
        """
        Check and parse the host provided by the user.

        Args:
            host (str): The host provided by the user.

        Returns:
            Dict[str, Any]: A dictionary containing the host and port.
        """
        host, _, port = host.partition(":")
        return {"host": host, "port": int(port) if port else 443}

    def get_certificate(self, host: str, port: int) -> x509.Certificate:
        """
        Connect to a server and retrieve the SSL certificate.

        Args:
            host (str): The host to connect to.
            port (int): The port to connect to.

        Returns:
            x509.Certificate: The SSL certificate of the server.
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssl_socket:
                    cert_pem = ssl.DER_cert_to_PEM_cert(ssl_socket.getpeercert(True))
                    cert = x509.load_pem_x509_certificate(
                        cert_pem.encode(), default_backend()
                    )
            return cert
        except ConnectionRefusedError:
            logging.error("Connection refused to %s:%s", host, port)
            sys.exit(1)
        except ssl.SSLError as e:
            logging.error("SSL error: %s", e)
            sys.exit(1)
        except socket.timeout:
            logging.error("Connection timed out to %s:%s", host, port)
            sys.exit(1)
        except socket.gaierror:
            logging.error("Hostname could not be resolved: %s", host)
            sys.exit(1)

    def normalize_subject(self, subject: str) -> str:
        """
        Normalize the subject of a certificate.

        Args:
            subject (str): The subject of the certificate.

        Returns:
            str: The normalized subject.
        """
        return "_".join(
            part.strip()
            .replace("=", "_")
            .replace(".", "_")
            .replace(" ", "_")
            .replace(",", "_")
            for part in subject.split("/")
            if part.strip()
        )

    def save_ssl_certificate(
        self,
        ssl_certificate: x509.Certificate,
        file_name: str,
    ) -> None:
        """
        Save an SSL certificate to a file.

        Args:
            ssl_certificate (x509.Certificate): The SSL certificate to save.
            file_name (str): The file name to save the SSL certificate as.
        """
        with open(file_name, "wb") as f:
            f.write(ssl_certificate.public_bytes(encoding=serialization.Encoding.PEM))

    def write_chain_to_file(
        self, certificate_chain: List[x509.Certificate], output_dir: str = "."
    ) -> None:
        """
        Write a certificate chain to files.

        Args:
            certificate_chain (List[x509.Certificate]): The certificate chain to write to files.
            output_dir (str, optional): The output directory for the certificate files. Defaults to ".".
        """
        os.makedirs(self.output_directory, exist_ok=True)
        for counter, certificate_item in enumerate(certificate_chain):
            cert_subject = certificate_item.subject.rfc4514_string()
            normalized_subject = self.normalize_subject(cert_subject)
            ssl_certificate_filename = (
                f"{len(certificate_chain) - 1 - counter}-{normalized_subject}.crt"
            )
            ssl_certificate_filepath = os.path.join(
                self.output_directory, ssl_certificate_filename
            )
            self.save_ssl_certificate(certificate_item, ssl_certificate_filepath)

    def return_cert_aia(self, ssl_certificate: x509.Certificate) -> x509.Extensions:
        """
        Get the Authority Information Access (AIA) extension from a certificate.

        Args:
            ssl_certificate (x509.Certificate): The SSL certificate.

        Returns:
            x509.Extensions: The AIA extension or None if not found.
        """
        try:
            aia = ssl_certificate.extensions.get_extension_for_oid(
                ExtensionOID.AUTHORITY_INFORMATION_ACCESS
            )
            return aia
        except x509.ExtensionNotFound:
            return None

    def get_certificate_from_uri(self, uri: str) -> x509.Certificate:
        """
        Retrieve a certificate from the given URI.

        Args:
            uri (str): The URI to get the certificate from.

        Returns:
            x509.Certificate: The certificate from the URI or None if there was an error.
        """
        try:
            with urlopen(uri) as response:
                if response.getcode() != 200:
                    return None
                aia_content = response.read()
                ssl_certificate = ssl.DER_cert_to_PEM_cert(aia_content)
                cert = x509.load_pem_x509_certificate(
                    ssl_certificate.encode("ascii"), default_backend()
                )
                return cert
        except (HTTPError, URLError):
            return None

    def return_cert_aia_list(self, ssl_certificate: x509.Certificate) -> list:
        """
        Get the list of AIA URIs from a certificate.

        Args:
            ssl_certificate (x509.Certificate): The SSL certificate.

        Returns:
            list: A list of AIA URIs.
        """
        aia_uri_list = []

        for extension in ssl_certificate.extensions:
            cert_value = extension.value

            if isinstance(cert_value, x509.AuthorityInformationAccess):
                data_aia = [x for x in cert_value or []]
                for item in data_aia:
                    if item.access_method._name == "caIssuers":
                        aia_uri_list.append(item.access_location._value)

        return aia_uri_list

    def return_cert_aki(
        self, ssl_certificate: x509.Certificate
    ) -> x509.AuthorityKeyIdentifier:
        """
        Get the Authority Key Identifier (AKI) from a certificate.

        Args:
            ssl_certificate (x509.Certificate): The SSL certificate.

        Returns:
            x509.AuthorityKeyIdentifier: The AKI extension or None if not found.
        """
        try:
            cert_aki = ssl_certificate.extensions.get_extension_for_oid(
                ExtensionOID.AUTHORITY_KEY_IDENTIFIER
            )
        except x509.extensions.ExtensionNotFound:
            cert_aki = None
        return cert_aki

    def return_cert_ski(
        self, ssl_certificate: x509.Certificate
    ) -> x509.SubjectKeyIdentifier:
        """
        Get the Subject Key Identifier (SKI) from a certificate.

        Args:
            ssl_certificate (x509.Certificate): The SSL certificate.

        Returns:
            x509.SubjectKeyIdentifier: The SKI extension.
        """
        cert_ski = ssl_certificate.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_KEY_IDENTIFIER
        )
        return cert_ski

    def load_root_ca_cert_chain(
        self,
        filename: str = None,
        ca_cert_text: str = None,
    ) -> Dict[str, str]:
        """
        Load the root CA certificate chain from a file or text.

        Args:
            filename (str, optional): The file name containing the root CA certificates.
            ca_cert_text (str, optional): The text containing the root CA certificates.

        Returns:
            Dict[str, str]: A dictionary containing the root CA certificates.
        """
        if filename is None and ca_cert_text is None:
            raise ValueError("Either filename or ca_cert_text must be provided")

        ca_root_store = {}

        if filename:
            with open(filename, "r") as f_ca_cert:
                ca_cert_text = f_ca_cert.read()

        lines = ca_cert_text.splitlines()
        line_count = len(lines)
        index = 0

        while index < line_count:
            current_line = lines[index]

            if re.search(r"^-----BEGIN CERTIFICATE-----", current_line):
                root_ca_cert = ""
                index += 1
                while index < line_count and not re.search(
                    r"^-----END CERTIFICATE-----", lines[index]
                ):
                    root_ca_cert += lines[index] + "\n"
                    index += 1

                root_ca_cert += lines[index] + "\n"
                index += 1

                cert = x509.load_pem_x509_certificate(
                    root_ca_cert.encode(), default_backend()
                )
                root_ca_name = cert.subject.rfc4514_string()
                ca_root_store[root_ca_name] = root_ca_cert
            else:
                index += 1

        logging.info("Number of Root CAs loaded: %d", len(ca_root_store))
        return ca_root_store

    def walk_the_chain(
        self,
        ssl_certificate: x509.Certificate,
        depth: int,
        max_depth: int = 4,
    ):
        """
        Recursively walk the certificate chain to gather all intermediate and root certificates.

        Args:
            ssl_certificate (x509.Certificate): The current SSL certificate being processed.
            depth (int): The depth of the current SSL certificate in the chain.
            max_depth (int, optional): The maximum depth allowed for the certificate chain. Defaults to 4.

        Raises:
            SystemExit: If a certificate cannot be retrieved, if a certificate doesn't have the AIA
                        extension, or if the root CA is not found in the pre-existing root CA store.
        """
        if depth <= max_depth:
            cert_aki = self.return_cert_aki(ssl_certificate)
            cert_ski = self.return_cert_ski(ssl_certificate)

            cert_aki_value = (
                cert_aki._value.key_identifier if cert_aki is not None else None
            )
            cert_ski_value = cert_ski._value.digest
            logging.info(
                f"Depth: {depth} - AKI: {cert_aki_value} - SKI: {cert_ski_value}"
            )

            if cert_aki_value is not None:
                aia_uri_list = self.return_cert_aia_list(ssl_certificate)
                if aia_uri_list:
                    for item in aia_uri_list:
                        next_cert = self.get_certificate_from_uri(item)
                        if next_cert is not None:
                            self.cert_chain.append(next_cert)
                            self.walk_the_chain(next_cert, depth + 1, max_depth)
                        else:
                            logging.warning("Could not retrieve certificate.")
                            sys.exit(1)
                else:
                    logging.warning("Certificate didn't have AIA.")
                    ca_root_store = self.load_root_ca_cert_chain("cacert.pem")
                    root_ca_cn = None

                    for root_ca in ca_root_store:
                        try:
                            root_ca_certificate_pem = ca_root_store[root_ca]
                            root_ca_certificate = x509.load_pem_x509_certificate(
                                root_ca_certificate_pem.encode("ascii")
                            )
                            root_ca_ski = self.return_cert_ski(root_ca_certificate)
                            root_ca_ski_value = root_ca_ski._value.digest

                            if root_ca_ski_value == cert_aki_value:
                                root_ca_cn = root_ca
                                self.cert_chain.append(root_ca_certificate)
                                logging.info(
                                    f"Root CA Found - {root_ca_cn}\nCERT_CHAIN - {self.cert_chain}"
                                )
                                break
                        except x509.extensions.ExtensionNotFound:
                            logging.info("Root CA didn't have a SKI. Skipping...")
                            pass

                    if root_ca_cn is None:
                        logging.error("Root CA NOT found.")
                        sys.exit(1)

    def run(self, args: Union[argparse.Namespace, dict]) -> Dict[str, List[str]]:
        """
        Main method that handles the execution of SSLCertificateChainDownloader based on the provided arguments.

        Args:
            args (Union[argparse.Namespace, dict]): A set of input arguments, either in the form of an
                                                    argparse.Namespace object or a dictionary.

        Raises:
            ValueError: If the provided 'args' is not an instance of argparse.Namespace or dict.

        Returns:
            Dict[str, List[str]]: A dictionary containing a key 'files' with a list of the paths of the saved certificate
                                chain files in the output directory.
        """
        if isinstance(args, argparse.Namespace):
            self.host = args.host
        elif isinstance(args, dict):
            self.host = args.get("host")
        else:
            raise ValueError(
                "Invalid argument type. Expected argparse.Namespace or dict."
            )

        self.parsed_url = SSLCertificateChainDownloader.check_url(self.host)

        if isinstance(args, argparse.Namespace):
            remove_ca_files = args.remove_ca_files
            get_ca_cert_pem = args.get_ca_cert_pem
        else:
            remove_ca_files = args.get("remove_ca_files")
            get_ca_cert_pem = args.get("get_ca_cert_pem")

        if remove_ca_files:
            self.remove_cacert_pem()
            return

        if get_ca_cert_pem:
            self.get_cacert_pem()

        ssl_certificate = self.get_certificate(
            self.parsed_url["host"], self.parsed_url["port"]
        )

        aia = self.return_cert_aia(ssl_certificate)

        if aia is not None and not self.return_cert_aia(ssl_certificate):
            logging.error(
                "Could not find AIA, possible decryption taking place upstream?"
            )
            sys.exit(1)

        self.cert_chain.append(ssl_certificate)

        self.walk_the_chain(ssl_certificate, 1, max_depth=4)

        self.write_chain_to_file(self.cert_chain)

        logging.info("Certificate chain downloaded and saved.")

        return {
            "files": [
                os.path.join(self.output_directory, f)
                for f in os.listdir(self.output_directory)
                if f.endswith(".crt")
            ]
        }


def main() -> None:
    """
    Main function to execute the script. Parses arguments, retrieves the SSL certificate, walks the chain,
    and writes the certificate chain and PEM-encoded certificates.
    """
    args = parse_arguments()

    log_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(log_level, int):
        raise ValueError(f"Invalid log level: {args.log_level}")

    logging.basicConfig(
        level=log_level, format="%(asctime)s [%(levelname)s] %(message)s"
    )

    downloader = SSLCertificateChainDownloader(output_directory=args.output_dir)
    downloader.run(args)


if __name__ == "__main__":
    main()
