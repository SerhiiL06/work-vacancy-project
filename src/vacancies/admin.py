from django.contrib import admin

from .models import Respond, Resume, Vacancy

admin.site.register(Vacancy)
admin.site.register(Resume)
admin.site.register(Respond)
