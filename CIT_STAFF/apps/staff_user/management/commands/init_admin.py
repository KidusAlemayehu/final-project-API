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
            "role": "Administrator",
            "gender": "Male"
        }
        if not StaffUser.objects.filter(username=data['username']).exists():
            print("Initiating Administrator Account ...")
            try:
                password = data.pop('password')
                admin_user = StaffUser.objects.create(**data)
                admin_user.set_password(password)
                admin_user.save()
                print("Initiating Completed!")
            except Exception as e:
                return str(e)
        else:
            print("Administrator Account already exists!")