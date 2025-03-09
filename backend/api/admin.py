from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


# class UserAdmin(admin.ModelAdmin):
#     """
#     Define StackedInline page for Student Response
#     """

#     model = User
# exclude = ["score"]


# class StudentAdmin(admin.ModelAdmin):
#     """
#     Define admin page for Students
#     """

#     inlines = [
#         StudentResponseInline,
#     ]
#     ordering = ["age"]
#     list_display = ["age", "gender"]


# class ResourceAdmin(admin.ModelAdmin):
#     """
#     Define admin page for Resources
#     """

#     ordering = ["id"]
#     list_display = ["type", "url"]


# admin.site.register(User, UserAdmin)
# admin.site.register(Resource, ResourceAdmin)
