import glob
import os

from django_forms import settings

for app in settings.INSTALLED_APPS:

    # Apps can be listed as "app" or "app.apps.AppConfig", split on . and grab first element.
    app = app.split('.')[0]

    app_dir = os.path.join(settings.BASE_DIR, app)

    # If it's not in the BASE_DIR then it isn't our own app
    if not os.path.isdir(app_dir):
        continue

    for file in glob.glob(os.path.join(app_dir, 'migrations', '*.py')):

        if '__init__' in file:
            continue

        os.remove(file)

if 'sqlite3' in settings.DATABASES.get('default'):

    try:
        os.remove(os.path.join(settings.BASE_DIR, settings.DATABASES['default']['name']))
    except (OSError, FileNotFoundError):
        pass
