from django.core.management.base import BaseCommand
from apps.staff_user.models import *
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {
            "first_name": os.getenv("DEVELOPER_FIRST_NAME"),
            "last_name": os.getenv("DEVELOPER_LAST_NAME"),
            "username": os.getenv("DEVELOPER_USERNAME"),
            "email": os.getenv("DEVELOPER_EMAIL"),
            "password": os.getenv("DEVELOPER_PASSWORD"),
            "phone": os.getenv("DEVELOPER_PHONE"),
            "gender": "Male",
            "is_superuser": True,
        }

        # Check if the developer user already exists
        dev_user = StaffUser.objects.filter(username=data['username']).first()
        if not dev_user:
            self.stdout.write(self.style.NOTICE("Initiating Developer Account ..."))
            try:
                # Create the user
                password = data.pop('password')
                dev_user = StaffUser.objects.create(**data)
                dev_user.set_password(password)
                dev_user.save()
                self.stdout.write(self.style.SUCCESS("Developer Account created successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during user creation: {str(e)}"))
                return
        
        # Get the DEV office
        dev_office = Office.objects.get(name=OfficeChoices.DEVELOPER)

        # Check if the role already exists
        if not Roles.objects.filter(user=dev_user, office=dev_office, role=RoleChoices.ADMINISTRATOR, work_role=WorkRoleChoices.ASSISTANT).exists():
            try:
                # Create the role
                dev_role = Roles.objects.create(user=dev_user, office=dev_office, role=RoleChoices.ADMINISTRATOR, work_role=WorkRoleChoices.ASSISTANT)
                dev_role.save()
                self.stdout.write(self.style.SUCCESS("Developer role created successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during role creation: {str(e)}"))
        else:
            self.stdout.write(self.style.NOTICE("Developer role already exists!"))

        self.stdout.write(self.style.SUCCESS("Initiating Completed Successfully!"))