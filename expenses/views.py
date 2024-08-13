from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from expenses.models import ExpenseTypes
from rest_framework.pagination import PageNumberPagination
from django.db import transaction

from expenses.serializers.CategoriesSerializer import ExpenseCategorySerializer
from users.permission_filter import allowed_groups


class ExpenseCategoriesView(viewsets.ModelViewSet):
    queryset = ExpenseTypes.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                category = ExpenseTypes.objects.create(
                    name=request.data.get('name'),
                    school=request.user.schools,
                    description=request.data.get('description')
                )
                return Response({"message": "Category created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        categories = ExpenseTypes.objects.filter(school=request.user.schools).values()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(categories, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        return Response({"results": categories}, status=200)
