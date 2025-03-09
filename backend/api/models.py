"""Define django models"""

from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Role(models.Model):
    TEACHER = "teacher"
    STUDENT = "student"

    ROLE_CHOICES = {
        TEACHER: "Teacher",
        STUDENT: "Student",
    }

    role = models.CharField(choices=ROLE_CHOICES, max_length=7)
    userRole = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userRole"
    )

    class Meta:
        """
        Constraint to ensure status value must be in (active, busy, dnd, away).
        """

        constraints = [
            models.CheckConstraint(
                check=models.Q(role="teacher") | models.Q(role="student"),
                name="Role constraint",
                violation_error_message="Role value must be in (teacher, student).",
            )
        ]

    def __str__(self):
        return f"Role:: {self.role} for student {self.userRole.first_name} {self.userRole.last_name}"


class Status(models.Model):
    """
    Model for user's status
    """

    ACTIVE = "active"
    BUSY = "busy"
    DO_NOT_DISTURB = "dnd"
    AWAY = "away"

    STATUS_CHOICES = {
        ACTIVE: "Active",
        BUSY: "Busy",
        DO_NOT_DISTURB: "Do Not Disturb",
        AWAY: "Away",
    }

    id = models.CharField(
        max_length=100, primary_key=True, db_index=True, default=uuid4()
    )
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default=ACTIVE, null=False, blank=False
    )
    userStatus = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userStatus"
    )

    class Meta:
        """
        Constraint to ensure status value must be in (active, busy, dnd, away).
        """

        constraints = [
            models.CheckConstraint(
                check=models.Q(status="active")
                | models.Q(status="busy")
                | models.Q(status="dnd")
                | models.Q(status="away"),
                name="Status constraint",
                violation_error_message="User's status value must be in (active, busy, dnd, away).",
            )
        ]

    def __str__(self):
        return f"Status:: {self.status} for student {self.userStatus.first_name} {self.userStatus.last_name}"


class Interest(models.Model):
    """
    Model for user's interest
    """

    id = models.CharField(
        max_length=100, primary_key=True, db_index=True, default=uuid4()
    )
    interest = models.CharField(
        max_length=99,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(0, "interest field cannot be empty"),
            RegexValidator(
                regex=r"^[a-z][a-z_]*[a-z]$",
                message="interest must be valid and in small letters",
            ),  # eg: data_analysis, math, personal_development
        ],
    )
    studentInterest = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="studentInterest"
    )

    def __str__(self):
        return f"Interest:: {self.interest} for student {self.studentInterest.first_name} {self.studentInterest.last_name}"


class Course(models.Model):
    """
    Model for Course
    """

    id = models.CharField(
        max_length=100, primary_key=True, db_index=True, default=uuid4()
    )
    name = models.CharField(max_length=250, null=False, blank=False)
    category = models.CharField(max_length=250, null=False, blank=False)
    subcategory = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    courseTracker = models.ManyToManyField(
        User, through="CourseTracker", related_name="courseTracker"
    )
    studentFeedback = models.ManyToManyField(
        User, through="StudentFeedback", related_name="studentFeedback"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Course name:: {self.name}\n"


class CourseTracker(models.Model):
    """
    Model for Course - Record author/learner of a course
    """

    AUTHOR = "author"
    LEARNER = "learner"

    PROFILE_CHOICES = {
        AUTHOR: "Author",
        LEARNER: "Learner",
    }
    id = models.CharField(
        max_length=100, primary_key=True, db_index=True, default=uuid4()
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(blank=False, null=False, default=False)
    profile = models.CharField(
        choices=PROFILE_CHOICES, max_length=50, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Constraint to ensure profile value must be in (author, learner).
        """

        constraints = [
            models.CheckConstraint(
                check=models.Q(profile="author") | models.Q(profile="learner"),
                name="Profile constraint",
                violation_error_message="Profile value must be in (author, learner).",
            )
        ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} is a {self.profile}"


class StudentFeedback(models.Model):
    """
    Model for Student feedback - Record feedback left by user on a course
    """

    id = models.CharField(
        max_length=100, primary_key=True, db_index=True, default=uuid4()
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    feedback = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback:: {self.feedback} provided by {self.student.first_name} {self.student.last_name}"


class CourseMaterial(models.Model):
    """
    Model for Course material
    """

    id = models.CharField(
        max_length=100, primary_key=True, db_index=True, default=uuid4()
    )
    title = models.CharField(max_length=250, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    # uploadURL = models.CharField(max_length=250, null=True)
    upload = models.FileField(upload_to="materials/", null=True, blank=True)
    duration = models.PositiveSmallIntegerField(null=False, blank=False)  # in minutes
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
