provider "scm" {
  # Authentication can be configured in multiple ways:
  # 1. Directly in this block (not recommended for sensitive data)
  # 2. Using environment variables (recommended)
  # 3. Using a JSON config file

  # Option 1: Direct configuration (use variables from terraform.tfvars)
  host          = var.scm_host
  auth_url      = var.scm_auth_url
  client_id     = var.scm_client_id
  client_secret = var.scm_client_secret
  scope         = var.scm_scope

  # Option 2: Environment variables (recommended)
  # Export these in your shell:
  # export SCM_HOST="api.sase.paloaltonetworks.com"
  # export SCM_AUTH_URL="https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
  # export SCM_CLIENT_ID="your-client-id"
  # export SCM_CLIENT_SECRET="your-client-secret"
  # export SCM_SCOPE="your-scope"

  # Option 3: JSON config file
  # auth_file = var.scm_auth_file

  # Logging level: quiet, action, path, info, debug
  logging = var.scm_logging
}
