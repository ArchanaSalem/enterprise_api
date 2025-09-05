from django.db import models
from django.utils import timezone


# ------- ENTERPRISE ----------------
class Enterprise(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# -------- REGION ----------------
class Region(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('enterprise', 'name')

    def __str__(self):
        return f"{self.name} ({self.enterprise.name})"

# ------ CIRCLE ----------------
class Circle(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='circles')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='circles')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('enterprise', 'region', 'name')

    def __str__(self):
        return f"{self.name} ({self.region.name} / {self.enterprise.name})"

# ------- CLUSTER -------
class Cluster(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='clusters')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='clusters')
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='clusters')
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('enterprise', 'region', 'circle', 'name')

    def __str__(self):
        return f"{self.name} ({self.circle.name} / {self.region.name} / {self.enterprise.name})"


# ----------------- STORE -----------------
class Store(models.Model):
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE, related_name='stores')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='stores')
    circle = models.ForeignKey('Circle', on_delete=models.CASCADE, related_name='stores')
    cluster = models.ForeignKey('Cluster', on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('enterprise', 'region', 'circle', 'cluster', 'name')

    def __str__(self):
        return f"{self.name} ({self.cluster.name} / {self.circle.name} / {self.region.name} / {self.enterprise.name})"

#------Role Table-----------

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#-------User Table...
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    experience = models.PositiveIntegerField(help_text="Experience in years")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # plain text as request 
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role} @ {self.store}"


