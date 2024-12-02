from django.contrib import admin

from . models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
    # list_display = ('username', 'email', 'first_name', 'last_name')
    # list_filter = ('id', 'username', 'email', 'first_name', 'last_name', 'user_avatar')
    # search_fields = ('username', 'email', 'first_name', 'last_name',)

    # class Meta:
    #     model = User
