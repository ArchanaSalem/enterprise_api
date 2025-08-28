from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Enterprise
from .serializers import EnterpriseSerializer
# CREATE
@api_view(['POST'])
def enterprise_create(request):
    serializer = EnterpriseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LIST (only active enterprises)
@api_view(['GET'])
def enterprise_list(request):
    enterprises = Enterprise.objects.filter(is_active=True)
    serializer = EnterpriseSerializer(enterprises, many=True)
    return Response(serializer.data)

# UPDATE
@api_view(['POST'])
def enterprise_update(request, pk):
    try:
        enterprise = Enterprise.objects.get(pk=pk, is_active=True)
    except Enterprise.DoesNotExist:
        return Response({"error": "Enterprise not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EnterpriseSerializer(enterprise, data=request.data, partial=True)  # partial=True → patch-like update
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SOFT DELETE
@api_view(['POST'])
def enterprise_softdelete(request, pk):
    try:
        enterprise = Enterprise.objects.get(pk=pk, is_active=True)
    except Enterprise.DoesNotExist:
        return Response({"error": "Enterprise not found"}, status=status.HTTP_404_NOT_FOUND)

    enterprise.is_active = False
    enterprise.save()
    return Response({"message": "Enterprise soft deleted"})
