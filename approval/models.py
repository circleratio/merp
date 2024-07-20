from django.db import models
from django.utils import timezone

class Workflow(models.Model):
    originator = models.CharField(max_length=200, default='')

    title = models.CharField(max_length=100, default='')
    
    FLOW_TYPES = [['trip', '出張精算'], ['expense', '経費精算'], ['exec', '事業実施'], ['payment', '支払'], ['contract', '契約']]
    flow_type = models.CharField(max_length=50, choices=FLOW_TYPES, default='')
    
    originate_date = models.DateTimeField(default=timezone.now)

    owner = models.CharField(max_length=50, default='')
    status = models.CharField(max_length=10, default='run')

    approvers = models.CharField(max_length=200, default='{}')
    observers = models.CharField(max_length=200, default='{}')
    history = models.CharField(max_length=200, default='{}')

    note = models.CharField(max_length=200, default='', null=True, blank=True)
    
    item1 = models.CharField(max_length=200, default='', null=True, blank=True)
    item2 = models.CharField(max_length=200, default='', null=True, blank=True)
    item3 = models.CharField(max_length=200, default='', null=True, blank=True)
    item4 = models.CharField(max_length=200, default='', null=True, blank=True)
    item5 = models.CharField(max_length=200, default='', null=True, blank=True)
