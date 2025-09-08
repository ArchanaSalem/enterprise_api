from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include all enterprise_app URLs
    path('api/', include('enterprise_app.urls')),  # <--- important

]
    