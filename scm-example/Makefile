.PHONY: help init plan apply destroy validate fmt clean

help:
	@echo "Available targets:"
	@echo "  init      - Initialize Terraform working directory"
	@echo "  validate  - Validate Terraform configuration"
	@echo "  fmt       - Format Terraform files"
	@echo "  plan      - Generate and show execution plan"
	@echo "  apply     - Apply the Terraform configuration"
	@echo "  destroy   - Destroy all managed infrastructure"
	@echo "  clean     - Remove Terraform state and cache files"

init:
	terraform init

validate: init
	terraform validate

fmt:
	terraform fmt -recursive

plan: validate
	terraform plan

apply: validate
	terraform apply

destroy:
	terraform destroy

clean:
	rm -rf .terraform/
	rm -f .terraform.lock.hcl
	rm -f terraform.tfstate*
	rm -f *.tfplan
