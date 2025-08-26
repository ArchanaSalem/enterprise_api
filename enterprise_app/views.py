from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Enterprise
from .serializers import EnterpriseSerializer

class EnterprisePostView(APIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get("action")

        # CREATE
        if action == "create":
            enterprises_data = request.data.get("enterprises")

            if enterprises_data:  # multiple enterprises
                serializer = EnterpriseSerializer(data=enterprises_data, many=True)
            else:  # single enterprise
                serializer = EnterpriseSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # UPDATE
        elif action == "update":
            try:
                enterprise = Enterprise.objects.get(id=request.data.get("id"))
            except Enterprise.DoesNotExist:
                return Response({"detail": "No Enterprise matches the given query."},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = EnterpriseSerializer(enterprise, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # DELETE
        elif action == "delete":
            try:
                enterprise = Enterprise.objects.get(id=request.data.get("id"))
                enterprise.delete()
                return Response({"detail": "Enterprise deleted successfully."},
                                status=status.HTTP_204_NO_CONTENT)
            except Enterprise.DoesNotExist:
                return Response({"detail": "No Enterprise matches the given query."},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
