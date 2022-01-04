from django.contrib import admin

from core.models import City, Country, Gender, RelationType, State

# Register your models here.
admin.site.register(Gender)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(RelationType)
