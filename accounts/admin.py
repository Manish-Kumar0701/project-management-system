from django.contrib import admin
from .models import Account,Project,ProjectMembers,ProjectTasks,Task,Report

# Register your models here.
models_to_register=[Account,Project,ProjectMembers,ProjectTasks,Task,Report]
for model in models_to_register:
    admin.site.register(model)