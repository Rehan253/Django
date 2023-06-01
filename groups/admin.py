from django.contrib import admin
from . import models

# Register your models here.
# to edit group members in admin page
class GroupMemberInLine(admin.TabularInline):
    model=models.GroupMember

admin.site.register(models.Group)
