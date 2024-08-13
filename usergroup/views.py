from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets, status
from rest_framework.response import Response

from usergroup.models import UserGroup
from usergroup.serializers import UserGroupSerializers
from users.models import CustomUser
from users.permission_filter import allowed_users, allowed_groups
from utils.ApiResponse import ApiResponse
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class UserGroupView(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializers
    permission_classes = [IsAuthenticated]

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def list(self, request, *args, **kwargs):
        groups = Group.objects.exclude(name='superuser').order_by("id")
        data = []
        for group in groups:
            group_permissions = group.permissions.all()
            permissions = [
                {"id": perm.id, "name": perm.name, "codename": perm.codename}
                for perm in group_permissions
            ]
            group_users = CustomUser.objects.filter(groups=group)
            users = [
                {
                    "id": user.id,
                    "phone": user.phone_number,
                    "name": f"{user.first_name} {user.last_name}",
                    "gender": user.gender,
                    "date_joined": user.date_joined,
                    "address": user.address,
                    "email": user.email
                }
                for user in group_users
            ]
            group_data = {
                "id": group.id,
                "name": group.name,
                "permissions": permissions,
                "users": users
            }
            data.append(group_data)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, request)
        return paginator.get_paginated_response(page)

    def create(self, request, *args, **kwargs):
        UserGroupData = self.get_serializer(data=request.data)

        if not UserGroupData.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(
                {"message": "Please fill in the details correctly or Group already exists.", "status": status_code},
                status=status_code)

        name = request.data.get("name")
        existingusergroup = Group.objects.filter(name=name).first()

        if existingusergroup:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Group already exists.", "status": status_code}, status=status_code)

        group = UserGroupData.save()
        permission_codenames = [""]
        permissions = Permission.objects.filter(codename__in=permission_codenames)

        group.permissions.add(*permissions)

        return Response(
            {"message": "Group created", "status": status.HTTP_201_CREATED, "data": UserGroupData.data},
            status=status.HTTP_201_CREATED)
