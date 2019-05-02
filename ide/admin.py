from django.contrib import admin
from .models import Problem, UserDetail, Submissions
# Register your models here.

admin.site.register(Problem)
admin.site.register(UserDetail)
admin.site.register(Submissions)
