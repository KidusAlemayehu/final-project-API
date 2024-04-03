from django.core.management.base import BaseCommand
from apps.staff_user.models import StaffUser
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            "first_name": os.getenv("ADMIN_FIRST_NAME"),
            "last_name": os.getenv("ADMIN_LAST_NAME"),
            "username": os.getenv("ADMIN_USERNAME"),
            "email": "kidusalemayehu3346@gmail.com",
            "password": os.getenv("ADMIN_PASSWORD"),
            "phone": os.getenv("ADMIN_PHONE"),
            "office":"HOD",
            "role": "Administrator",
            "gender": "Male"
        }
        if not StaffUser.objects.filter(username=data['username']).exists():
            self.stdout.write(self.style.NOTICE("Initiating Administrator Account ..."))
            try:
                password = data.pop('password')
                admin_user = StaffUser.objects.create(**data)
                admin_user.set_password(password)
                admin_user.save()
                self.stdout.write(self.style.SUCCESS("Initiating Completed!"))
            except Exception as e:
                return str(e)
        else:
            self.stdout.write(self.style.ERROR_OUTPUT("Administrator Account already exists!"))