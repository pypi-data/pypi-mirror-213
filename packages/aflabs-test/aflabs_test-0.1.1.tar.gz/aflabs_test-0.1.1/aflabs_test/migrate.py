

from django.core.management import call_command
from aflabs_test.boot_django import boot_django

boot_django()
call_command("migrate", "aflabs_test")