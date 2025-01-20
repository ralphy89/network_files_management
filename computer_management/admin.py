from django.contrib import admin
from .models import Computer
from .models import Student, History
# Register your models here.

admin.site.register(Computer)
admin.site.register(Student)
admin.site.register(History)

