from django.core.management.base import BaseCommand
from apps.staff_user.models import *
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        # Create offices
        for office_choice in OfficeChoices:
            office, created = Office.objects.get_or_create(name=office_choice.value)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created office: {office_choice.value}"))
            else:
                self.stdout.write(self.style.NOTICE(f"Office already exists: {office_choice.value}"))

        # Create sections for UG office
        for section_choice in SectionChoices:
            office = Office.objects.get(name=OfficeChoices.UG)
            section, created = Section.objects.get_or_create(name=section_choice.value, office=office)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created section: {section_choice.value} for UG office"))
            else:
                self.stdout.write(self.style.NOTICE(f"Section already exists: {section_choice.value}"))

        # Administrator data from environment variables
        data = {
            "first_name": os.getenv("ADMIN_FIRST_NAME"),
            "last_name": os.getenv("ADMIN_LAST_NAME"),
            "username": os.getenv("ADMIN_USERNAME"),
            "email": "kidusalemayehu3346@gmail.com",
            "password": os.getenv("ADMIN_PASSWORD"),
            "phone": os.getenv("ADMIN_PHONE"),
            "gender": "Male",
            "is_superuser": True,
        }

        # Check if the administrator user already exists
        admin_user = StaffUser.objects.filter(username=data['username']).first()
        if not admin_user:
            self.stdout.write(self.style.NOTICE("Initiating Administrator Account ..."))
            try:
                # Create the user
                password = data.pop('password')
                admin_user = StaffUser.objects.create(**data)
                admin_user.set_password(password)
                admin_user.save()
                self.stdout.write(self.style.SUCCESS("Administrator Account created successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during user creation: {str(e)}"))
                return
        
        # Get the HOD office
        hod_office = Office.objects.get(name=OfficeChoices.HOD)

        # Check if the role already exists
        if not Roles.objects.filter(user=admin_user, office=hod_office, role=RoleChoices.ADMINISTRATOR, work_role=WorkRoleChoices.LECTURER).exists():
            try:
                # Create the role
                admin_role = Roles.objects.create(user=admin_user, office=hod_office, role=RoleChoices.ADMINISTRATOR, work_role=WorkRoleChoices.LECTURER)
                admin_role.save()
                self.stdout.write(self.style.SUCCESS("Administrator role created successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error during role creation: {str(e)}"))
        else:
            self.stdout.write(self.style.NOTICE("Administrator role already exists!"))

        self.stdout.write(self.style.SUCCESS("Initiating Completed Successfully!"))
