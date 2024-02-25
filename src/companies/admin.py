from django.contrib import admin
from .models import Company, Country, ScoreOfActivity, VerifyRequest


admin.site.register(Country)
admin.site.register(Company)
admin.site.register(ScoreOfActivity)
admin.site.register(VerifyRequest)
