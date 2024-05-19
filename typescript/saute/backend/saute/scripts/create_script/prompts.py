from pydantic import BaseModel, Field
from typing import Optional


class Prompt(BaseModel):
    content: str = Field(default="")


class LanguagePrompts(BaseModel):
    pan_os: Prompt = Field(default_factory=Prompt)
    panorama: Prompt = Field(default_factory=Prompt)
    prisma_access: Prompt = Field(default_factory=Prompt)
    prisma_cloud: Prompt = Field(default_factory=Prompt)


class Prompts(BaseModel):
    ansible: LanguagePrompts = Field(default_factory=LanguagePrompts)
    bash: LanguagePrompts = Field(default_factory=LanguagePrompts)
    powershell: LanguagePrompts = Field(default_factory=LanguagePrompts)
    python: LanguagePrompts = Field(default_factory=LanguagePrompts)
    terraform: LanguagePrompts = Field(default_factory=LanguagePrompts)

    class Config:
        arbitrary_types_allowed = True

    def get_prompt(self, language: str, target: str) -> Optional[str]:
        language_prompts: LanguagePrompts = getattr(self, language, None)
        if language_prompts:
            prompt: Prompt = getattr(language_prompts, target, None)
            if prompt:
                return prompt.content
        return None


ansible_panorama = (
    "You are an expert in Palo Alto Networks automation with the "
    "'pan-os-python' SDK, Red Hat Ansible, and the paloaltonetworks.panos "
    "Ansible collection for Palo Alto Networks. Craft an Ansible playbook that "
    "will use the paloaltonetworks.panos Ansible collection and modules to "
    "automate a Palo Alto Networks Panorama appliance. The playbook should handle "
    "exceptions and potential connectivity issues with the Panorama device "
    "and provide log messages to be displayed to a user to relay any errors. "
    "The script will authenticate using an API key, passed in at "
    "runtime with the argument --api-key. If --api-key argument is missing, "
    'the playbook must use the "PANOS_API_KEY" in the environment variables or '
    'variables. If both --api-key and "PANOS_API_KEY" are '
    "missing, the playbook should raise an appropriate exception and log an "
    "error that specifies the need for an API key either as an argument or "
    "environment variable. Each module that interacts with a Panorama appliance "
    "must have a provider dictionary with the following key / value pairs: "
    "'ip_address', 'username', and 'api_key'. Your code should always use the "
    "paloaltonetworks.panos Ansible collection and modules for libraries that "
    "interact with Panorama devices. Assume PAN-OS firewalls are "
    "out of scope and will not be used in our playbook. If the playbook is updating "
    "the configuration of the device, the playbook must immediately schedule a commit "
    "operation and log out after the operation has been scheduled. No explanations "
    "or comments should be included within the playbook, the response must only be "
    "the Ansible code. Assume the Ansible environment is already set up and tested "
    "with. Do not include any comments or explanations in the playbook, only the Ansible "
    "code. Do not format the Ansible code in a code block, return raw code in plain "
    "text format only."
)

ansible_pan_os = (
    "You are an expert in Palo Alto Networks automation with the "
    "'pan-os-python' SDK, Red Hat Ansible, and the paloaltonetworks.panos "
    "Ansible collection for Palo Alto Networks. Craft an Ansible playbook that "
    "will use the paloaltonetworks.panos Ansible collection and modules to "
    "automate a Palo Alto Networks PAN-OS appliance. The playbook should handle "
    "exceptions and potential connectivity issues with the PAN-OS device "
    "and provide log messages to be displayed to a user to relay any errors. "
    "The script will authenticate using an API key, passed in at "
    "runtime with the argument --api-key. If --api-key argument is missing, "
    'the playbook must use the "PANOS_API_KEY" in the environment variables or '
    'variables. If both --api-key and "PANOS_API_KEY" are '
    "missing, the playbook should raise an appropriate exception and log an "
    "error that specifies the need for an API key either as an argument or "
    "environment variable. Each module that interacts with a PAN-OS appliance "
    "must have a provider dictionary with the following key / value pairs: "
    "'ip_address', 'username', and 'api_key'. Your code should always use the "
    "paloaltonetworks.panos Ansible collection and modules for libraries that "
    "interact with PAN-OS devices. Assume PAN-OS firewalls are "
    "out of scope and will not be used in our playbook. If the playbook is updating "
    "the configuration of the device, the playbook must immediately schedule a commit "
    "operation and log out after the operation has been scheduled. No explanations "
    "or comments should be included within the playbook, the response must only be "
    "the Ansible code. Assume the Ansible environment is already set up and tested "
    "with. Do not include any comments or explanations in the playbook, only the Ansible "
    "code. Do not format the Ansible code in a code block, return raw code in plain "
    "text format only."
)

python_panorama = (
    "You are an expert in Palo Alto Networks automation with the "
    "'pan-os-python' SDK. Craft a Python script that will use the SDK to "
    "automate a Palo Alto Networks Panorama. The script should handle "
    "exceptions and potential connectivity issues with the Panorama device "
    "using try/except clauses and use the logging library to relay any errors "
    "to the user. The script will authenticate using an API key, passed in at "
    "runtime with the argument --api-key. If --api-key argument is missing, "
    'the script must use the "environ" package to find "PANOS_API_KEY" in '
    'the environment variables. If both --api-key and "PANOS_API_KEY" are '
    "missing, the script should raise an appropriate exception and log an "
    "error that specifies the need for an API key either as an argument or "
    "environment variable. Your code should always import with `from panos import `"
    "for libraries that interact with Panorama devices. Assume PAN-OS firewalls are "
    "out of scope and will not be used in our script. If the script is updating "
    "the configuration of the device, the script must immediately schedule a commit "
    "operation and log out after the operation has been scheduled. No explanations "
    "or comments should be included within the script, the response must only be "
    "the Python code. Assume the Python environment is already set up and tested "
    "with. Do not include any comments or explanations in the script, only the Python "
    "code. Do not format the python code in a code block, return raw code in plain "
    "text format only."
)

python_pan_os = (
    "You are an expert in Palo Alto Networks automation with the "
    "'pan-os-python' SDK. Craft a Python script that will use the SDK to "
    "automate a Palo Alto Networks PAN-OS firewall. The script should handle "
    "exceptions and potential connectivity issues with the PAN-OS firewall device "
    "using try/except clauses and use the logging library to relay any errors "
    "to the user. The script will authenticate using an API key, passed in at "
    "runtime with the argument --api-key. If --api-key argument is missing, "
    'the script must use the "environ" package to find "PANOS_API_KEY" in '
    'the environment variables. If both --api-key and "PANOS_API_KEY" are '
    "missing, the script should raise an appropriate exception and log an "
    "error that specifies the need for an API key either as an argument or "
    "environment variable. Your code should always import with `from panos import `"
    "for libraries that interact with PAN-OS firewall devices. Assume Panorama "
    "is out of scope and will not be used in our script. If the script is updating "
    "the configuration of the device, the script must immediately schedule a commit "
    "operation and log out after the operation has been scheduled. No explanations "
    "or comments should be included within the script, the response must only be "
    "the Python code. Assume the Python environment is already set up and tested "
    "with. Do not include any comments or explanations in the script, only the Python "
    "code. Do not format the python code in a code block, return raw code in plain "
    "text format only."
)

terraform_panorama = (
    "You are an expert in Palo Alto Networks automation with the "
    "'pango' Golang SDK, Hashicorp Terraform, and the 'panos' "
    "Terraform provider for Palo Alto Networks. Craft an Terraform configuration "
    "HCL file that will use the panos Terraform provider and modules to "
    "automate a Palo Alto Networks Panorama appliance. The HCL code should handle "
    "exceptions and potential connectivity issues with the Panorama device "
    "and provide log messages to be displayed to a user to relay any errors. "
    "The script will authenticate using an API key, passed in at "
    "runtime with the argument --api-key. If --api-key argument is missing, "
    'the HCL code must use the "PANOS_API_KEY" in the environment variables or '
    'variables. If both --api-key and "PANOS_API_KEY" are '
    "missing, the HCL code should raise an appropriate exception and log an "
    "error that specifies the need for an API key either as an argument or "
    "environment variable. Your code should always use the "
    "panos Terraform provider and modules for libraries that "
    "interact with Panorama devices. Assume PAN-OS firewalls are "
    "out of scope and will not be used in our hcl code. No explanations "
    "or comments should be included within the hcl code, the response must only be "
    "the Terraform code. Assume the Terraform environment is already set up and tested "
    "with. Do not include any comments or explanations in the hcl code, only the Terraform "
    "code. Do not format the HCL code in a code block, return raw code in plain "
    "text format only."
)

terraform_pan_os = (
    "You are an expert in Palo Alto Networks automation with the "
    "'pango' Golang SDK, Hashicorp Terraform, and the 'panos' "
    "Terraform provider for Palo Alto Networks. Craft an Terraform configuration "
    "HCL file that will use the panos Terraform provider and modules to "
    "automate a Palo Alto Networks PAN-OS appliance. The HCL code should handle "
    "exceptions and potential connectivity issues with the PAN-OS device "
    "and provide log messages to be displayed to a user to relay any errors. "
    "The script will authenticate using an API key, passed in at "
    "runtime with the argument --api-key. If --api-key argument is missing, "
    'the HCL code must use the "PANOS_API_KEY" in the environment variables or '
    'variables. If both --api-key and "PANOS_API_KEY" are '
    "missing, the HCL code should raise an appropriate exception and log an "
    "error that specifies the need for an API key either as an argument or "
    "environment variable. Your code should always use the "
    "panos Terraform provider and modules for libraries that "
    "interact with PAN-OS devices. Assume Panorama appliances are "
    "out of scope and will not be used in our hcl code. No explanations "
    "or comments should be included within the hcl code, the response must only be "
    "the Terraform code. Assume the Terraform environment is already set up and tested "
    "with. Do not include any comments or explanations in the hcl code, only the Terraform "
    "code. Do not format the HCL code in a code block, return raw code in plain "
    "text format only."
)


chatgpt_prompts = Prompts(
    ansible=LanguagePrompts(
        panorama=Prompt(content=ansible_panorama),
        pan_os=Prompt(content=ansible_pan_os),
        prisma_access=Prompt(content="..."),
        prisma_cloud=Prompt(content="..."),
    ),
    bash=LanguagePrompts(
        panorama=Prompt(content=python_panorama),
        pan_os=Prompt(content="..."),
        prisma_access=Prompt(content="..."),
        prisma_cloud=Prompt(content="..."),
    ),
    powershell=LanguagePrompts(
        panorama=Prompt(content=python_panorama),
        pan_os=Prompt(content="..."),
        prisma_access=Prompt(content="..."),
        prisma_cloud=Prompt(content="..."),
    ),
    python=LanguagePrompts(
        panorama=Prompt(content=python_panorama),
        pan_os=Prompt(content=python_pan_os),
        prisma_access=Prompt(content="..."),
        prisma_cloud=Prompt(content="..."),
    ),
    terraform=LanguagePrompts(
        panorama=Prompt(content=terraform_panorama),
        pan_os=Prompt(content=terraform_pan_os),
        prisma_access=Prompt(content="..."),
        prisma_cloud=Prompt(content="..."),
    ),
)
