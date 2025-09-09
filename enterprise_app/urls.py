from django.urls import path
from . import views
from .views import create_user, update_user, delete_user, login_user,change_password

urlpatterns = [
    # Enterprise
    path('enterprise/list', views.enterprise_list),
    path('enterprise/create', views.enterprise_create),
    path('enterprise/update', views.enterprise_update),
    path('enterprise/delete', views.enterprise_delete),

    # Region
    path('region/list', views.region_list),
    path('region/create', views.region_create),
    path('region/update', views.region_update),
    path('region/delete', views.region_delete),

    # Circle
    path('circle/list', views.circle_list),
    path('circle/create', views.circle_create),
    path('circle/update', views.circle_update),
    path('circle/delete', views.circle_delete),

    # Cluster
    path('cluster/list', views.cluster_list),
    path('cluster/create', views.cluster_create),
    path('cluster/update', views.cluster_update),
    path('cluster/delete', views.cluster_delete),

    # Store
    path('store/list', views.store_list),
    path('store/create', views.store_create),
    path('store/update', views.store_update),
    path('store/delete', views.store_delete),

    #for CASCADING ***********
    path('enterprise/deactivate', views.deactivate_enterprise),
    path('region/deactivate', views.deactivate_region),
    path('circle/deactivate', views.deactivate_circle),
    path('cluster/deactivate', views.deactivate_cluster),
    path('store/delete', views.delete_store),

    # ROLE
    
    path('role/create', views.role_create),
    path('role/update', views.role_update),


    # USER

    path('create-user', create_user),
    path('update-user', update_user),
    path('delete-user', delete_user),
    path('login-user', login_user),
    path('change-password', change_password),

    path("generate-otp", views.generate_and_send_otp),

    path("verify-otp", views.verify_otp),
    path("reset-password", views.reset_password),
]
