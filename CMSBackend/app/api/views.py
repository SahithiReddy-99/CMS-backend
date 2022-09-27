import json
from django.contrib import messages, auth
from app.models import User, Employees, Roles
from app.api.serializers import FlatOwnerSerializer, EmployeesSerializer
from django.http import Http404, QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FlatOwnerAV(APIView):

    def get(self, request, format=None):
        owners = User.objects.all()
        serializer = FlatOwnerSerializer(owners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FlatOwnerSerializer(data=request.data)
        password=request.data.get('password')
        confirm_password=request.data.get('confirm_password')
        email=request.data.get('email')
        if serializer.is_valid():
            if not password==confirm_password:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
               serializer.save()
               return Response(  {"Success": "You are now registered and can log in"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlatOwnerDetailsAV(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
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


class EmployeesAV(APIView):
    def get(self, request, format=None):
        employees = Employees.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        roleId = request.data['roleId']
        role = Roles.objects.get(role=roleId)
        data = json.dumps(request.data)
        res=json.loads(data)
        res['roleId'] = role.id

        serializer = EmployeesSerializer(data=res)
        if serializer.is_valid():
            if Employees.objects.filter(email=res['email']).exists():
                messages.error(request, 'That email is being used')
                return Response({"Error": "Email already exists"},
serializer.errors, status=status.HTTP_400_BAD_REQUEST, )

            serializer.save()
            messages.success(request, 'Employee is now registered and can log in')
            return Response(  {"Success": "Employee is now registered and can log in"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
