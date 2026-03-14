# Product Requirements Document: PAN-OS NGFW Configuration via Terraform

**Version:** 1.0
**Date:** 2023-10-27
**Author/Reviewer:** AI Assistant
**Status:** Draft

---

## 1. Introduction

This document outlines the requirements for a Terraform project designed to manage Palo Alto Networks PAN-OS configurations on a NGFW management server. The project leverages the official `PaloAltoNetworks/panos` Terraform provider, specifically version `2.0.0`. The goal is to provide an Infrastructure as Code (IaC) approach for defining, deploying, and managing core NGFW objects like Templates, Template Stacks, Device Groups, Policies, and associated network/security objects.

---

## 2. Goals

- **Automate Configuration:** Automate the deployment and modification of PAN-OS configurations within NGFW.
- **Consistency:** Ensure consistent configurations across different environments or device groups managed by NGFW.
- **Version Control:** Enable tracking of configuration changes through standard Git workflows.
- **Modularity:** Provide a structured approach to managing different aspects of NGFW configuration (e.g., network, security policies, objects).
- **Repeatability:** Allow for easy replication of configurations for new sites or device groups.
- **Utilize `panos` Provider v2.0.0:** Leverage the features and resource types available in version `2.0.0` of the `panos` provider.

---

## 3. Target Audience

- Network Engineers / Administrators responsible for managing Palo Alto Networks firewalls via NGFW.
- Security Engineers defining and implementing security policies.
- DevOps / Platform Engineers integrating network infrastructure management into IaC workflows.
- Users familiar with both Terraform and PAN-OS NGFW concepts (Templates, Device Groups, Shared vs. DG/Template scope).

---

## 4. Requirements

### 4.1. Functional Requirements

The system MUST provide the capability to define and manage the following NGFW configuration elements using Terraform:

- **FR-01: Provider Configuration:**
  - MUST allow configuration of connection details to the target NGFW instance (hostname, username, password) via Terraform variables.
  - MUST explicitly require and use the `PaloAltoNetworks/panos` provider version `2.0.0`.
- **FR-02: Location Targeting:**
  - MUST utilize the `location` attribute within `panos` provider resources to target configuration deployment to the correct scope within NGFW (e.g., Shared, specific Device Group, specific Template, specific Template Stack, NGFW System).
- **FR-03: Templates & Template Stacks:**
  - MUST allow creation and management of NGFW Templates (e.g., `panos_template`).
  - MUST allow creation and management of NGFW Template Stacks (e.g., `panos_template_stack`), including assignment of Templates and devices.
- **FR-04: Device Groups & Hierarchy:**
  - MUST allow creation and management of NGFW Device Groups (e.g., `panos_device_group`), including device assignment.
  - MUST allow configuration of the Device Group hierarchy (parent/child relationships) (e.g., `panos_device_group_parent`).
- **FR-05: Network Configuration (within Templates):**
  - MUST allow configuration of DNS settings (e.g., `panos_dns_settings`) at both NGFW System and Template levels.
  - MUST allow configuration of NTP settings (e.g., `panos_ntp_settings`) at both NGFW System and Template levels.
  - MUST allow configuration of Interface Management Profiles (e.g., `panos_interface_management_profile`).
  - MUST allow definition of Template Variables (e.g., `panos_template_variable`).
  - MUST allow configuration of Ethernet Interfaces (e.g., `panos_ethernet_interface`), including Layer 3 settings (DHCP, static IPs, management profiles) and referencing Template Variables.
  - MUST allow configuration of Loopback Interfaces (e.g., `panos_loopback_interface`).
  - MUST allow configuration of Security Zones (e.g., `panos_zone`) and association with interfaces.
  - MUST allow configuration of Virtual Routers (e.g., `panos_virtual_router`), including interface assignment and static routes.
- **FR-06: Object Management (within Device Groups):**
  - MUST allow creation and management of Administrative Tags (e.g., `panos_administrative_tag`).
  - MUST allow creation and management of Address Objects (IP Netmask, IP Range, FQDN) (e.g., `panos_addresses`) with associated tags.
  - MUST allow creation and management of Address Groups (Static and Dynamic) (e.g., `panos_address_group`) with associated tags.
  - MUST allow creation and management of Service Objects (TCP/UDP) (e.g., `panos_service`) with associated tags.
  - MUST allow creation and management of Service Groups (e.g., `panos_service_group`) with associated tags.
  - MUST allow creation and management of Custom URL Categories (e.g., `panos_custom_url_category`).
- **FR-07: Security Policy Management (within Device Groups):**
  - MUST allow creation and management of Security Policy rules (e.g., `panos_security_policy`) within a specified Device Group and rulebase (e.g., pre-rulebase).
  - MUST support defining rule components: name, source/destination zones/addresses, applications, services, action, logging, tags.
- **FR-08: Variable-Driven Configuration:**
  - MUST use Terraform input variables (`variables.tf`) and a variable definitions file (`terraform.tfvars`) to drive the configuration of all managed resources.
  - Variable structure SHOULD logically map to the resource types being configured.
- **FR-09: Dependency Management:**
  - MUST correctly utilize Terraform's implicit and explicit (`depends_on`) dependency management to ensure resources are created/updated in the required order (e.g., Template before Template Stack, Objects before Policies).
- **FR-10: Outputs:**
  - MUST output key identifiers of created resources (e.g., Template names, Device Group names, Zone names, Service names, Security Rules) for potential use in other processes or for verification.

### 4.2. Non-Functional Requirements

- **NFR-01: Maintainability:** The Terraform code MUST be structured logically with comments to enhance readability and ease of maintenance. Resource definitions SHOULD be grouped by function (e.g., Templates, Device Groups, Objects).
- **NFR-02: Configurability:** The project MUST be highly configurable through the `terraform.tfvars` file, allowing adaptation to different NGFW environments and requirements without code changes in `main.tf`.
- **NFR-03: Idempotency:** Leveraging Terraform core functionality, applying the configuration multiple times MUST result in the same desired state in NGFW.
- **NFR-04: Usability:** The project MUST include a README file explaining prerequisites, setup, core concepts (like `location`), configuration structure, and basic usage commands (`init`, `plan`, `apply`).

### 4.3. Technical Requirements

- **TR-01:** Terraform `v1.5.0` or later MUST be used.
- **TR-02:** `PaloAltoNetworks/panos` provider version `2.0.0` MUST be used.
- **TR-03:** Valid NGFW credentials with sufficient permissions to create/modify the targeted objects MUST be available.
- **TR-04:** Network connectivity MUST exist between the machine running Terraform and the NGFW appliance.

---

## 5. Design and Architecture

- **Provider:** `PaloAltoNetworks/panos` `v2.0.0`.
- **Core Files:**
  - `provider.tf`: Defines required provider version and configures connection details (via variables).
  - `variables.tf`: Defines the structure and types for all input variables. Variables are organized into complex objects and maps to represent the NGFW hierarchy.
  - `terraform.tfvars`: Contains user-specific values for the variables defined in `variables.tf`. This file drives the entire configuration.
  - `main.tf`: Contains the resource definitions for all managed NGFW objects. Resources leverage variables from `terraform.tfvars` and use the `location` attribute extensively. Explicit `depends_on` blocks are used where necessary. Resources are grouped logically using comments.
  - `outputs.tf`: Defines outputs for key resource attributes.
  - `README.md`: User documentation.
- **Key Concepts:**
  - **Variable-Driven:** All resource attributes are parameterized using variables.
  - **Location Attribute:** The `location` block within each resource is critical for specifying _where_ in the NGFW hierarchy (Shared, DG, Template, etc.) the configuration should be applied.
  - **Hierarchical Configuration:** The `terraform.tfvars` structure mirrors the NGFW hierarchy (e.g., defining objects within a specific Device Group map key).
  - **Explicit Dependencies:** `depends_on` is used to enforce creation order where Terraform cannot implicitly determine it (e.g., ensuring a Device Group exists before adding objects to it).

---

## 6. Usage Workflow

1.  Clone the repository/project.
2.  Copy `terraform.tfvars.example` to `terraform.tfvars`.
3.  Modify `terraform.tfvars` with environment-specific details (NGFW credentials, desired object names, IPs, etc.), following the structure defined in `variables.tf`.
4.  Run `terraform init` to initialize the provider.
5.  Run `terraform plan` to preview the changes that will be made to NGFW.
6.  Review the plan carefully.
7.  Run `terraform apply` to apply the configuration changes to NGFW.
8.  **(Manual Step)** Log in to NGFW and perform a Commit operation to push the candidate configuration to managed firewalls.

---

## 7. Limitations & Known Issues (Based on provided files)

- **Provider State:** The `panos` provider `v2.0.0` might still be considered relatively new or potentially have limitations compared to more mature providers (as noted "alpha state" in the original README, although v2.0.0 is a GA release, caution might still be warranted).
- **No Commit:** The Terraform configuration only modifies the _candidate_ configuration on NGFW. A manual commit operation within the NGFW UI is required to make the changes live on managed devices. This Terraform project does _not_ automate the commit process.
- **Resource Coverage:** While extensive, the project may not cover _all_ possible PAN-OS objects or attributes available in the `panos` `v2.0.0` provider.
- **Potential Bugs:** A commented-out section in `main.tf` regarding `panos_ethernet_interface` override indicates a potential issue or complexity with template stack overrides for that specific resource at the time the code was written (`plugin6.(*GRPCProvider).ApplyResourceChange request was cancelled`).

---

## 8. Future Considerations (Optional)

- Integrate with a commit automation solution (e.g., using `panos-python-sdk` in a separate script triggered after `terraform apply`).
- Expand resource coverage to include other PAN-OS features (e.g., NAT Policies, QoS, VPNs, User-ID).
- Implement Terratest for automated validation of deployed configurations.
- Develop modules for reusable components (e.g., a standard branch template/DG module).
- Improve error handling and input validation.

---

## 9. Document History

- **v1.0 (2023-10-27):** Initial draft based on provided Terraform project files.
