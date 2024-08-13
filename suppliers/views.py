from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from suppliers.models import Suppliers
from suppliers.serializers.SuppliersSerializer import SuppliersSerializers
from django.db import transaction
from users.permission_filter import allowed_groups


class SuppliersView(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializers
    permission_classes = [IsAuthenticated]

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        school = request.user.schools
        Suppliers.objects.create(
            supplierName=request.data.get('supplierName'),
            idno=request.data.get('idno'),
            supplierEmail=request.data.get('contactEmail'),
            supplierPhone=request.data.get('contactPhoneNumber'),
            supplierAddress=request.data.get('supplierAddress'),
            supplierWebsite=request.data.get('supplierWebsite'),
            businessName=request.data.get('businessName'),
            school=school,
            businessRegistrationNumber=request.data.get('businessRegistrationNumber'),
            kra=request.data.get('kra'),
            industry=request.data.get('industry'),
            productServices=request.data.get('productServices'),
            payment_mode=request.data.get('payment_mode'),
            bankName=request.data.get('bankName'),
            accountName=request.data.get('accountName'),
            accountNumber=request.data.get('accountNumber'),
            mpesaName=request.data.get('mpesaName'),
            mpesaNumber=request.data.get('mpesaNumber'),
            openingBalance=request.data.get('openingBalance'),
            paymentInterval=request.data.get('paymentInterval')
        )
        return Response({"message": "Supplier Created"}, status=status.HTTP_201_CREATED)

    @allowed_groups(allowed_groups=['superuser', 'admin', 'accountant'])
    def list(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        suppliers = Suppliers.objects.filter(school=request.user.schools)
        page = paginator.paginate_queryset(suppliers, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
