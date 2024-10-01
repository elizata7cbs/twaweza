import os
import time
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from parents.models import Parents
from students.models import VirtualAccounts
from students.models.StudentsModel import Students
from students.models.StudentsParentsModel import StudentsParents
from students.serializers.StudentsViewSerializers import StudentsSerializers
from users.permission_filter import allowed_groups
from utils.Helpers import Helpers
from django.core.files.storage import FileSystemStorage
from core.settings import MEDIA_URL
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.db.models import Q
from schools.models import Schools  # Import the Schools model

class StudentsView(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @allowed_groups(allowed_groups=['superuser', 'admin', 'accountant'])
    def list(self, request, *args, **kwargs):
        paginate = request.query_params.get('paginate', 'true').lower() == 'true'
        students = Students.objects.filter(school=request.user.schools)

        if paginate:
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(students, request)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)

    @allowed_groups(allowed_groups=['superuser', 'admin', 'accountant'])
    def list_unpaginated(self, request, *args, **kwargs):
        students = Students.objects.filter(school=request.user.schools).values()
        return Response(students, 200)

    def update(self, request, *args, **kwargs):
        students_details = Students.objects.get(id=kwargs['pk'])
        students_serializer_data = StudentsSerializers(students_details, data=request.data, partial=True)
        if students_serializer_data.is_valid():
            students_serializer_data.save()
            status_code = status.HTTP_200_OK
            return Response({"message": "Student Updated Successfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Student data Not found", "status": status_code})

    @allowed_groups(allowed_groups=['superuser', 'admin'])
    @transaction.atomic
    def createStudent(self, request):
        # Extract school ID
        school_id = request.data.get('school')
        print(f"Received School ID: {school_id}")  # Debugging line

        # Validate school existence
        if not school_id:
            return Response({"error": "School information not found"}, status=400)

        try:
            school = Schools.objects.get(id=int(school_id))
        except Schools.DoesNotExist:
            return Response({"error": "Invalid school ID"}, status=400)

        unique_number = Helpers().generate_unique_student_id(school)
        admission_number = request.data.get('admNumber')
        urls = []

        # Handle file uploads
        if request.FILES:
            uploaded_files = request.FILES
            upload_dir = os.path.join(MEDIA_URL, "students")
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            for uploaded_file_name, uploaded_file in uploaded_files.items():
                print(uploaded_file_name)
                fs = FileSystemStorage(location=upload_dir)
                filename = fs.save(uploaded_file_name, uploaded_file)
                uploaded_file_path = os.path.join(upload_dir, filename)

                timestamp = str(int(time.time() * 1000))
                file_name, file_extension = os.path.splitext(uploaded_file_name)
                new_filename = f"{admission_number}_{timestamp}{file_extension}"
                new_file_path = os.path.join(upload_dir, new_filename)
                os.rename(uploaded_file_path, new_file_path)

                domain = request.get_host()
                protocol = 'https://' if request.is_secure() else 'http://'
                media_url = f"{protocol}{domain}/{MEDIA_URL}"
                file_url = media_url + 'students/' + new_filename
                urls.append(file_url)

        # Get the first URL or None if no files were uploaded
        url = urls[0] if urls else None

        # Create the student record
        student = Students.objects.create(
            uniqueNumber=unique_number,
            admNumber=admission_number,
            school=school,
            first_name=request.data.get('first_name'),
            middle_name=request.data.get('middle_name'),
            last_name=request.data.get('last_name'),
            gender=request.data.get('gender'),
            dob=request.data.get('dob'),
            date_of_admission=request.data.get('date_of_admission'),
            health_status=request.data.get('health_status'),
            upi_number=request.data.get('upi_number'),
            urls=url
        )

        # Handle parents
        parents_string = request.data.get("parents", "").split(',')
        parents = [int(n.strip()) for n in parents_string if n.strip()]
        for parent_id in parents:
            try:
                parent_obj = Parents.objects.get(id=parent_id)
                StudentsParents.objects.create(
                    parent=parent_obj,
                    student=student
                )
            except Parents.DoesNotExist:
                return Response({"error": f"Parent with ID {parent_id} does not exist"}, status=400)

        # Create virtual account
        VirtualAccounts.objects.create(
            student=student,
            balance=0.00
        )

        return Response({"message": "Student created"}, status=201)

    @allowed_groups(allowed_groups=['superuser', 'admin', 'accountant'])
    def search_student(self, request, *args, **kwargs):
        param = request.query_params.get('param', None)
        print(param)
        if not param:
            return Response({"error": "Search parameter is missing"}, status=400)

        school = request.user.schools
        columns = ['uniqueNumber', 'admNumber', 'first_name', 'middle_name', 'last_name', 'upi_number']
        query = Q()
        for column in columns:
            query |= Q(**{f"{column}__icontains": param})
        students = Students.objects.filter(query, school=school)
        serializer = StudentsSerializers(students, many=True)
        return Response(serializer.data, 200)
