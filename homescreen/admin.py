from django.contrib import admin

# Register your models here.
from .models import Courses, Reviews

# Register your models here.
admin.site.register(Courses)
admin.site.register(Reviews)
