from django.db import models
from django.utils import timezone

# ------------------- Enterprise -------------------
class Enterprise(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True, default='Unknown')
    industry = models.CharField(max_length=255, null=True, blank=True, default='General')

    def __str__(self):
        return self.name

# ------------------- Region -------------------
class Region(models.Model):
    name = models.CharField(max_length=255)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'enterprise')

    def __str__(self):
        return self.name

# ------------------- Circle -------------------
class Circle(models.Model):
    name = models.CharField(max_length=255)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'enterprise', 'region')

    def __str__(self):
        return self.name

# ------------------- Cluster -------------------
class Cluster(models.Model):
    name = models.CharField(max_length=255)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'enterprise', 'region', 'circle')

    def __str__(self):
        return self.name

# ------------------- Store -------------------
class Store(models.Model):
    name = models.CharField(max_length=255)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE)
    cluster = models.ForeignKey('Cluster', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True, default='Unknown')
    industry = models.CharField(max_length=255, null=True, blank=True, default='General')

    class Meta:
        unique_together = ('name', 'enterprise', 'region', 'circle', 'cluster')

    def __str__(self):
        return self.name
