from django.contrib import admin
from .models import User

# Зарегистрировали модель User в админ-панели
admin.site.register(User)
