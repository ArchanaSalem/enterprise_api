from django.db import models

class Enterprise(models.Model):
    name = models.CharField(max_length=200, default="Unknown")
    location = models.CharField(max_length=200, default="Not Specified")
    industry = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.name
