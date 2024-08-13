from rest_framework import serializers
from students.models.StudentsModel import Students


class StudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"
