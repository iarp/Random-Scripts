import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iarp.settings")
django.setup()

from django.db import connection
from django.conf import settings

from domain_rates.models import TldHistory

highest = TldHistory.objects.order_by('id').last()
print(highest.pk)

with connection.constraint_checks_disabled():
    with open(os.path.join(settings.BASE_DIR, 'domain_rates/fixtures/TldHistory.json'), 'r') as fo:
        data = json.load(fo)
        for obj in data:
            pk = obj['pk']

            if pk % 10000 == 0:
                print(pk)

            if pk <= highest.pk:
                continue

            reg_id = obj['fields'].pop('registrar')

            TldHistory.objects.create(
                pk=pk,
                registrar_id=reg_id,
                **obj['fields']
            )
