from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from expenses.models import ExpenseTypes
from rest_framework.pagination import PageNumberPagination
from django.db import transaction

from fee.models import FeeCategory, FeeCollections
from fee.serializers.FeeCategoriesSerializer import FeeCategorySerializer
from fee.serializers.FeeCollectionSerializer import FeeCollectionSerializer
from parents.models import Parents
from students.models import Students
from transactions.models import Transactions, Receipts
from users.permission_filter import allowed_groups
from utils.Helpers import Helpers
import time

from utils.emails import Mailing


class FeeCategoriesView(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                category = FeeCategory.objects.create(
                    name=request.data.get('name'),
                    amount=request.data.get('amount'),
                    school=request.user.schools,
                    description=request.data.get('description')
                )
                return Response({"message": "Category created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @allowed_groups(allowed_groups=['superuser', 'admin', 'accountant'])
    def list(self, request, *args, **kwargs):
        paginate = request.query_params.get('paginate', 'true').lower() == 'true'
        categories = FeeCategory.objects.filter(school=request.user.schools).values()
        if paginate:
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(categories, request)
            if page is not None:
                return paginator.get_paginated_response(page)
        else:
            return Response(categories, status=200)


class FeeView(viewsets.ModelViewSet):
    queryset = FeeCollections.objects.all()
    serializer_class = FeeCollectionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @allowed_groups(allowed_groups=['superuser', 'admin', 'accountant'])
    @transaction.atomic
    def pay_fee(self, request, *args, **kwargs):
        student = get_object_or_404(Students, id=request.data.get('student'))
        parent = get_object_or_404(Parents, id=request.data.get('paid_by'))
        category = get_object_or_404(FeeCategory, id=request.data.get('fee_category'))
        school = request.user.schools
        receipt_number = Helpers().generate_receipt_number()
        current_milliseconds = int(time.time() * 1000)

        # Insert fee
        fee = FeeCollections.objects.create(
            student=student,
            paid_by=parent,
            fee_category=category,
            amountPaid=request.data.get('amountPaid'),
            school=school,
            receipt_number=receipt_number,
            payment_reference=f"CASH{current_milliseconds}",
            payment_type="CR",
            payment_mode="Cash",
        )

        # Insert Transaction
        transaction = Transactions.objects.create(
            amount=request.data.get('amountPaid'),
            ref_number=f"CASH{current_milliseconds}",
            type="CREDIT",
            tran_ref=fee.id,
            tran_category="FEE_PAYMENT",
        )
        # Insert Receipt
        receipt = Receipts.objects.create(
            transaction=transaction,
            file_url=f"https://example.com/receipts/{receipt_number}.jpg",
            receipt_number=receipt_number,
        )

        # @TODO: Populate students balance, include the on the notification, make file downloadable

        # send Notification and Receipt URL
        Mailing().send_payment_confirmation(parent, transaction, receipt)
        return Response({"message": "Payment was successful"}, 201)
