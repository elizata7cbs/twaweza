import random
import string

from django.contrib.auth.models import Group, Permission
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.permission_filter import allowed_users, allowed_groups
from users.serializers.LoginViewSerializer import LoginViewSerializer
from users.serializers.MyTokenObtainSerializer import MyTokenObtainPairSerializer
from users.serializers.givepermissionsserializer import givePermissionsSerializer
from users.serializers.serializers import CustomUserSerializer
from users.serializers.userpermissionserializer import PermissionsSerializer
from utils.ApiResponse import ApiResponse

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

from utils.emails import Mailing


class CustomUserView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def list(self, request, *args, **kwargs):
        data = CustomUser.objects.filter(schools=request.user.schools)
        modified_data = []
        for instance in data:
            roles = [group.name for group in instance.groups.all()]

            modified_object = {
                "id": instance.id,
                "date_joined": instance.date_joined,
                "last_login": instance.last_login,
                "is_superuser": instance.is_superuser,
                "is_staff": instance.is_staff,
                "is_active": instance.is_active,
                "username": instance.username,
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "middle_name": instance.middle_name,
                "gender": instance.gender,
                "date_of_birth": instance.date_of_birth,
                "nationality": instance.nationality,
                "address": instance.address,
                "school_name": instance.schools.name,
                "roles": roles,
            }
            modified_data.append(modified_object)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(modified_data, request)
        return paginator.get_paginated_response(page)

    # @permission_classes([IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_permissions = instance.user_permissions.all()  # Accessing user_permissions through the instance
        roles = [permission.name for permission in user_permissions]
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['group'] = instance.usergroup.name
        data['school'] = instance.schools.name
        data['roles'] = roles
        return Response(data)

    def generate_unique_username(self, first_name, last_name):
        base_username = f"{first_name}.{last_name}".lower()
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def generate_random_password(self, length=16):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Email is already in use.", "status": status_code}, status_code)
        # Generate a unique username
        username = self.generate_unique_username(request.data.get('first_name'), request.data.get('last_name'))
        # Generate a random password
        password = self.generate_random_password()
        try:
            with transaction.atomic():
                # Create the user
                group = Group.objects.get(id=request.data.get('usergroup'))

                user = CustomUser.objects.create(
                    username=username,
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    middle_name=request.data.get('middle_name'),
                    gender=request.data.get('gender'),
                    date_of_birth=request.data.get('date_of_birth'),
                    nationality=request.data.get('nationality'),
                    address=request.data.get('address'),
                    email=email,
                    usergroup=group,
                    password=make_password(password),
                    schools=request.user.schools
                )
                # Add the user to the group

                user.groups.add(group)
                Mailing().welcome_new_user_email(user, username, password)

        except Exception as e:
            print(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response({"message": "An error occurred during user creation.", "error": str(e)}, status=status_code)

        return Response({"message": "User created", "username": username, "password": password},
                        status=status.HTTP_201_CREATED)

    def change_password(self, request):
        user_id = request.data.get("userid")
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")
        confirm_password = request.data.get("confirmPassword")

        if not user_id or not old_password or not new_password or not confirm_password:
            return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)

        if not check_password(old_password, user.password):
            return Response({"message": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"message": "New password and confirmation password do not match."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.first_login = False
        user.save()

        refresh = MyTokenObtainPairSerializer.get_token(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            "message": "Password changed successfully.",
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        userData = CustomUser.objects.filter(id=kwargs['pk'])
        if userData:
            userData.delete()
            status_code = status.HTTP_200_OK
            return Response({"message": "CustomUser deleted Successfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "CustomUser data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        customuser_details = self.get_object()  # Get the object to be updated
        customuser_serializer_data = CustomUserSerializer(
            customuser_details, data=request.data, partial=True)  # Allow partial updates

        if customuser_serializer_data.is_valid():
            customuser_serializer_data.save()
            status_code = status.HTTP_200_OK  # Use HTTP_200_OK for successful update
            return Response({
                "message": "User's data updated successfully",
                "status": status_code,
                "data": customuser_serializer_data.data  # Return the updated data
            })
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                "message": "Validation failed",
                "status": status_code,
                "errors": customuser_serializer_data.errors  # Include validation errors in response
            })

    def filter_users(self, request, *args, **kwargs):
        columns = ['usergroup__name', 'username', 'email', 'id']  # Use '__' for traversing relationships
        search_param = kwargs.get('str', '')

        filters = Q()
        for column in columns:
            filters |= Q(**{f"{column}__icontains": search_param})

        # Applying filters to the queryset
        user_data = CustomUser.objects.filter(filters)

        if user_data.exists():
            # Fetch additional related data using annotations
            user_data = user_data.annotate(
                school_name=F('schools__name'),
                usergroup_name=F('usergroup__name')
            ).values('id', 'username', 'email', 'school_name', 'usergroup_name', 'date_joined', 'last_login',
                     'is_superuser', 'is_staff',
                     'is_active', 'password', 'first_name', 'last_name', 'gender', 'nationality', 'address',
                     'middle_name')

            response = {
                "message": "Records retrieved",
                "status_code": 200,
                "data": list(user_data)
            }
        else:
            response = {
                "message": "No records found for the provided search criteria",
                "status_code": 404,
                "data": []
            }

        return Response(response, status=status.HTTP_200_OK if user_data.exists() else status.HTTP_404_NOT_FOUND)

    def deactivate(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            user = CustomUser.objects.get(email=email)
            serializer = CustomUserSerializer(instance=user, data={'is_active': False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User deactivated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message": "CustomUser not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_profile(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk')
            user = get_object_or_404(CustomUser, id=user_id)

            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User profile updated successfully.", "status": status.HTTP_200_OK})
            else:
                return Response({"message": "Invalid data provided.", "status": status.HTTP_400_BAD_REQUEST})

        except CustomUser.DoesNotExist:
            return Response({"message": "User not found.", "status": status.HTTP_404_NOT_FOUND})
        except Exception as e:
            return Response({"message": "An error occurred.", "status": status.HTTP_500_INTERNAL_SERVER_ERROR})


class PermissionsView(viewsets.ModelViewSet):
    serializer_class = PermissionsSerializer

    def list(self, request, *args, **kwargs):
        permissions = Permission.objects.all()
        p = []
        for perm in permissions:
            permissionData = {
                "name": perm.name,
                "content_type": perm.content_type.name,
                "codename": perm.codename,
                "id": perm.id

            }
            p.append(permissionData)
        response = ApiResponse()
        response.setStatusCode(status.HTTP_200_OK)
        response.setMessage("Found")
        response.setEntity(p)
        return Response(response.toDict(), status=response.status)

    def create(self, request, *args, **kwargs):
        response = ApiResponse()
        permissionsData = PermissionsSerializer(data=request.data)

        if not permissionsData.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill in the details correctly.", "status": status_code}, status_code)

        # Check if the name is already in use
        name = request.data.get("name")
        existing_permission = Permission.objects.filter(name=name).first()

        if existing_permission:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Name is already in use.", "status": status_code}, status_code)

        # If name is not in use, save the new permission
        permission = permissionsData.save()

        response.setStatusCode(status.HTTP_201_CREATED)
        response.setMessage("Created")
        response.setEntity(permissionsData.data)  # Use userData.data instead of request.data
        return Response(response.toDict(), status=status.HTTP_201_CREATED)

    def give_permissions(self, request):
        serializer = givePermissionsSerializer(data=request.data)
        if serializer.is_valid():
            group_name = serializer.validated_data.get('name')
            permission_ids = serializer.validated_data.get('permissions')

            try:
                group = Group.objects.get(name=group_name)
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.add(*permissions)
                return Response({"message": "Permissions added successfully."}, status=status.HTTP_200_OK)
            except Group.DoesNotExist:
                return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    serializer_class = LoginViewSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        return Response({'email': user.email}, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
