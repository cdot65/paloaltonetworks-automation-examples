# dynaconf to handle settings and secrets
from config import settings

# Palo Alto Networks Prisma imports
from panapi import PanApiSession
from panapi.config.objects import Address

# create an empty session
session = PanApiSession()

# authenticate to Prisma OAUTH API
session.authenticate(
    client_id=settings.oauth.client_id,
    client_secret=settings.oauth.client_secret,
    scope=f"profile tsg_id:{settings.tenant.mytentantid.tsg} email",
    token_url=settings.oauth.token_url,
)

# create an address object dictionary
address_object = {
    "folder": "Prisma Access",
    "name": "panapi test",
    "description": "this is just a test",
    "fqdn": "test.redtail.com",
}

# pass the dictionary as arguments into a new PrismaAddress object
prisma_address_object = Address(**address_object)

# create the address object
prisma_address_object.create(session)

# delete the address object
# prisma_address_object.delete(session)
