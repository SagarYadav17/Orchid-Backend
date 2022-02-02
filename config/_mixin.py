from os import environ
from dotenv import load_dotenv

load_dotenv()

# Django Default
DJANGO_SECRET_KEY = environ.get("DJANGO_SECRET_KEY", "django-insecure-0p10lo00s_*fx%g0l5isyyfv_fk2+u!8^6xtn^@*6x-taqabq9")

# Auth0
AUTH0_JWT_ISSUER = environ.get("AUTH0_JWT_ISSUER")
AUTH0_API_IDENTIFIER = environ.get("AUTH0_API_IDENTIFIER")
