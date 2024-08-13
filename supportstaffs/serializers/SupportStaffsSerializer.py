from rest_framework import serializers


class SupportStaffsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    idno = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=10)
    dob = serializers.CharField(max_length=100)
    type = serializers.IntegerField()
    bankName = serializers.CharField(max_length=100)
    accountNumber = serializers.CharField(max_length=200)
    accountName = serializers.CharField(max_length=200)



