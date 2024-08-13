from rest_framework import serializers
from supportstaffs.models.CategoryModel import SupportCategory


class SupportCategoriesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, allow_null=False)
    # class Meta:
    #     model = SupportCategory
    #     fields = "__all__"



