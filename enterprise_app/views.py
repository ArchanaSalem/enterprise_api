from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.http import JsonResponse
from .models import Enterprise, Region, Circle, Cluster, Store,Role,User
from .utils import send_test_email
from .serializers import (
    EnterpriseSerializer, RegionSerializer, CircleSerializer,
    ClusterSerializer, StoreSerializer,RoleSerializer,UserSerializer)

# #########
# Cascading function
# -------------------------------
def set_active_status(obj, active):
    obj.is_active = active
    obj.save()

    for region in getattr(obj, 'region_set', []):
        region.is_active = active
        region.save()

        for circle in getattr(region, 'circle_set', []):
            circle.is_active = active
            circle.save()

            for cluster in getattr(circle, 'cluster_set', []):
                cluster.is_active = active
                cluster.save()

                for store in getattr(cluster, 'store_set', []):
                    store.is_active = active
                    store.save()

# ----------------
# Deactivation / Deletion Endpoints (JSON input)
# ------

@api_view(['POST'])
def deactivate_enterprise(request):
    enterprise_id = request.data.get('enterprise_id')
    if not enterprise_id:
        return Response({"error": "enterprise_id is required"}, status=400)
    try:
        enterprise = Enterprise.objects.get(id=enterprise_id)
    except Enterprise.DoesNotExist:
        return Response({"error": "Enterprise not found"}, status=404)
    set_active_status(enterprise, False)
    return Response({'detail': 'Enterprise and all children deactivated'})


@api_view(['POST'])
def deactivate_region(request):
    region_id = request.data.get('region_id')
    if not region_id:
        return Response({"error": "region_id is required"}, status=400)
    try:
        region = Region.objects.get(id=region_id)
    except Region.DoesNotExist:
        return Response({"error": "Region not found"}, status=404)
    set_active_status(region, False)
    return Response({'detail': 'Region and all its children deactivated'})


@api_view(['POST'])
def deactivate_circle(request):
    circle_id = request.data.get('circle_id')
    if not circle_id:
        return Response({"error": "circle_id is required"}, status=400)
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        return Response({"error": "Circle not found"}, status=404)
    set_active_status(circle, False)
    return Response({'detail': 'Circle and all its children deactivated'})


@api_view(['POST'])
def deactivate_cluster(request):
    cluster_id = request.data.get('cluster_id')
    if not cluster_id:
        return Response({"error": "cluster_id is required"}, status=400)
    try:
        cluster = Cluster.objects.get(id=cluster_id)
    except Cluster.DoesNotExist:
        return Response({"error": "Cluster not found"}, status=404)
    set_active_status(cluster, False)
    return Response({'detail': 'Cluster and its stores deactivated'})


@api_view(['DELETE'])
def delete_store(request):
    store_id = request.data.get('store_id')
    if not store_id:
        return Response({"error": "store_id is required"}, status=400)
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=404)
    store.delete()
    return Response({'detail': 'Store deleted'})

# ---- ENTERPRISE ----------=---- #
@api_view(['GET'])
def enterprise_list(request):
    enterprise = Enterprise.objects.filter(is_active=True).order_by('-updated_on', '-created_on')

    # Substring search on name
    search_query = request.GET.get('name', '')
    if search_query:
        enterprise = enterprise.filter(name__icontains=search_query)

    # Pagination
    paginator = PageNumberPagination()
    page_size = request.GET.get('size')  # get page size from request
    paginator.page_size = int(page_size) if page_size else 5  # default 5
    result_page = paginator.paginate_queryset(enterprise, request)

    # Serializer (keep your existing nested cascade serializer)
    serializer = EnterpriseSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


   
@api_view(['POST'])
def enterprise_create(request):
    serializer = EnterpriseSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response(EnterpriseSerializer(obj).data, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def enterprise_update(request):
    pk = request.data.get('id')
    if not pk:
        return Response({"error": "id is required"}, status=400)
    try:
        obj = Enterprise.objects.get(pk=pk, is_active=True)
    except Enterprise.DoesNotExist:
        return Response({"error": f"Enterprise with ID {pk} not found"}, status=404)
    update_data = request.data.copy()
    update_data.pop('id', None)
    serializer = EnterpriseSerializer(obj, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"errors": serializer.errors}, status=400)

@api_view(['POST'])
def enterprise_delete(request):
    pk = request.data.get('id')
    try:
        obj = Enterprise.objects.get(pk=pk, is_active=True)
        obj.is_active = False
        obj.save()
        return Response({str(pk): "Enterprise soft deleted successfully"})
    except Enterprise.DoesNotExist:
        return Response({"error": f"Enterprise with ID {pk} not found or already deleted"}, status=404)


# ------- REGION ----
@api_view(['GET'])
def region_list(request):
    regions = Region.objects.filter(is_active=True).order_by('-updated_on', '-created_on')

    # Substring search on name
    search_query = request.GET.get('name', '')
    if search_query:
        regions = regions.filter(name__icontains=search_query)

    # Pagination
    paginator = PageNumberPagination()
    page_size = request.GET.get('size')
    paginator.page_size = int(page_size) if page_size else 5
    result_page = paginator.paginate_queryset(regions, request)

    serializer = RegionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data) 


@api_view(['POST'])
def region_create(request):
    serializer = RegionSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response(RegionSerializer(obj).data, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def region_update(request):
    pk = request.data.get('id')
    if not pk:
        return Response({"error": "id is required"}, status=400)
    try:
        obj = Region.objects.get(pk=pk, is_active=True)
    except Region.DoesNotExist:
        return Response({"error": f"Region with ID {pk} not found"}, status=404)
    update_data = request.data.copy()
    update_data.pop('id', None)
    serializer = RegionSerializer(obj, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"errors": serializer.errors}, status=400)

@api_view(['POST'])
def region_delete(request):
    pk = request.data.get('id')
    try:
        obj = Region.objects.get(pk=pk, is_active=True)
        obj.is_active = False
        obj.save()
        return Response({str(pk): "Region soft deleted successfully"})
    except Region.DoesNotExist:
        return Response({"error": f"Region with ID {pk} not found or already deleted"}, status=404)


# ------- CIRCLE ----- #

@api_view(['GET'])
def circle_list(request):
    circles = Circle.objects.filter(is_active=True).order_by('-updated_on', '-created_on')

    # Substring search on name
    search_query = request.GET.get('name', '')
    if search_query:
        circles = circles.filter(name__icontains=search_query)

    # Pagination
    paginator = PageNumberPagination()
    page_size = request.GET.get('size')
    paginator.page_size = int(page_size) if page_size else 5
    result_page = paginator.paginate_queryset(circles, request)

    serializer = CircleSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)




@api_view(['POST'])
def circle_create(request):
    serializer = CircleSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response(CircleSerializer(obj).data, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def circle_update(request):
    pk = request.data.get('id')
    if not pk:
        return Response({"error": "id is required"}, status=400)
    try:
        obj = Circle.objects.get(pk=pk, is_active=True)
    except Circle.DoesNotExist:
        return Response({"error": f"Circle with ID {pk} not found"}, status=404)
    update_data = request.data.copy()
    update_data.pop('id', None)
    serializer = CircleSerializer(obj, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"errors": serializer.errors}, status=400)

@api_view(['POST'])
def circle_delete(request):
    pk = request.data.get('id')
    try:
        obj = Circle.objects.get(pk=pk, is_active=True)
        obj.is_active = False
        obj.save()
        return Response({str(pk): "Circle soft deleted successfully"})
    except Circle.DoesNotExist:
        return Response({"error": f"Circle with ID {pk} not found or already deleted"}, status=404)


# ----- CLUSTER-------------- #

@api_view(['GET'])
def cluster_list(request):
    clusters = Cluster.objects.filter(is_active=True).order_by('-updated_on', '-created_on')

    # Substring search on name
    search_query = request.GET.get('name', '')
    if search_query:
        clusters = clusters.filter(name__icontains=search_query)

    # Pagination
    paginator = PageNumberPagination()
    page_size = request.GET.get('size')
    paginator.page_size = int(page_size) if page_size else 5
    result_page = paginator.paginate_queryset(clusters, request)

    serializer = ClusterSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)



@api_view(['POST'])
def cluster_create(request):
    serializer = ClusterSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response(ClusterSerializer(obj).data, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cluster_update(request):
    pk = request.data.get('id')
    if not pk:
        return Response({"error": "id is required"}, status=400)
    try:
        obj = Cluster.objects.get(pk=pk, is_active=True)
    except Cluster.DoesNotExist:
        return Response({"error": f"Cluster with ID {pk} not found"}, status=404)
    update_data = request.data.copy()
    update_data.pop('id', None)
    serializer = ClusterSerializer(obj, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"errors": serializer.errors}, status=400)

@api_view(['POST'])
def cluster_delete(request):
    pk = request.data.get('id')
    try:
        obj = Cluster.objects.get(pk=pk, is_active=True)
        obj.is_active = False
        obj.save()
        return Response({str(pk): "Cluster soft deleted successfully"})
    except Cluster.DoesNotExist:
        return Response({"error": f"Cluster with ID {pk} not found or already deleted"}, status=404)


# ------------ STORE ---
@api_view(['GET'])
def store_list(request):
    stores = Store.objects.filter(is_active=True).order_by('-updated_on', '-created_on')

    # Substring search on name
    search_query = request.GET.get('name', '')
    if search_query:
        stores = stores.filter(name__icontains=search_query)

    # Pagination
    paginator = PageNumberPagination()
    page_size = request.GET.get('size')
    paginator.page_size = int(page_size) if page_size else 5
    result_page = paginator.paginate_queryset(stores, request)

    serializer = StoreSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def store_create(request):
    serializer = StoreSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response(StoreSerializer(obj).data, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def store_update(request):
    pk = request.data.get('id')
    if not pk:
        return Response({"error": "id is required"}, status=400)
    try:
        obj = Store.objects.get(pk=pk, is_active=True)
    except Store.DoesNotExist:
        return Response({"error": f"Store with ID {pk} not found"}, status=404)
    update_data = request.data.copy()
    update_data.pop('id', None)
    serializer = StoreSerializer(obj, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"errors": serializer.errors}, status=400)

@api_view(['POST'])
def store_delete(request):
    pk = request.data.get('id')
    try:
        obj = Store.objects.get(pk=pk, is_active=True)
        obj.is_active = False
        obj.save()
        return Response({str(pk): "Store soft deleted successfully"})
    except Store.DoesNotExist:
        return Response({"error": f"Store with ID {pk} not found or already deleted"}, status=404)

# ------- CREATE ROLE ----------------

# Create Role
@api_view(['POST'])
def role_create(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Role created", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Role
@api_view(['POST'])
def role_update(request):
    role_id = request.data.get('id')
    if not role_id:
        return Response({"detail": "Role ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        instance = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        return Response({"detail": "Role not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoleSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Role updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#--------------Create User---------

@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save user and get the created user instance
        user = serializer.save()

        # Trigger email after user creation
        subject = "Welcome to Our Platform"
        message = f"Hello {user.first_name},\n\nYour account has been created successfully!"
        send_test_email(user.email, subject, message)  # TO email from user input

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#..............Update User--------

@api_view(['POST'])
def user_update(request):
    try:
        user = User.objects.get(id=request.data.get("id"), is_active=True)
    except User.DoesNotExist:
        return Response({"error": "Active user not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#,,,,,,,UserStoreRole ku views==========
@api_view(['POST'])
def assign_user_role_store(request):
    serializer = UserStoreRoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#'''''''''Removing Userstorerole''''''

@api_view(['POST'])
def remove_user_role_store(request):
    try:
        obj = UserStoreRole.objects.get(id=request.data.get('id'))
        obj.is_active = False
        obj.save()
        return Response({"message": "Assignment deactivated"}, status=status.HTTP_200_OK)
    except UserStoreRole.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Send test Email

def send_email_view(request):
    to_email = 'recipient@example.com'
    subject = 'Test Email from Django'
    message = 'Hello! This is a test email from Archana Ramesh to your Django app'

    send_test_email(to_email, subject, message)

    return JsonResponse({'status': 'Email sent successfully'})


