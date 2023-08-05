#!/usr/bin/env python
# makemigrations.py

from django.core.management import call_command
from aflabs_test.boot_django import boot_django

boot_django()
call_command("makemigrations", "aflabs_test")