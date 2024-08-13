from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from parents.models import Parents
from parents.serializers import ParentsCreateSerializers, ParentsLoginSerializers
from users.permission_filter import allowed_groups
from utils.Helpers import Helpers
from utils.ApiResponse import ApiResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.contrib.auth.hashers import make_password

from utils.emails import Mailing
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ParentViewSet(ModelViewSet):
    queryset = Parents.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'login':
            return ParentsLoginSerializers
        return ParentsCreateSerializers

    @action(detail=False, methods=['POST'], url_path='login', url_name='login')
    def login(self, request):
        serializer = ParentsLoginSerializers(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            helpers = Helpers()
            helpers.log(request)
            if username and password:
                try:
                    parent = Parents.objects.get(username=username)
                    if parent.check_password(password):
                        parent_data = ParentsCreateSerializers(parent).data
                        response = ApiResponse()
                        response.setStatusCode(status.HTTP_200_OK)
                        response.setMessage("Login successful")
                        response.setEntity(parent_data)
                        return Response(response.toDict(), status=response.status)
                    else:
                        response = ApiResponse()
                        response.setStatusCode(status.HTTP_400_BAD_REQUEST)
                        response.setMessage("Incorrect login credentials")
                        return Response(response.toDict(), status=200)
                except Parents.DoesNotExist:
                    response = ApiResponse()
                    response.setStatusCode(status.HTTP_400_BAD_REQUEST)
                    response.setMessage("Incorrect login credentials")
                    return Response(response.toDict(), status=200)
            else:
                response = ApiResponse()
                response.setStatusCode(status.HTTP_400_BAD_REQUEST)
                response.setMessage("Username and password are required")
                return Response(response.toDict(), status=response.status)
        else:
            response = ApiResponse()
            response.setStatusCode(status.HTTP_400_BAD_REQUEST)
            response.setMessage("Invalid data")
            return Response(response.toDict(), status=response.status)

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def list(self, request, *args, **kwargs):
        parents = Parents.objects.filter(school=request.user.schools)
        serializer = ParentsCreateSerializers(parents, many=True)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(page)

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    @transaction.atomic
    def create(self, request):
        username = request.data.get('phone_number')
        password = request.data.get('phone_number')
        school = request.user.schools

        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        parent_idno = request.data.get('parent_idno')

        # Check if email already exists
        if Parents.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if phone number already exists
        if Parents.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if parent ID number already exists
        if Parents.objects.filter(parent_idno=parent_idno).exists():
            return Response({"error": "Parent ID number already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create parent
        parent = Parents.objects.create(
            email=email,
            username=username,
            password=make_password(password),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            parent_idno=parent_idno,
            school=school,
            phone_number=phone_number,
            parentType=request.data.get('parentType'),
        )
        mailer = Mailing().welcome_new_user_email(parent, username, password)
        return Response({"message": "Parent created"}, status=status.HTTP_201_CREATED)



