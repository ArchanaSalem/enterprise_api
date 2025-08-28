from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.enterprise_create, name='enterprise-create'),  # POST → create
    path('list/', views.enterprise_list, name='enterprise-list'),             # GET → list active
    path('update/<int:pk>/', views.enterprise_update, name='enterprise-update'),  # POST → update
    path('delete/<int:pk>/', views.enterprise_softdelete, name='enterprise-softdelete'),  # POST → soft delete
]
