# dynaconf to handle settings and secrets
from config import settings

# Palo Alto Networks Prisma imports
from panapi import PanApiSession
from panapi.config.objects import AddressGroup

# create an empty session
session = PanApiSession()

# authenticate to Prisma OAUTH API
session.authenticate(
    client_id=settings.oauth.client_id,
    client_secret=settings.oauth.client_secret,
    scope=f"profile tsg_id:{settings.oauth.tsg} email",
    token_url=settings.oauth.token_url,
)

# create an address object dictionary
address_group = {
    "folder": "Prisma Access",
    "name": "test",
    "description": "this is just a test",
    "static": ["panapi test"],
}

# pass the dictionary as arguments into a new AddressGroup object
prisma_address_group = AddressGroup(**address_group)

# create the address object
prisma_address_group.create(session)

# delete the address object
# prisma_address_group.delete(session)
