from django.db import models
import datetime

# Create your models here.
class Sync(models.Model):
    sync_time = models.DateTimeField()