# Product Requirements Document: Panorama Address Object Creator

**Version:** 1.0
**Date:** 2024-02-29
**Author:** [Your Name/Team Name]
**Status:** Draft

---

## 1. Introduction

This document outlines the requirements for the "Panorama Address Object Creator," a Python tool designed to automate the creation of Address Objects on a Palo Alto Networks Panorama appliance. The tool will leverage the `pan-os-python` library (version 1.12.1) to interact with the Panorama API, streamlining network configuration tasks, reducing manual errors, and enabling programmatic infrastructure management.

## 2. Goals and Objectives

- **Automate Provisioning:** Eliminate the need for manual creation of Address Objects via the Panorama GUI or CLI.
- **Improve Efficiency:** Significantly reduce the time required to provision multiple Address Objects.
- **Ensure Consistency:** Apply Address Objects consistently according to defined input data, reducing typos and configuration drift.
- **Reduce Errors:** Minimize human error associated with manual data entry.
- **Provide Programmatic Interface:** Enable integration into larger automation workflows or scripts.
- **Utilize Modern Python Stack:** Build upon the specified technology stack (Python 3.10-3.12, Pydantic 2.11, `pan-os-python` 1.12.1).

## 3. Target Audience

- Network Administrators / Engineers managing Palo Alto Networks firewalls via Panorama.
- Security Operations (SecOps) teams needing to quickly update network objects.
- Infrastructure Automation Engineers integrating network changes into pipelines.

## 4. Scope

**In Scope (Version 1.0):**

- Connect securely to a specified Panorama appliance using an API key.
- Read a list of Address Objects to be created from a structured input file (e.g., JSON or YAML).
- Support creation of **IP Netmask** type Address Objects (e.g., `192.168.1.1/32`, `10.0.0.0/8`).
- Validate input data format using Pydantic (e.g., valid IP/mask format, required fields present).
- Check if an Address Object with the same name already exists on Panorama _before_ attempting creation. Skip creation if it exists, log a warning.
- Create the specified Address Objects on Panorama within a designated Device Group (configurable).
- Perform a `commit` operation on Panorama to apply the created objects. Making the commit optional via a flag is desirable.
- Provide clear logging output indicating success/failure for each object and the overall commit status.
- Basic error handling for connection issues, authentication failures, API errors, and commit failures.
- Configuration of Panorama connection details (hostname, API key) via environment variables or a configuration file.

**Out of Scope (Version 1.0):**

- Modifying existing Address Objects.
- Deleting Address Objects.
- Creating other Address Object types (e.g., FQDN, IP Range, IP Wildcard, Address Groups, Tags) - _Considered for future versions_.
- Advanced validation (e.g., checking for overlapping subnets).
- Direct interaction with individual firewalls (managed via Panorama only).
- Graphical User Interface (GUI).
- Complex workflow orchestration (e.g., multi-stage approvals).
- Support for username/password authentication (API Key is preferred for security and automation).
- Pushing configuration selectively to specific Device Groups during the commit (Commit will be Panorama-wide initially, or targeted to the DG where objects are created if API allows easily).

## 5. Functional Requirements

|  ID  | Requirement                  | Description                                                                                                                                                                                          |  Priority  | Notes                                                                               |
| :--: | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: | :---------------------------------------------------------------------------------- |
| FR1  | Panorama Connection          | The tool must connect to the specified Panorama appliance using its hostname/IP address and a valid API key over HTTPS.                                                                              |  **Must**  | Use `pan-os-python`'s `Panorama` class.                                             |
| FR2  | Input Data Processing        | The tool must read Address Object definitions (name, IP value/mask, description) from a specified input file (Format TBD: JSON or YAML).                                                             |  **Must**  | Leverage `Pydantic` for parsing and initial validation.                             |
| FR3  | Input Data Validation        | Input data must be validated: required fields (name, value) present, IP address/netmask format is valid. Description field is optional.                                                              |  **Must**  | Pydantic models enforce structure and basic types. Add custom validators if needed. |
| FR4  | Pre-Creation Check           | Before attempting to create an object, the tool must check if an object with the same `name` already exists in the target Device Group on Panorama.                                                  |  **Must**  | Use `pan-os-python` find/refresh methods.                                           |
| FR5  | Address Object Creation      | For each valid and non-existent object definition, the tool must use `pan-os-python` to create an `AddressObject` of type 'ip-netmask' on Panorama in the specified Device Group.                    |  **Must**  | Use `panorama.objects.AddressObject` and `create()` methods.                        |
| FR6  | Handle Existing Objects      | If an object with the same name already exists (as per FR4), the tool must skip creation for that specific object and log a clear warning message.                                                   |  **Must**  | Do not error out the entire process.                                                |
| FR7  | Panorama Commit              | After attempting to create all objects, the tool must trigger a `commit` operation on Panorama to make the configuration changes live.                                                               |  **Must**  | Use `panorama.commit()` method.                                                     |
| FR8  | Optional Commit Flag         | Provide a command-line flag (e.g., `--no-commit` or `--commit`) to control whether the commit operation (FR7) is performed. Default should be to commit.                                             | **Should** | Allows for staging changes without immediate application.                           |
| FR9  | Configuration Management     | Panorama hostname, API key, and target Device Group must be configurable via environment variables or a dedicated configuration file (e.g., `config.yaml`).                                          |  **Must**  | Avoid hardcoding credentials. Document precedence (e.g., Env > Config File).        |
| FR10 | Execution Feedback / Logging | The tool must provide console output logging: Connection attempt/success/failure, file reading, validation results, object creation success/skip/failure (per object), commit start/success/failure. |  **Must**  | Use Python's standard `logging` module.                                             |

## 6. Non-Functional Requirements

| ID   | Requirement     | Description                                                                                                                                                                 |  Priority  | Notes                                                                                      |
| :--- | :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: | :----------------------------------------------------------------------------------------- |
| NFR1 | Security        | API keys must not be stored in source code. Configuration files containing sensitive info must have appropriate permissions. Use HTTPS.                                     |  **Must**  | Recommend environment variables or secure vault integration for production.                |
| NFR2 | Reliability     | The tool should handle common exceptions gracefully (e.g., network timeouts, invalid API key, Panorama API errors, commit failures) and provide informative error messages. |  **Must**  | Exit codes should indicate overall success (0) or failure (non-zero).                      |
| NFR3 | Usability (CLI) | The tool should be invokable from the command line with clear arguments (e.g., path to input file, optional flags). Provide `--help` output.                                |  **Must**  | Consider using libraries like `argparse` or `typer`.                                       |
| NFR4 | Maintainability | Code must adhere to PEP 8 standards, be formatted with `ruff`, linted with `flake8`, and include type hints validated by `mypy`. Use specified dependencies.                |  **Must**  | Follows user-provided dev dependencies. Include docstrings for key functions/classes.      |
| NFR5 | Performance     | The tool should be reasonably performant for creating batches of ~100 objects. Performance is largely dependent on Panorama responsiveness.                                 | **Should** | Focus on correctness first. Optimize API calls if necessary (e.g., batching if supported). |
| NFR6 | Logging         | Implement configurable log levels (e.g., INFO, DEBUG, WARNING, ERROR). Log detailed API interactions at DEBUG level.                                                        |  **Must**  | Log to console by default, optionally to a file.                                           |

## 7. Data Requirements

### Input Data Model

A Pydantic model defining the structure for a single address object:

```python
# Example Pydantic Model
from pydantic import BaseModel, Field, IPvAnyNetwork
from typing import Optional

class AddressObjectInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=63, pattern=r'^[a-zA-Z0-9_.-]+$') # PAN-OS limits & typical valid chars
    value: IPvAnyNetwork # Validates IP/Mask format e.g., "192.168.1.1/32" or "10.0.0.0/8"
    description: Optional[str] = Field(None, max_length=255) # PAN-OS limit
```

### Input File Format

A list of `AddressObjectInput` objects, likely in JSON or YAML format. (Decision required: Prefer JSON for simplicity, YAML for readability/comments).

- _Example (JSON):_
  ```json
  [
    {
      "name": "Server_Prod_1",
      "value": "10.1.1.10/32",
      "description": "Production Server 1 Primary IP"
    },
    {
      "name": "Mgmt_Network",
      "value": "192.168.100.0/24",
      "description": "Management Subnet"
    },
    {
      "name": "Invalid-Name-Example!",
      "value": "1.1.1.1/32"
    },
    {
      "name": "Valid_But_No_Desc",
      "value": "8.8.8.8/32"
    }
  ]
  ```

### Configuration Data

- `PANORAMA_HOSTNAME`: FQDN or IP address of Panorama.
- `PANORAMA_API_KEY`: API Key for authentication.
- `PANORAMA_DEVICE_GROUP`: Target Device Group name (e.g., "shared" or a specific DG).

## 8. Error Handling

- **Connection Error:** Log error, exit with non-zero code.
- **Authentication Error:** Log error (masking key details), exit with non-zero code.
- **Input File Not Found/Readable:** Log error, exit with non-zero code.
- **Input Data Validation Error:** Log specific validation error (field, value, reason). _Recommendation: Report all validation errors found in the input file, then exit with non-zero code._
- **Object Already Exists:** Log warning, skip creation for that object, continue processing next object.
- **PAN-OS API Error during Creation:** Log detailed error from `pan-os-python` for the specific object. _Recommendation: Log failure and continue with the next object._
- **Commit Failure:** Log detailed error from `pan-os-python`, exit with non-zero code.

## 9. Technology Stack

- **Programming Language:** Python (Versions 3.10 - 3.12)
- **Core Libraries:**
  - `pan-os-python`: 1.12.1 (For Panorama interaction)
  - `pydantic`: 2.11 (For data validation and modeling)
- **Development Tooling:**
  - `ruff`: Code formatting & Fast Linting (Can potentially replace Flake8)
  - `flake8`: Linting (If Ruff doesn't cover all desired checks)
  - `mypy`: Static type checking
  - `ipython`: Enhanced interactive shell (for development/debugging)

_(Note: `ruff` can often replace `flake8` entirely. Confirm if both are strictly needed.)_

## 10. Future Considerations / Roadmap (Post V1.0)

- Support for other Address Object types (FQDN, Range, Wildcard, etc.).
- Support for Address Groups.
- Ability to add Tags to objects during creation.
- Option to modify/update existing objects based on input data.
- Option to delete objects based on input data or a separate list.
- Support for CSV input format.
- "Dry Run" mode to show what changes _would_ be made without creating/committing.
- More granular commit options (e.g., commit only specific device group changes if supported by API).
- Integration with secrets management systems (e.g., HashiCorp Vault, AWS Secrets Manager).

## 11. Open Questions

- Confirm preferred input file format: **JSON** or **YAML**? (_Recommendation: JSON for simplicity, YAML for comments/readability_).
- Default behavior for commit: Commit by default (`--no-commit` flag to disable) or require explicit commit (`--commit` flag to enable)? (_Recommendation: Commit by default for simpler common use case_).
- Behavior on input validation error: Fail fast on first error, or report all validation errors then exit, or skip invalid entries and continue? (_Recommendation: Report all validation errors then exit_).
- Behavior on API error during _single_ object creation: Halt entire process or log error for that object and continue with others? (_Recommendation: Log error and continue_).
- Specify exact structure/naming for configuration file if chosen over/alongside environment variables (e.g., `config.yaml` with keys `panorama_hostname`, `api_key`, `device_group`).
- Clarify Ruff vs Flake8 usage: Is Ruff intended to replace Flake8, or are they used together for different checks?

## 12. Success Metrics

- Successful creation of Address Objects on Panorama using the tool, verified via Panorama UI/API.
- Reduction in time spent by administrators creating objects manually (measured via qualitative feedback or time estimates).
- Adoption rate by the target Network/SecOps/Automation teams.
- Number of successful end-to-end script executions vs. executions ending in failure (tracked via logs or run statistics).
