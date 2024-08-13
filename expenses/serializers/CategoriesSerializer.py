from rest_framework import serializers


class ExpenseCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)



