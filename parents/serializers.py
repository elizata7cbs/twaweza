import random
import string
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from parents.models import Parents
from utils.Helpers import Helpers


class ParentsCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parents
        exclude = ["username", "password", "school", "first_login"]


class ParentsLoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
