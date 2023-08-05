
# boot_django.py
#
# to setup and configure, we use this file. Which is used by scripts 
# that must run on a Django server as if it was running.
import os
import django
from django.conf import settings
 
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "aflabs_test"))
 
def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default":{
                "ENGINE":"django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            "aflabs_test",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()