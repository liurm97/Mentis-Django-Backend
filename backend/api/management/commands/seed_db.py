from ...models import (
    Interest,
    Notification,
    Course,
    CourseTracker,
    CourseMaterial,
    StudentFeedback,
    Status,
    Role,
)

from django.contrib.auth.models import User

from typing import Any
from django.core.management.base import BaseCommand
from uuid import uuid4


class Command(BaseCommand):
    help = """

        Seed database

        - Add 5 users:
            - 2 Students
            - 3 Teachers
            - Add to Role and Status (Should be added along with Users)

        - Add Interest:
            - 1 student has interests
            - 1 student has no interest

        - Add Notification:
            - 1 student has 1 notification
            - Other student has no notification
            - 1 teacher has 1 notification
            - Other teachers has no notification

        - Add Courses:
            - 3 categories - 5 subcategories each - 1 course each
            - categories = ["Business", "Development", "Personal Development"
            - subcategories = {
                "business": ["Entrepreneurship", "Communication", "Sales", "Human Resources", "E-commerce"],
                "development": ["Web Development", "Data Science", "Mobile Development", "Game Development", "Software Testing"],
                "personal_development": ["Productivity", "Leadership", "Career Development", "Creativity", "Stress Management"]
            }

        - Add Course material

        - Add Course feedback

        - Add CourseTracker:
            - 1 student enrolled in a course authored by a teacher
            - 3 teachers authored 5 courses each
    """

    course_payload = [
        # Business (taught by daniel1980)
        {
            "name": "Startup Success: From Idea to Execution",
            "category": "business",
            "subcategory": "entrepreneurship",
            "description": "Learn the essential steps to launching and scaling a successful business. This course covers ideation, business planning, funding strategies, marketing, and scaling your startup effectively.",
            "author": "daniel1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Mastering Communication: Speak, Listen, and Influence",
            "category": "business",
            "subcategory": "communication",
            "description": "Enhance your communication skills for personal and professional success. Learn how to articulate ideas clearly, improve listening skills, and influence others through effective verbal and non-verbal communication techniques.",
            "author": "daniel1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Sales Mastery: Closing Deals and Winning Clients",
            "category": "business",
            "subcategory": "sales",
            "description": "Discover proven sales techniques to attract, engage, and convert customers. From prospecting to closing, this course equips you with the skills to boost your sales performance and build long-term client relationships.",
            "author": "daniel1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "HR Essentials: Hiring, Managing, and Retaining Talent",
            "category": "business",
            "subcategory": "human_resources",
            "description": "Gain a comprehensive understanding of human resource management, including talent acquisition, performance evaluation, employee engagement, and workplace policies to build a strong and motivated workforce.",
            "author": "daniel1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "E-commerce Masterclass: Launch, Scale, and Succeed",
            "category": "business",
            "subcategory": "e_commerce",
            "description": "Learn how to build and manage a successful online store. This course covers choosing the right platform, product sourcing, digital marketing, customer retention, and scaling your e-commerce business.",
            "author": "daniel1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        # Development (taught by mark1980)
        {
            "name": "Full-Stack Web Development: Build and Deploy Modern Apps",
            "category": "development",
            "subcategory": "web_development",
            "description": "Learn how to build and manage a successful online store. This course covers choosing the right platform, product sourcing, digital marketing, customer retention, and scaling your e-commerce business.",
            "author": "mark1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Data Science Foundations: Analyze, Predict, and Visualize",
            "category": "development",
            "subcategory": "data_science",
            "description": "Develop data analysis and machine learning skills to extract insights from data. Learn Python, SQL, data visualization, statistical modeling, and AI-driven predictive analytics to make data-driven decisions.",
            "author": "mark1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Mobile App Development: Build iOS & Android Apps",
            "category": "development",
            "subcategory": "mobile_development",
            "description": "Learn to create cross-platform mobile applications using React Native, Flutter, or native technologies. This course covers UI/UX design, API integration, and app deployment on both iOS and Android.",
            "author": "mark1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Game Development Bootcamp: From Concept to Playable Game",
            "category": "development",
            "subcategory": "game_development",
            "description": "Explore game design and development using Unity or Unreal Engine. Learn game mechanics, physics, AI programming, and monetization strategies to bring your game ideas to life.",
            "author": "mark1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Software Testing & QA: Ensuring Bug-Free Applications",
            "category": "development",
            "subcategory": "software_testing",
            "description": "Master the fundamentals of software testing, including manual and automated testing techniques. Learn how to identify bugs, write test cases, and use industry-standard testing tools to improve software quality.",
            "author": "mark1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        # Personal Development (taught by wesley1980)
        {
            "name": "Productivity Hacks: Work Smarter, Not Harder",
            "category": "personal_development",
            "subcategory": "productivity",
            "description": "Unlock productivity secrets to manage your time efficiently and get more done. This course covers goal-setting, time management techniques, and digital tools to boost your personal and professional efficiency.",
            "author": "wesley1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Effective Leadership: Inspire, Motivate, and Lead",
            "category": "personal_development",
            "subcategory": "leadership",
            "description": "Develop leadership skills to inspire and guide teams toward success. Learn how to communicate vision, make strategic decisions, resolve conflicts, and build a high-performance team.",
            "author": "wesley1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Career Growth Blueprint: Skills, Networking & Success",
            "category": "personal_development",
            "subcategory": "career_development",
            "description": "Learn how to build a successful career through skill development, networking, and personal branding. This course provides strategies to land your dream job and accelerate professional growth.",
            "author": "wesley1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
        {
            "name": "Stress Management Techniques: Stay Calm & Focused",
            "category": "personal_development",
            "subcategory": "stress_management",
            "description": "Learn practical strategies to manage stress, improve mental well-being, and maintain focus. This course covers mindfulness techniques, work-life balance, and coping mechanisms to reduce anxiety and increase resilience.",
            "author": "wesley1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
            "feedback": {"feedback": "Stress management is a great technique to learn"},
            "enrolledStudent": "bob1997",
        },
        {
            "name": "Unlock Your Creativity: Think Outside the Box",
            "category": "personal_development",
            "subcategory": "creativity",
            "description": "Discover practical techniques to enhance creativity and innovative thinking. This course helps you overcome mental blocks, generate unique ideas, and apply creative problem-solving in any field.",
            "author": "wesley1980",
            "courseMaterial": {
                "title": "introduction",
                "content": "Introduction to the course",
                "duration": 10,
            },
        },
    ]

    user_payload = [
        {
            "username": "bob1997",
            "first_name": "Bobby",
            "last_name": "Taylor",
            "email": "bob97@gmail.com",
            "role": "student",
            "password": "bob1997",
            "interest": [{"interest": "business"}, {"interest": "development"}],
        },
        {
            "username": "john1998",
            "first_name": "John",
            "last_name": "Park",
            "email": "john1998@gmail.com",
            "role": "student",
            "password": "john1998",
        },
        {
            "username": "daniel1980",
            "first_name": "Daniel",
            "last_name": "West",
            "email": "daniel1980@gmail.com",
            "role": "teacher",
            "password": "daniel1980",
        },
        {
            "username": "mark1980",
            "first_name": "Mark",
            "last_name": "Jacob",
            "email": "mark1980@gmail.com",
            "role": "teacher",
            "password": "mark1980",
        },
        {
            "username": "wesley1980",
            "first_name": "Wesley",
            "last_name": "Sanders",
            "email": "wesley1980@gmail.com",
            "role": "teacher",
            "password": "wesley1980",
        },
    ]

    def seed_user_role_status_interest(self) -> None:
        """
        - seed users
        - seed user roles
        - seed user statuses
        - seed interests for student users
        """
        for user_payload in self.user_payload:
            role = user_payload.pop("role")

            # student has interest
            if role == "student" and "interest" in user_payload:
                list_of_interest = user_payload.pop("interest")
                interest_payload = []

                # insert into User table
                created_user = User.objects.create_user(**user_payload)

                # insert into Role table
                Role.objects.create(role=role, userRole=created_user)

                # insert into Status table
                status_unique_id = uuid4()
                Status.objects.create(id=status_unique_id, userStatus=created_user)

                # prepare Interest object for bulk_create
                for interest in list_of_interest:
                    unique_interest_id = uuid4()
                    interest_value = interest.get("interest")

                    interest_payload.append(
                        Interest(
                            id=unique_interest_id,
                            interest=interest_value,
                            studentInterest=created_user,
                        )
                    )

                # bulk_create interest
                Interest.objects.bulk_create(interest_payload)

            # student has no interest and teacher
            elif role == "student" or role == "teacher":
                # insert into User table
                created_user = User.objects.create_user(**user_payload)

                # insert into Role table
                Role.objects.create(role=role, userRole=created_user)

                # insert into Status table
                status_unique_id = uuid4()
                Status.objects.create(id=status_unique_id, userStatus=created_user)

            user_payload["role"] = role

    def seed_course_material_feedback_tracker(self) -> None:
        """
        - seed courses
        - seed course materials
        - seed course feedbacks
        """
        for course_payload in self.course_payload:
            course_unique_id = uuid4()

            # Insert into Course
            created_course = Course.objects.create(
                id=course_unique_id,
                name=course_payload.get("name"),
                category=course_payload.get("category"),
                subcategory=course_payload.get("subcategory"),
                description=course_payload.get("description"),
            )

            # Insert into CourseTracker
            course_author_username = course_payload.get("author")
            course_author = User.objects.filter(username=course_author_username).first()
            course_tracker_unique_id = uuid4()

            ### Insert course authors
            CourseTracker.objects.create(
                id=course_tracker_unique_id,
                user=course_author,
                course=created_course,
                profile="author",
            )

            ### Insert enrolled students
            if "enrolledStudent" in course_payload:
                course_tracker_unique_id_2 = uuid4()
                enrolled_student_username = course_payload.get("enrolledStudent")
                enrolled_student_user = User.objects.filter(
                    username=enrolled_student_username
                ).first()

                CourseTracker.objects.create(
                    id=course_tracker_unique_id_2,
                    user=enrolled_student_user,
                    course=created_course,
                    profile="learner",
                )

            # Insert into CourseMaterial
            course_material_unique_id = uuid4()

            CourseMaterial.objects.create(
                id=course_material_unique_id,
                title=course_payload.get("courseMaterial").get("title"),
                content=course_payload.get("courseMaterial").get("content"),
                duration=course_payload.get("courseMaterial").get("duration"),
                course=created_course,
            )

            # if course contains student feedback
            if "feedback" in course_payload:
                course_feedback = course_payload.get("feedback").get("feedback")
                course_feedback_unique_id = uuid4()
                random_student_user = (
                    Role.objects.filter(role="student").first().userRole
                )

                StudentFeedback.objects.create(
                    id=course_feedback_unique_id,
                    course=created_course,
                    student=random_student_user,
                    feedback=course_feedback,
                )

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.seed_user_role_status_interest()
        self.seed_course_material_feedback_tracker()
