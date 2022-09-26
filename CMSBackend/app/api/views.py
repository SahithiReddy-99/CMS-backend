from app.models import FlatOwner
from app.api.serializers import FlatOwnerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FlatOwnerAV(APIView):

    def get(self, request, format=None):
        owners = FlatOwner.objects.all()
        serializer = FlatOwnerSerializer(owners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FlatOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlatOwnerDetailsAV(APIView):

    def get_object(self, pk):
        try:
            return FlatOwner.objects.get(pk=pk)
        except FlatOwner.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        owner = self.get_object(pk)
        serializer = FlatOwnerSerializer(owner)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        owner = self.get_object(pk)
        serializer = FlatOwnerSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        owner = self.get_object(pk)
        owner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
