from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


# class UserAdmin():
#     """
#     Define StackedInline page for Student Response
#     """

#     # inlines = [MyInlineAdmin]


class StatusAdmin(admin.ModelAdmin):
    """
    Define admin page for Status
    """


class RoleAdmin(admin.ModelAdmin):
    """
    Define admin page for Role
    """


class InterestAdmin(admin.ModelAdmin):
    """
    Define admin page for Interest
    """


class CourseAdmin(admin.ModelAdmin):
    """
    Define admin page for Course
    """


class CourseTrackerAdmin(admin.ModelAdmin):
    """
    Define admin page for CourseTracker
    """


class StudentFeedbackAdmin(admin.ModelAdmin):
    """
    Define admin page for StudentFeedback
    """


class CourseMaterialAdmin(admin.ModelAdmin):
    """
    Define admin page for CourseMaterial
    """


admin.site.register(Status, StatusAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseTracker, CourseTrackerAdmin)
admin.site.register(StudentFeedback, StudentFeedbackAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)
