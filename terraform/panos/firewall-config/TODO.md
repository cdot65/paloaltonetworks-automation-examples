# TODO List: Building PAN-OS NGFW Terraform Configuration

This list outlines the steps required to create the Terraform project for managing NGFW configurations using the `panos` provider v2.0.0.

## Phase 1: Project Setup & Initialization

- [ ] Create a new project directory.
- [ ] Initialize a Git repository (`git init`).
- [ ] Create the core Terraform files:
  - [ ] `provider.tf`
  - [ ] `variables.tf`
  - [ ] `main.tf`
  - [ ] `outputs.tf`
  - [ ] `terraform.tfvars.example`
  - [ ] `README.md`
- [ ] Create a `.gitignore` file and add standard Terraform entries (`.terraform/`, `*.tfstate`, `*.tfstate.*`, `crash.log`, `*.tfvars` - _Note: Users must manage their own `terraform.tfvars` securely_).
- [ ] Ensure Terraform v1.5.0+ is installed locally.

## Phase 2: Provider and Variable Configuration

- [ ] **Provider Definition (`provider.tf`):**
  - [ ] Define the `required_providers` block specifying `PaloAltoNetworks/panos` version `2.0.0`.
  - [ ] Define the `provider "panos"` block.
  - [ ] Configure provider arguments (`hostname`, `username`, `password`) to reference input variables.
- [ ] **Core Variables (`variables.tf`):**
  - [ ] Define the `ngfw` input variable (object type) for connection details.
  - [ ] Define the variable structure for `dns_settings` (map of objects).
  - [ ] Define the variable structure for `ntp_settings` (map of objects).
  - [ ] Define the variable structure for `templates` (map of objects).
  - [ ] Define the variable structure for `template_stacks` (map of objects).
  - [ ] Define the variable structure for `interface_management_profiles` (map of objects).
  - [ ] Define the variable structure for `template_variables` (map of objects).
  - [ ] Define the variable structure for `ethernet_interfaces` (map of objects).
  - [ ] Define the variable structure for `loopback_interfaces` (map of objects).
  - [ ] Define the variable structure for `zones` (map of objects).
  - [ ] Define the variable structure for `virtual_routers` (map of objects).
  - [ ] Define the variable structure for `device_groups` (map of objects).
  - [ ] Define the variable structure for `device_group_parents` (map of objects).
  - [ ] Define the variable structure for `administrative_tags` (map of objects).
  - [ ] Define the variable structure for `addresses` (map of objects containing a map).
  - [ ] Define the variable structure for `address_groups` (map of objects containing a map).
  - [ ] Define the variable structure for `services` (map of objects containing a map).
  - [ ] Define the variable structure for `service_groups` (map of objects containing a map).
  - [ ] Define the variable structure for `security_policies` (map of objects containing a list).
  - [ ] Define the variable structure for `custom_url_categories` (map of objects containing a map).
- [ ] **Example Values (`terraform.tfvars.example`):**
  - [ ] Populate `terraform.tfvars.example` with sample values matching the structure defined in `variables.tf` for all variables. Use placeholders for sensitive data.

## Phase 3: Resource Implementation (`main.tf`)

_(Ensure `location` blocks and `depends_on` clauses are added appropriately for each resource)_

- [ ] **System/Shared Settings:**
  - [ ] Implement `panos_dns_settings` resource(s) for NGFW System and Template(s), referencing `var.dns_settings`.
  - [ ] Implement `panos_ntp_settings` resource(s) for NGFW System and Template(s), referencing `var.ntp_settings`.
- [ ] **Templates & Template Stacks:**
  - [ ] Implement `panos_template` resource(s), referencing `var.templates`.
  - [ ] Implement `panos_template_stack` resource(s), referencing `var.template_stacks` and depending on relevant `panos_template`.
- [ ] **Template Network Configuration:**
  - [ ] Implement `panos_interface_management_profile` resource(s) within Template scope, referencing `var.interface_management_profiles`.
  - [ ] Implement `panos_template_variable` resource(s) within Template scope, referencing `var.template_variables`.
  - [ ] Implement `panos_ethernet_interface` resource(s) within Template scope, referencing `var.ethernet_interfaces` and related variables/profiles.
  - [ ] Implement `panos_loopback_interface` resource(s) within Template scope, referencing `var.loopback_interfaces`.
  - [ ] Implement `panos_zone` resource(s) within Template scope, referencing `var.zones` and associated interfaces.
  - [ ] Implement `panos_virtual_router` resource(s) within Template scope, referencing `var.virtual_routers` and associated interfaces/zones.
- [ ] **Device Groups & Hierarchy:**
  - [ ] Implement `panos_device_group` resource(s), referencing `var.device_groups`.
  - [ ] Implement `panos_device_group_parent` resource(s), referencing `var.device_group_parents` and depending on relevant `panos_device_group`.
- [ ] **Device Group Objects:**
  - [ ] Implement `panos_administrative_tag` resource(s) within Device Group scope, referencing `var.administrative_tags`.
  - [ ] Implement `panos_addresses` resource(s) within Device Group scope, referencing `var.addresses` and depending on relevant tags/DG.
  - [ ] Implement `panos_address_group` resource(s) within Device Group scope, referencing `var.address_groups` and depending on relevant addresses/tags/DG.
  - [ ] Implement `panos_service` resource(s) within Device Group scope, referencing `var.services` and depending on relevant tags/DG.
  - [ ] Implement `panos_service_group` resource(s) within Device Group scope, referencing `var.service_groups` and depending on relevant services/tags/DG.
  - [ ] Implement `panos_custom_url_category` resource(s) within Device Group scope, referencing `var.custom_url_categories`.
- [ ] **Device Group Policies:**
  - [ ] Implement `panos_security_policy` resource(s) within Device Group scope (pre-rulebase), referencing `var.security_policies` and depending on relevant zones, objects, services, tags, DGs.

## Phase 4: Outputs and Documentation

- [ ] **Outputs (`outputs.tf`):**
  - [ ] Define outputs for key created resources (e.g., template names, stack names, device group names, zone names, service names, policy rule details) by referencing attributes from the resources defined in `main.tf`.
- [ ] **Documentation (`README.md`):**
  - [ ] Write overview section.
  - [ ] List prerequisites (Terraform version, Provider version, NGFW access).
  - [ ] Detail getting started steps (cloning, `terraform.tfvars` setup, basic commands).
  - [ ] Explain the configuration structure (`main.tf`, `variables.tf`, `terraform.tfvars`).
  - [ ] Explain core concepts, emphasizing the `location` attribute and dependency order.
  - [ ] Provide clear usage instructions (`init`, `plan`, `apply`).
  - [ ] Document the variable structure expected in `terraform.tfvars` with examples.
  - [ ] Explain how to make changes (modify `terraform.tfvars`, plan, apply).
  - [ ] List known limitations (e.g., manual commit required, provider state).
  - [ ] Add a section for contributing (optional).

## Phase 5: Testing and Refinement

- [ ] Run `terraform fmt` to ensure code formatting consistency.
- [ ] Run `terraform validate` to check syntax.
- [ ] Create a personal `terraform.tfvars` file (not committed to Git) with valid credentials and test configuration values.
- [ ] Run `terraform plan` against a test NGFW instance/vsys. Review the plan carefully.
- [ ] Run `terraform apply` against the test NGFW instance. Verify resource creation in NGFW UI.
- [ ] **(Manual Step)** Perform a `Commit` operation within the NGFW UI to validate the configuration applies without errors.
- [ ] Test modifications: Change values in `terraform.tfvars`, run `plan` and `apply` again, verify changes in NGFW, and perform another manual `Commit`.
- [ ] Run `terraform destroy` against the test instance and verify resource removal.
- [ ] Refine variable structures, resource definitions, and documentation based on testing results.
- [ ] Iterate through testing steps until the configuration is stable and correct.
