from django.contrib import admin
from .models import Company, Country, ScoreOfActivity


admin.site.register(Country)
admin.site.register(Company)
admin.site.register(ScoreOfActivity)
