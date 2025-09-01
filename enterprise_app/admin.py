from django.contrib import admin
from .models import Enterprise, Region, Circle, Cluster

admin.site.register(Enterprise)
admin.site.register(Region)
admin.site.register(Circle)
admin.site.register(Cluster)

