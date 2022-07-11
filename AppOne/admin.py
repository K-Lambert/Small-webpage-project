from django.contrib import admin
from AppOne.models import *

# Register your models here.
admin.site.register(StudentClassModel),
admin.site.register(UserClassExtension),
admin.site.register(StudentProfileModel),
admin.site.register(TaskModel),
admin.site.register(StudentMarksModel)
