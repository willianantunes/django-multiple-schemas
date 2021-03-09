from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with CMU pronunciation dictionary"

    def add_arguments(self, parser):
        parser.add_argument("--create-super-user", action="store_true")
        parser.add_argument("-u", type=str, default="admin")
        parser.add_argument("-p", type=str, default="admin")

    def handle(self, *args, **options):
        self.create_super_user = options["create_super_user"]
        self.admin_username = options["u"].strip()
        self.admin_password = options["p"].strip()

        if self.create_super_user:
            if User.objects.filter(username=self.admin_username).count() == 0:
                self.stdout.write(f"Creating ADMIN username {self.admin_username}")
                _create_super_user(self.admin_username, self.admin_password)
            else:
                self.stdout.write(f"Super user already exists")


def _create_super_user(username, password):
    return User.objects.create_superuser(username, None, password)
