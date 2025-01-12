# dynaconf to handle settings and secrets
from config import settings

# Palo Alto Networks Prisma imports
from panapi.config.security import SecurityRule
from panapi import PanApiSession

session = PanApiSession()

# authenticate to Prisma Access OAuth API
session.authenticate(
    client_id=settings.oauth.client_id,
    client_secret=settings.oauth.client_secret,
    scope=f"profile tsg_id:{settings.oauth.tsg} email",
    token_url=settings.oauth.token_url,
)

# Create a security rule object
security_rule = {
    "name": "DMZ Outbound",
    "action": "allow",
    "from": ["any"],
    "to": ["any"],
    "source": ["any"],
    "destination": ["any"],
    "source_user": ["any"],
    "category": ["any"],
    "application": ["any"],
    "service": ["application-default"],
    "log_setting": "Cortex Data Lake",
    "description": "Control outbound internet access for DMZ",
    "folder": "Prisma Accses",
    "position": "pre",
}

# Create the security rule
prisma_rule = SecurityRule(**security_rule)
prisma_rule.create(session)
