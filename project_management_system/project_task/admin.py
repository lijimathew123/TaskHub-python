from django.contrib import admin
from .models import Employee,Task,Group,Activity

# Register your models here.
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Group)
admin.site.register(Activity)

