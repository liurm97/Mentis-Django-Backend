from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import (
    Course,
)


class Command(BaseCommand):
    help = "Clears and reset database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        User.objects.all().delete()
        Course.objects.all().delete()
