from rest_framework import serializers


class FeeCollectionSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    paid_by = serializers.IntegerField()
    fee_category = serializers.IntegerField()
    amountPaid = serializers.FloatField()
    payment_mode = serializers.CharField()



