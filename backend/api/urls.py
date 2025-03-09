from django.urls import path
from .views.views_user import CreateUserView, ListUserDetailView, ListUsersView
from .views.views_course import (
    AddCourseReviewView,
    CreateUserCourseView,
    EnrollUserCourseView,
    ListCourseByUserView,
    ListCourseDetailView,
    ListCousesByCategoryView,
    RemoveStudentFromCourseView,
    UpdateCourseUserBlockStatusView,
)

from .views.views_course_material import (
    AddCourseMaterialView,
    DownloadCourseMaterialAttachmentView,
)
from .views.views_status import UserStatus


urlpatterns = [
    # ------------ Course ------------ #
    path(
        "courses/list-three-by-category",
        ListCousesByCategoryView.as_view(),
        name="list-three-courses-by-category",
    ),
    path(
        "courses/<str:course_id>",
        ListCourseDetailView.as_view(),
        name="list-course-details",
    ),
    path(
        "courses/<str:course_id>/student",
        RemoveStudentFromCourseView.as_view(),
        name="remove-student-from-course",
    ),
    path(
        "courses/<str:course_id>/student/<str:student_id>",
        UpdateCourseUserBlockStatusView.as_view(),
        name="update-user-block-status-in-course",
    ),
    path(
        "courses/<str:course_id>/review",
        AddCourseReviewView.as_view(),
        name="add-course-review",
    ),
    # ------------ Course Material ------------ #
    path(
        "courses/<str:course_id>/course-material",
        AddCourseMaterialView.as_view(),
        name="add-course-material",
    ),
    path(
        "courses/materials/download",
        DownloadCourseMaterialAttachmentView.as_view(),
        name="download-course-material-attachment",
    ),
    # ------------ User ------------ #
    # Update user status
    path(
        "users/status",
        UserStatus.as_view(),
        name="update-user-status",
    ),
    # Get courses related to an user
    path(
        "users/courses/<str:username>",
        ListCourseByUserView.as_view(),
        name="get-user-courses",
    ),
    # Create course
    path(
        "users/course/author",
        CreateUserCourseView.as_view(),
        name="create-user-course",
    ),
    path(
        "users/course/enroll",
        EnrollUserCourseView.as_view(),
        name="enroll-user-in-course",
    ),
    # Get all users
    path(
        "users",
        ListUsersView.as_view(),
        name="list-all-users",
    ),
    # Get all users
    path(
        "users/<str:username>",
        ListUserDetailView.as_view(),
        name="list-specific-user-details",
    ),
]
