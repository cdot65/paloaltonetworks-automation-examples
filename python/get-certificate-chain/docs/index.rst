.. _get_certificate_chain:

============================
Get Certificate Chain 🌐🔐
============================

This Python script retrieves the certificate chain from a website, allowing you to analyze and verify the SSL/TLS certificates of the website. This project is a custom fork of the `getCertificateChain project <https://github.com/TheScriptGuy/getCertificateChain>`_, and the overwhelming majority of credit goes to `TheScriptGuy <https://github.com/TheScriptGuy>`_.

.. contents:: Table of Contents
   :local:

Requirements 📋
---------------

- Python 3.9+
- Poetry (optional) - `Python Poetry <https://python-poetry.org/docs/>`_

Installation
------------

PyPi
^^^^^

To install the package from PyPi, simply run the appropriate command.

.. code-block:: bash

   pip install get-certificate-chain

GitHub
^^^^^^

To install from the GitHub repository, follow these steps:

1. Clone the repository.
2. Change the directory to the cloned repository.
3. Install the package using pip.

.. code-block:: bash

   git clone https://github.com/cdot65/get_certificate_chain.git
   cd get_certificate_chain
   pip install .

Usage 🚀
--------

Import into script
^^^^^^^^^^^^^^^^^^

To use the package in your script, simply import the package and create an instance of the `SSLCertificateChainDownloader` object.


To pass arguments into the object, you can use the `argparse` library:

.. code-block:: python

   import argparse
   from get_certificate_chain.download import SSLCertificateChainDownloader

   # Add your arguments
   args = parser.parse_args()

   downloader = SSLCertificateChainDownloader()
   downloader.run(args)

Or pass the arguments directly into the object:

.. code-block:: python

   from get_certificate_chain.download import SSLCertificateChainDownloader
   args = {'host': 'www.google.com'}
   downloader = SSLCertificateChainDownloader()
   downloader.run(args)

You may also specify an output directory when creating an instance of the class:

.. code-block:: python

   from get_certificate_chain.download import SSLCertificateChainDownloader
   downloader = SSLCertificateChainDownloader(output_directory="/var/tmp")
   downloader.run({"host": "www.google.com"})

Command Line CLI
^^^^^^^^^^^^^^^^

To use the script from the command line, run the following command:

.. code-block:: bash

   get-certificate-chain --host www.google.com
   get-certificate-chain --rm-ca-files

Arguments
+++++++++

- `--host`: The host:port pair that the script should connect to. Defaults to www.google.com:443.
- `--rm-ca-files`: Remove the certificate files in the current working directory (`*.crt`, `*.pem`).
- `--get-ca-cert-pem`: Get cacert.pem from the curl.se website to help find Root CA.
- `--log-level`: Set the log level. Defaults to INFO.
- `--output-dir`: Set the output directory. Defaults to the current working directory.

Contributing
------------

Contributions are welcome! To contribute, please follow these guidelines:

1. Write tests for your code using `pytest`. Make sure your tests follow the standards set by the existing tests.
2. Set up a virtual environment using `Poetry`. You can install Poetry by following the instructions at https://python-poetry.org/docs/#installation.

To set up a new virtual environment for the project, run the appropriate command.

.. code-block:: bash

   poetry install

To activate the virtual environment, run the appropriate command.

.. code-block:: bash

   poetry shell

After making your changes and adding tests, ensure that all tests pass by running the appropriate command.

.. code-block:: bash

   pytest

License
-------

This project is licensed under the MIT License - see the License in the repository for details.