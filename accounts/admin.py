from django.contrib import admin
from .models import MyUser,EmailVerification

# Register your models here.
admin.site.register(MyUser)
admin.site.register(EmailVerification)
