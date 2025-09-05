from django.urls import path
from . import views
from .views import user_create

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
    path('users/create', views.user_create),
    path('users/update', views.user_update),


    path('users/create/', user_create), 
]
    





