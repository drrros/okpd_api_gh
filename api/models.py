from django.db import models
from uuid import uuid4


class Record(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    okpd = models.CharField(max_length=12, unique=True)
    ktru_records_count = models.CharField(max_length=30, blank=True, editable=False)
    isCanceled = models.BooleanField(blank=True, editable=False)
    zapret = models.CharField(max_length=20, blank=True, editable=False)
    ogranichenia = models.CharField(max_length=20, blank=True, editable=False)
    preimuschestvo = models.CharField(max_length=20, blank=True, editable=False)
    dopusk = models.CharField(max_length=20, blank=True, editable=False)
    perechen = models.CharField(max_length=20, blank=True, editable=False)
    forma = models.CharField(max_length=20, blank=True, editable=False)
    tk = models.CharField(max_length=20, blank=True, editable=False)
    efektivnost = models.CharField(max_length=20, blank=True, editable=False)
    perechenTryUIS = models.CharField(max_length=20, blank=True, editable=False)
    nepubl = models.CharField(max_length=20, blank=True, editable=False)
    date_changed = models.DateTimeField(auto_now=True, blank=True, editable=False)
    got_results = models.BooleanField(editable=False, default=False)

    def __repr__(self):
        return f'ОКПД - {self.okpd}'

    def __str__(self):
        return f'ОКПД - {self.okpd}'
