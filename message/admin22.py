from django.contrib import admin
from . models import Messages
# Register your models here.


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    pass
