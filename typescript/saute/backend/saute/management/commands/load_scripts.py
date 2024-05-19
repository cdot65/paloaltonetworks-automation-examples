import os
from django.core.management.base import BaseCommand, CommandError
from saute.models import Script
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Loads Python scripts from a specified directory into the database"

    def add_arguments(self, parser):
        parser.add_argument("dir", type=str, help="Directory to load scripts from")

    def handle(self, *args, **options):
        dir = options["dir"]
        if not os.path.isdir(dir):
            raise CommandError(f"{dir} is not a directory")

        system_user, _ = User.objects.get_or_create(username="system")

        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    filename = os.path.basename(
                        path
                    )  # Just get the filename, not the full path
                    script, created = Script.objects.get_or_create(
                        name=filename,
                        defaults={"file": filename, "author": system_user},
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created script {script.name}"
                            )
                        )
                    else:
                        self.stdout.write(f"Script {script.name} already exists")
