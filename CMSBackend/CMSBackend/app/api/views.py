from distutils import errors
import json

from django.contrib import messages, auth
from app.models import User, Roles,Reviews
from app.api.serializers import FlatOwnerSerializer, RegistrationSerializer,ReviewSerializer
from django.http import Http404, QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


from rest_framework.parsers import FileUploadParser

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
import random
import re
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes

# from .permissions import IsAdminOrLoggedInUser, LoggedInUserOrAdminOnly
#

def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in
                   range(length))



class FlatOwnerAV(APIView):
    # permission_classes = (IsAuthenticated,)

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

class UserLogin(APIView):
    def post(self,request,format=None):
        serializer = RegistrationSerializer(data=request.data)
        email=request.data.get('email')
        password=request.data.get('password')
        if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            return JsonResponse({'error': 'Enter a valid email'})

        if len(password) < 3:
            return JsonResponse({'error': 'Password needs to be at least of 3 char'})

        # UserModel = get_user_model()

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if password == user.password:
                token = generate_session_token()
                user.session_token = token
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return JsonResponse({'token': token.key, 'user': user, 'status': 200})
            else:
                return JsonResponse({'error': 'Invalid password', 'status': 404})





        # try:
        #
        #     user = UserModel.objects.get(email=email)
        #
        #     if user.check_password(password):
        #         usr_dict = UserModel.objects.filter(
        #             email=email).values().first()
        #         usr_dict.pop('password')
        #         token = generate_session_token()
        #         user.session_token = token
        #         user.save()
        #         token, _ = Token.objects.get_or_create(user=user)
        #         login(request, user)
        #         return JsonResponse({'token': token.key, 'user': usr_dict, 'status': 200})
        #     else:
        #         return JsonResponse({'error': 'Invalid password', 'status': 404})
        #
        # except UserModel.DoesNotExist:
        #     return JsonResponse({'error': 'Invalid Email'})


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegistrationSerializer(data=request.data)
        if reg_serializer.is_valid():
            newUser = reg_serializer.save()
            if newUser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





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


# class EmployeesAV(APIView):
#     def get(self, request, format=None):
#         employees = User.objects.all()
#         serializer = EmployeesSerializer(employees, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         roleId = request.data['roleId']
#         role = Roles.objects.get(role=roleId)
#         data = json.dumps(request.data)
#         res=json.loads(data)
#         res['roleId'] = role.id
#
#         serializer = EmployeesSerializer(data=res)
#         if serializer.is_valid():
#             if Employees.objects.filter(email=res['email']).exists():
#                 messages.error(request, 'That email is being used')
#                 return Response({"Error": "Email already exists"},
# serializer.errors, status=status.HTTP_400_BAD_REQUEST, )

        #     serializer.save()
        #     messages.success(request, 'Employee is now registered and can log in')
        #     return Response(  {"Success": "Employee is now registered and can log in"}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsAV(APIView):
    def get(self, request, format=None):
        owners = Reviews.objects.all()
        serializer = ReviewSerializer(owners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        # password=request.data.get('password')
        # confirm_password=request.data.get('confirm_password')
        # email=request.data.get('email')
        if serializer.is_valid():
               serializer.save()
               return Response(  {"Success": "You review is now added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterReviewsAV(APIView):
    
    def post(self, request, format=None):
        
        user_email=request.data.get('email')
        user=User.objects.filter(email=user_email)
        response=Reviews.objects.filter(email=user)
        response=json.dumps(response)
        response=json.loads(response)
        if response:
            return JsonResponse(response)
        return Response("failed",status=404)