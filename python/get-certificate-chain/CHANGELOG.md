# CHANGELOG

## 2023-04-19

### Version 0.1.7

* --get-ca-cert-pem now default to prevent issues where certificate did not have AIA.

### Version 0.1.6

* run method now returns a dictionary of the certificate chain files

### Version 0.1.5

* Refactored the normalize_subject method to use a list comprehension.
* Changed the check_url method to a static method since it doesn't use instance variables.

### Version 0.1.4

* change `--url` to `--host` to align with TLS spec
* added `--output-dir` to allow for custom output directory
* added `--log-level` to allow for custom logging level
* fixed optional `--get-ca-cert-pem` and `--rm-ca-files` from continuing the full script after execution

## 2023-04-18

### Version 0.1.3

* renamed script to `download` to help with imports
* parse_args now uses strong typing
* added exceptions for urllib errors
* removed remaining print statements
* relax on python version requirements
* change `--domain` to `--url` to allow for more flexibility

## 2023-04-17

### Version 0.1.2

* added CLI support
* added screenshots to documentation

### Version 0.1.1

* moved functionality into a class to allow for easier import into other scripts
* support for passing a dictionary or argparse object into the class
* updated tests to reflect changes
* updated documentation to reflect changes
* added screenshots to documentation

## 2023-04-16

### Version 0.1.0

* Custom fork of [getCertificateChain](https://github.com/TheScriptGuy/getCertificateChain)
* Complete refactor of code to use more pythonic style
* Prepare script for pypi release

## 2023-03-20

### Version 0.04

* Fixing bug [MitM proxy/ssl decrypt](https://github.com/TheScriptGuy/getCertificateChain/issues/5)

### Version 0.03

* Enhancement request [adding Root Found output](https://github.com/TheScriptGuy/getCertificateChain/issues/2)

### Version 0.02

* Fixing bug [deprecation warning](https://github.com/TheScriptGuy/getCertificateChain/issues/1)

## 2023-03-12

### Version 0.01

* First release.
