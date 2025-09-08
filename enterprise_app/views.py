from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate
import re
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.http import JsonResponse
from .models import Enterprise, Region, Circle, Cluster, Store,Role,User,PasswordHistory
from .utils import send_test_email,encrypt_email
from .serializers import (
    EnterpriseSerializer, RegionSerializer, CircleSerializer,
    ClusterSerializer, StoreSerializer,RoleSerializer)

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

#--------------Create User------

# Password validation----
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must have at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must have at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must have at least one number"
    if not re.search(r"[!@#$%^&*()_+]", password):
        return False, "Password must have at least one special character"
    return True, ""

# ------------------ CREATE USER ------------------
@api_view(['POST'])
def create_user(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        address = data.get('address', '')
        experience = data.get('experience', 0)
        role_id = data.get('role')
        store_id = data.get('store')
        is_active = data.get('is_active', True)  # can be set in create JSON

        if not all([email, password, first_name, last_name, role_id, store_id]):
            return Response({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password
        valid, msg = validate_password(password)
        if not valid:
            return Response({"message": msg}, status=status.HTTP_400_BAD_REQUEST)

        # Get role and store
        try:
            role = Role.objects.get(id=role_id)
            store = Store.objects.get(id=store_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Store.DoesNotExist:
            return Response({"message": "Store not found"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            address=address,
            experience=experience,
            role=role,
            store=store,
            is_active=is_active
        )

        # Send email
        subject = "Account Created"
        message = f"Hello {first_name},\n\nYour account has been created successfully.\n\nEmail: {email}\nPassword: {password}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------ UPDATE USER ------------------
@api_view(['POST'])
def update_user(request):
    try:
        data = request.data
        email = data.get('email')
        if not email:
            return Response({"message": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Optional fields update
        if 'password' in data:
            valid, msg = validate_password(data['password'])
            if not valid:
                return Response({"message": msg}, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(data['password'])
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'address' in data:
            user.address = data['address']
        if 'experience' in data:
            user.experience = data['experience']
        if 'role' in data:
            try:
                user.role = Role.objects.get(id=data['role'])
            except Role.DoesNotExist:
                return Response({"message": "Role not found"}, status=status.HTTP_400_BAD_REQUEST)
        if 'store' in data:
            try:
                user.store = Store.objects.get(id=data['store'])
            except Store.DoesNotExist:
                return Response({"message": "Store not found"}, status=status.HTTP_400_BAD_REQUEST)

        user.save()
        return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------ SOFT DELETE USER ------------------
@api_view(['POST'])
def delete_user(request):
    try:
        email = request.data.get('email')
        if not email:
            return Response({"message": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"message": "User not found or already inactive"}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = False
        user.save()
        return Response({"message": "User deactivated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------ LOGIN USER ------------------
@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"message": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Login is not successful"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------ PASSWORD CHANGE  ------------------
@api_view(['POST'])
def change_password(request):
    """
    JSON input:
    {
      "email": "user@example.com",
      "old_password": "OldPass@123",
      "new_password": "NewPass@123"
    }
    """
    try:
        data = request.data
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not all([email, old_password, new_password]):
            return Response({"message": "email, old_password and new_password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Find active user
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Verify old password matches current stored password
        if not check_password(old_password, user.password):
            return Response({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate new password strength
        valid, msg = validate_password(new_password)
        if not valid:
            return Response({"message": msg}, status=status.HTTP_400_BAD_REQUEST)

        # New must not be same as current
        if check_password(new_password, user.password):
            return Response({"message": "New password must not match current password"}, status=status.HTTP_400_BAD_REQUEST)

        # Check against recent 3 password history
        recent_history = PasswordHistory.objects.filter(user=user).order_by('-created_on')[:3]
        for hist in recent_history:
            if check_password(new_password, hist.password_hash):
                return Response({"message": "New password must not match any of last 3 passwords"},
                                status=status.HTTP_400_BAD_REQUEST)

        # update inside a transaction
        with transaction.atomic():
            # Hash new password and save to User
            hashed_new = make_password(new_password)
            user.password = hashed_new
            user.save()

            # Create history record for new password
            PasswordHistory.objects.create(user=user, password_hash=hashed_new)

            # Keep only latest 3 entries: delete older if more than 3
            all_history = PasswordHistory.objects.filter(user=user).order_by('-created_on')
            if all_history.count() > 3:
                # get id to delete (oldest ones)
                to_delete = all_history[3:]  # slice: entries after top 3 (older ones)
                # delete 
                ids = [p.id for p in to_delete]
                PasswordHistory.objects.filter(id__in=ids).delete()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
