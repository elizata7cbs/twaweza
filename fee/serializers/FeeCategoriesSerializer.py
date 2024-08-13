from rest_framework import serializers


class FeeCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    amount = serializers.FloatField()
    description = serializers.CharField(max_length=255)



