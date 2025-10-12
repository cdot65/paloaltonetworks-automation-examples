# ============================================================================
# Tags - Austin Folder
# ============================================================================
# Organizational tags for environment and tier classification
# ============================================================================

# ----------------------------------------------------------------------------
# Environment Tags
# ----------------------------------------------------------------------------

resource "scm_tag" "production" {
  folder   = "Austin"
  name     = "production"
  color    = "Red"
  comments = "Production environment"
}

resource "scm_tag" "development" {
  folder   = "Austin"
  name     = "development"
  color    = "Blue"
  comments = "Development environment"
}

# ----------------------------------------------------------------------------
# Tier Tags
# ----------------------------------------------------------------------------

resource "scm_tag" "web_tier" {
  folder   = "Austin"
  name     = "web-tier"
  color    = "Green"
  comments = "Web tier resources"
}

resource "scm_tag" "app_tier" {
  folder   = "Austin"
  name     = "app-tier"
  color    = "Orange"
  comments = "Application tier resources"
}

resource "scm_tag" "data_tier" {
  folder   = "Austin"
  name     = "data-tier"
  color    = "Purple"
  comments = "Data tier resources"
}

resource "scm_tag" "dmz" {
  folder   = "Austin"
  name     = "dmz"
  color    = "Yellow"
  comments = "DMZ resources"
}
