from MySQLdb._mysql import IntegrityError

from supportstaffs.models import SupportStaff, supportAccounts
from supportstaffs.models.CategoryModel import SupportCategory
from supportstaffs.serializers.CategoriesSerializer import SupportCategoriesSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from supportstaffs.serializers.SupportStaffsSerializer import SupportStaffsSerializer
from users.permission_filter import allowed_groups
from django.db import transaction


class SupportCategoryView(viewsets.ModelViewSet):
    queryset = SupportCategory.objects.all()
    serializer_class = SupportCategoriesSerializer
    permission_classes = [IsAuthenticated]

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            SupportCategory.objects.create(
                name=request.data.get('name'),
                school=request.user.schools
            )
            return Response({"message": "Support category created successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle the specific integrity error
            return Response({"message": "Category exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other potential exceptions
            return Response({"message": "Category exists"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pass

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def list(self, request, *args, **kwargs):
        categories = SupportCategory.objects.filter(school=request.user.schools).values()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(categories, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        return Response({"results": list(categories)}, status=200)


class SupportStaffView(viewsets.ModelViewSet):
    queryset = SupportStaff.objects.all()
    serializer_class = SupportStaffsSerializer
    permission_classes = [IsAuthenticated]

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            type = get_object_or_404(SupportCategory, id=request.data.get('type'))
            staff = SupportStaff.objects.create(
                name=request.data.get('name'),
                school=request.user.schools,
                idno=request.data.get('idno'),
                phone_number=request.data.get('phone_number'),
                gender=request.data.get('gender'),
                dob=request.data.get('dob'),
                type=type,
            )

            # set Up Account Number
            account = supportAccounts(
                bankName=request.data.get('bankName'),
                accountNumber=request.data.get('accountNumber'),
                accountName=request.data.get('accountName'),
                staff=staff
            )
            account.save()

            return Response({"message": "Staff created successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle the specific integrity error
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other potential exceptions
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pass

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def list(self, request, *args, **kwargs):
        staffs = SupportStaff.objects.filter(school=request.user.schools).select_related('type').prefetch_related(
            'supportaccounts_set')

        staff_list = []
        for staff in staffs:
            staff_data = {
                "id": staff.id,
                "name": staff.name,
                "idno": staff.idno,
                "phone_number": staff.phone_number,
                "gender": staff.gender,
                "status": staff.status,
                "dob": staff.dob,
                "type": {
                    "id": staff.type.id,
                    "name": staff.type.name
                },
                "account": [
                    {
                        "bankName": account.bankName,
                        "accountNumber": account.accountNumber,
                        "accountName": account.accountName
                    }
                    for account in staff.supportaccounts_set.all()
                ]
            }
            staff_list.append(staff_data)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(staff_list, request)

        if page is not None:
            return paginator.get_paginated_response(page)

        return Response({"results": staff_list}, status=200)




