from django.urls import path
from .views import EnterprisePostView

urlpatterns = [
    path('enterprises/post/', EnterprisePostView.as_view(), name='enterprise-post'),
]
