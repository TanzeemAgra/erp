from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Set password for admin user'

    def handle(self, *args, **options):
        try:
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully set admin password to: admin123')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Admin user does not exist')
            )
