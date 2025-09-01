from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Enterprise, Region,Circle,Cluster,Store
from .serializers import EnterpriseSerializer, RegionSerializer,CircleSerializer,ClusterSerializer,StoreSerializer


# ----CREATE Enterprise -----------------
@api_view(['POST'])
def enterprise_create(request):
    serializer = EnterpriseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- LIST Enterprises -----------------
@api_view(['GET'])
def enterprise_list(request):
    enterprises = Enterprise.objects.filter(is_active=True)  # only active records
    serializer = EnterpriseSerializer(enterprises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#-----------UPDATE Enterprise--------

@api_view(['POST'])
def enterprise_update(request):
    enterprise_id = request.data.get("id")  # ID from JSON
    if not enterprise_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        enterprise = Enterprise.objects.get(id=enterprise_id)
    except Enterprise.DoesNotExist:
        return Response({"error": "Enterprise not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EnterpriseSerializer(enterprise, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- DELETE Enterprise(Soft Delete) 
@api_view(['POST'])
def enterprise_delete(request):
    enterprise_id = request.data.get("id")  # ID from JSON
    if not enterprise_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        enterprise = Enterprise.objects.get(id=enterprise_id)
    except Enterprise.DoesNotExist:
        return Response({"error": "Enterprise not found"}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete
    enterprise.is_active = False
    enterprise.save()

    return Response({"message": "Enterprise soft-deleted successfully"}, status=status.HTTP_200_OK)

# =================== REGION VIEWS===================


# GET → list all active regions
@api_view(['GET'])
def region_list(request):
    regions = Region.objects.filter(is_active=True)
    serializer = RegionSerializer(regions, many=True)
    return Response(serializer.data)

# POST → create region
@api_view(['POST'])
def region_create(request):
    serializer = RegionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- UPDATE Region-----------------
@api_view(['POST'])
def region_update(request):
    region_id = request.data.get("id")  # ID from JSON
    if not region_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        region = Region.objects.get(id=region_id)
    except Region.DoesNotExist:
        return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = RegionSerializer(region, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- DELETE Region (Soft Delete) -----------------
@api_view(['POST'])
def region_delete(request):
    region_id = request.data.get("id")  # ID from JSON
    if not region_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        region = Region.objects.get(id=region_id)
    except Region.DoesNotExist:
        return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete
    region.is_active = False
    region.save()

    return Response({"message": "Region soft-deleted successfully"}, status=status.HTTP_200_OK)


#====================Circle Views====================

# GET → list active circles
@api_view(['GET'])
def circle_list(request):
    circles = Circle.objects.filter(is_active=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)

# POST → create circle
@api_view(['POST'])
def circle_create(request):
    serializer = CircleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -            --- UPDATE Circle  ------
@api_view(['POST'])
def circle_update(request):
    circle_id = request.data.get("id")  # ID from JSON
    if not circle_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        return Response({"error": "Circle not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CircleSerializer(circle, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 #---------------- DELETE Circle(Soft Delete) -...
@api_view(['POST'])
def circle_delete(request):
    circle_id = request.data.get("id")  # ID from JSON
    if not circle_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        return Response({"error": "Circle not found"}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete
    circle.is_active = False
    circle.save()

    return Response({"message": "Circle soft-deleted successfully"}, status=status.HTTP_200_OK)


#===========================Cluster View==============

# List active clusters
@api_view(['GET'])
def cluster_list(request):
    clusters = Cluster.objects.filter(is_active=True)
    serializer = ClusterSerializer(clusters, many=True)
    return Response(serializer.data)

# Create cluster
@api_view(['POST'])
def cluster_create(request):
    serializer = ClusterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- UPDATE Cluster 
@api_view(['POST'])
def cluster_update(request):
    cluster_id = request.data.get("id")  # ID from JSON
    if not cluster_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cluster = Cluster.objects.get(id=cluster_id)
    except Cluster.DoesNotExist:
        return Response({"error": "Cluster not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClusterSerializer(cluster, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- DELETE Cluster(Soft Delete) -----------------
@api_view(['POST'])
def cluster_delete(request):
    cluster_id = request.data.get("id")  # ID from JSON
    if not cluster_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cluster = Cluster.objects.get(id=cluster_id)
    except Cluster.DoesNotExist:
        return Response({"error": "Cluster not found"}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete
    cluster.is_active = False
    cluster.save()

    return Response({"message": "Cluster soft-deleted successfully"}, status=status.HTTP_200_OK)


#======================Store View=============

# GET: List active stores
@api_view(['GET'])
def store_list(request):
    stores = Store.objects.filter(is_active=True)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)

# POST: Create store
@api_view(['POST'])
def store_create(request):
    serializer = StoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---- UPDATE Store --
@api_view(['POST'])
def store_update(request):
    store_id = request.data.get("id")  # ID from JSON
    if not store_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StoreSerializer(store, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -- DELETE (Soft Delete) -----------------
@api_view(['POST'])
def store_delete(request):
    store_id = request.data.get("id")  # ID from JSON
    if not store_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete
    store.is_active = False
    store.save()

    return Response({"message": "Store soft-deleted successfully"}, status=status.HTTP_200_OK)



