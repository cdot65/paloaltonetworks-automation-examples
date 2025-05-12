# PRD: Terraform Provisioning for Strata Cloud Manager (SCM)

## 1. Introduction

### 1.1 Overview

This document outlines the requirements for a project to leverage the `scm` Terraform provider for provisioning and managing resources within Strata Cloud Manager (SCM). The goal is to implement Infrastructure as Code (IaC) principles for SCM configuration, enabling automated, consistent, and version-controlled deployments.

By adopting Terraform, we aim to move away from manual configuration via the SCM UI or ad-hoc scripting, reducing errors, improving repeatability, and integrating SCM configuration into our existing infrastructure deployment workflows.

### 1.2 Goals and Objectives

*   **Primary Goal:** Successfully provision and manage core SCM resources using Terraform.
*   **Objective 1:** Define and implement Terraform modules for frequently used SCM resource types.
*   **Objective 2:** Establish a version-controlled repository for SCM Terraform code.
*   **Objective 3:** Enable consistent deployment of SCM configurations across different environments (e.g., development, staging, production).
*   **Objective 4:** Reduce the time and effort required for initial SCM setup and ongoing configuration changes.
*   **Objective 5:** Improve auditability and traceability of SCM configuration changes.

### 1.3 Dependencies

*   Access to a Strata Cloud Manager tenant.
*   Necessary API credentials for the `scm` provider with appropriate permissions.
*   Terraform installed and configured.
*   Access to a remote state backend (e.g., S3, GCS, Azure Blob Storage, Terraform Cloud).
*   Familiarity with Terraform concepts and practices.

## 2. Scope

### 2.1 In Scope

The initial phase of this project will focus on enabling provisioning for the following core SCM resource types using the `scm` Terraform provider:

*   `scm_address_object`
*   `scm_address_group`
*   `scm_service_object`
*   `scm_service_group`
*   `scm_security_rule`
*   `scm_security_rule_group`
*   `scm_vpn_ike_gateway`
*   `scm_vpn_ipsec_tunnel`
*   `scm_vulnerability_protection_profile`
*   `scm_url_access_profile`
*   `scm_file_blocking_profile`
*   `scm_anti_spyware_profile`
*   `scm_anti_virus_profile`
*   `scm_wildfire_anti_virus_profile`
*   `scm_decryption_profile`
*   `scm_dos_protection_profile`
*   `scm_qos_profile`
*   `scm_schedule`

*(**Note:** This list should be refined based on your organization's immediate needs. Prioritize the most critical or frequently changed resources.)*

The project will include:

*   Creation of a dedicated Git repository for the SCM Terraform code.
*   Structuring the repository with appropriate directories (e.g., `modules/`, `environments/`, `examples/`).
*   Implementing reusable Terraform modules for the in-scope resource types where appropriate.
*   Defining variable inputs for module configurations to allow for environment-specific settings.
*   Configuring the `scm` provider within the Terraform code.
*   Implementing secure methods for provider authentication (e.g., via environment variables, secrets management).
*   Setting up and documenting the remote state backend configuration.
*   Providing basic examples demonstrating how to use the modules and deploy common configurations.

### 2.2 Out of Scope

The following are explicitly out of scope for this initial phase:

*   Provisioning SCM infrastructure elements not listed in the In Scope section (e.g., specific integrations not covered by the provider, advanced reporting configurations).
*   Managing licenses or subscriptions within SCM via Terraform (unless explicitly supported by the provider and added to scope).
*   Automated migration of *existing* manual SCM configurations into Terraform state (focus is on managing future configurations or greenfield deployments).
*   Full integration into a CI/CD pipeline (this may be a future phase).
*   Developing custom tooling beyond standard Terraform workflows (e.g., custom plan/apply wrappers beyond simple scripts).
*   Extensive testing infrastructure setup (basic validation and testing against a development SCM tenant are included).

## 3. Target Audience

The primary users of this project's output (the Terraform code and documentation) will be:

*   DevOps Engineers
*   Site Reliability Engineers (SREs)
*   Network Engineers
*   Cloud Infrastructure Teams

These users are expected to have a working understanding of Terraform concepts and command-line usage.

## 4. User Stories / Use Cases

Here are some example user stories illustrating how the target audience will use this project:

*   **As a DevOps Engineer**, I want to define a standard set of security rules for a new application environment so that security policies are consistently applied.
*   **As a Network Engineer**, I want to quickly create and manage network objects (addresses, services) for new deployments using version-controlled code instead of the SCM UI.
*   **As an SRE**, I want to automate the setup and configuration of VPN tunnels for new site-to-site connections using IaC principles.
*   **As a Security Engineer**, I want to ensure that standard security profiles (e.g., URL filtering, anti-malware) are applied consistently across all environments managed by Terraform.
*   **As a Team Lead**, I want to have a clear, auditable history of all SCM configuration changes made via Terraform.
*   **As an Engineer deploying a new environment**, I want to be able to provision all necessary SCM configurations by running a simple `terraform apply` command specific to that environment.

## 5. Functional Requirements

The Terraform project must meet the following functional requirements:

*   **FR-1:** Ability to `terraform plan` and `terraform apply` configurations for the in-scope SCM resources.
*   **FR-2:** Ability to update existing SCM resources by modifying Terraform configuration and running `terraform apply`.
*   **FR-3:** Ability to delete SCM resources by removing their definition from Terraform configuration and running `terraform apply`.
*   **FR-4:** Organize common resource configurations into reusable Terraform modules.
*   **FR-5:** Parameterize configurations using Terraform variables to support different environments and configurations.
*   **FR-6:** Securely handle SCM provider authentication credentials (e.g., API keys, tokens) without embedding them directly in the code.
*   **FR-7:** Support state management using a configured remote backend.
*   **FR-8:** Provide clear input and output variables for modules and root configurations.
*   **FR-9:** Include examples demonstrating the usage of core modules and common deployment patterns.
*   **FR-10:** Validate Terraform code correctness using `terraform validate` and format using `terraform fmt`.

## 6. Non-Functional Requirements

The project output must meet the following non-functional requirements:

*   **NFR-1 (Reliability):** The Terraform code should consistently apply the desired state when executed against the SCM API.
*   **NFR-2 (Maintainability):** The codebase should be well-structured, documented, and easy for the target audience to understand and modify.
*   **NFR-3 (Security):** SCM API credentials and other sensitive information must be handled securely (e.g., not stored in plain text in the repository or state file). The chosen authentication method must align with organizational security policies.
*   **NFR-4 (Usability):** Modules and root configurations should be intuitive to use, with clear documentation on inputs and outputs.
*   **NFR-5 (Testability):** The code structure should facilitate testing, ideally allowing for integration tests against a non-production SCM environment.
*   **NFR-6 (Performance):** Terraform operations (`plan`, `apply`) should complete within a reasonable timeframe, although performance is heavily dependent on the complexity of the configuration and the SCM API responsiveness.
*   **NFR-7 (Scalability):** The architecture should support managing a growing number of SCM resources and potentially multiple environments without significant re-architecture.

## 7. Technical Design (Overview)

*   **Repository Structure:** A standard Terraform project structure will be used, potentially including `modules/` (for reusable components), `environments/` (for environment-specific configurations), and `examples/` (for usage demonstrations).
*   **Provider Configuration:** The `scm` provider will be configured, likely specifying a version constraint. Authentication will leverage provider-specific methods, prioritizing environment variables or integration with a secrets manager over hardcoding.
*   **State Management:** A remote backend (e.g., Terraform Cloud, AWS S3, Azure Blob Storage, GCP GCS) will be configured to store the Terraform state file securely and enable collaboration. State locking will be enabled.
*   **Modules:** Reusable modules will be created for logical groupings of SCM resources (e.g., a `security_policy` module, a `network_objects` module).
*   **Variables:** Input variables will be used extensively to make configurations flexible and environment-aware. Sensitive variables will be marked as `sensitive`.
*   **Tooling:** Standard Terraform CLI commands (`init`, `validate`, `fmt`, `plan`, `apply`, `destroy`) will be the primary interface. Integration with linters (e.g., tflint) and security scanners (e.g., tfsec) will be considered.

*(**Note:** A separate, detailed technical design document may be created to elaborate on the repository structure, module design patterns, variable naming conventions, state management strategy, and specific authentication methods.)*

## 8. Open Questions / Decisions Needed

*   What is the exact list of SCM resource types required for the Minimum Viable Product (MVP)?
*   What is the preferred method for authenticating the `scm` provider (e.g., specific environment variables, integration with a secrets manager like HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)?
*   Which remote backend will be used for Terraform state?
*   What is the strategy for managing multiple SCM tenants/environments (e.g., separate state files per environment, Terraform workspaces)?
*   What level of testing (e.g., local `validate`, integration tests against a dev tenant) is required before merging code?
*   What are the naming conventions for resources, modules, and variables?

## 9. Future Considerations / Roadmap

*   Integration with CI/CD pipelines for automated plan and apply workflows.
*   Expanding the scope to include more SCM resource types as needed.
*   Implementing automated testing beyond basic validation.
*   Developing tooling or scripts to assist with state migration or management (if necessary).
*   Implementing drift detection mechanisms.
*   Adding support for advanced SCM features or services via Terraform.

## 10. Definition of Done

A requirement or user story is considered "Done" when:

*   The necessary Terraform code has been written and passes `terraform validate` and `terraform fmt`.
*   The code successfully applies the desired configuration using `terraform apply` in a designated testing environment.
*   The code has been reviewed by at least one other team member.
*   Relevant documentation (e.g., module READMEs, examples) has been created or updated.
*   The code has been merged into the main branch of the repository.
*   (If applicable) Automated tests for the functionality are passing.

## 11. Key Performance Indicators (KPIs)

While not traditional KPIs for a product feature, success indicators for this project could include:

*   Reduction in time taken to onboard a new application/environment requiring SCM configuration.
*   Reduction in manual configuration errors related to SCM.
*   Increase in the percentage of SCM configuration managed by Terraform.
*   Positive feedback from engineers using the Terraform modules/codebase.

## 12. Appendix

### 12.1 Glossary

*   **SCM:** Strata Cloud Manager
*   **IaC:** Infrastructure as Code
*   **PRD:** Product Requirements Document
*   **Terraform:** An open-source IaC tool by HashiCorp
*   **Provider:** A plugin in Terraform that interacts with an API to manage resources (e.g., `scm` provider)
*   **Resource:** An infrastructure object managed by a provider (e.g., `scm_security_rule`)
*   **Module:** A reusable, shareable package of Terraform code
*   **State:** The file where Terraform stores information about your managed infrastructure
*   **Remote Backend:** A configuration to store the state file in a shared, remote location

### 12.2 References

*   Terraform SCM Provider Documentation: [Link to the `scm` provider documentation on registry.terraform.io]
*   Strata Cloud Manager Documentation: [Link to relevant SCM documentation]
*   [Link to Technical Design Document (if separate)]
*   [Link to Repository]

---

**Document History:**

*   [Date]: Initial Draft Created
*   [Date]: Reviewed by [Name(s)]
*   [Date]: [Specific Updates/Decisions]