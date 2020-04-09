from django.contrib import admin
from .models import Priority, Todo


class TodoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Todo, TodoAdmin)
admin.site.register(Priority, TodoAdmin)
