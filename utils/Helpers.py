import os
import django

from schools.models import Schools
from students.models import Students
from transactions.models import Receipts

# Manually configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
import os
import random

from core.settings import BASE_DIR
from datetime import timedelta, datetime, date

class Helpers:

    def __init__(self):
        self.schools_counter = {}

    def generateSchoolCode(self, name):
        while True:
            splitted_name = name.split(' ')
            initials = ''.join([n[0] for n in splitted_name]).upper()

            if initials not in self.schools_counter:
                self.schools_counter[initials] = 1

            primary_key = str(self.schools_counter[initials]).zfill(3)
            self.schools_counter[initials] += 1

            school_code = f"{initials}-{primary_key}"

            # Check if the generated code already exists in the database
            if not Schools.objects.filter(school_code=school_code).exists():
                return school_code

    def generateSchoolId(self):
        pass

    # create school code
    def generateSchoolId(self, school_name, country_code):
        """Generates a unique school code based on name and country code, with validation.

        Args:
            school_name: The name of the school.
            country_code: The country code of the school.

        Returns:
            A unique school code string if successful, None otherwise.
        """

        # Validate school name format (optional, adjust as needed)
        if not school_name or not school_name.isalnum() or len(school_name) > 50:
            return None  # Invalid school name format

        # Validate country code format (alphanumeric, 2-3 characters)
        if not country_code or not country_code.isalnum() or len(country_code) not in [2, 3]:
            return None  # Invalid country code format

        # Generate the base school code
        school_code = self.generate_base_code(school_name, country_code)

        # Check for uniqueness in the database
        while Schools.objects.filter(school_code=school_code).exists():
            # If a duplicate is found, increment the count and regenerate
            count = int(school_code.split('-')[-1])  # Extract the count from the code
            school_code = self.generate_base_code(school_name, country_code, count + 1)

        return school_code

    def generateUniqueId(self, schoolCode, admNumber):
        unique = f'{schoolCode}-{admNumber}'
        return str(unique)

    def generatecategorycode(self, name, description):
        categorycode = f'{name}-{description}'
        return categorycode



    def generate_reference(self, paymentmode, payment_date):
        reference = f'{paymentmode}-{payment_date}'
        return reference

    def calculate_balance(self, debit, credit):
        # Calculate the balance before saving
        balance = debit - credit
        return balance

    def generateUniqueexpenseid(self):
        pass

    def generateUniquefeepaymentid(self):
        pass





    def generateotp(self):
        characters = "0123456789"
        otp = ''.join(random.choice(characters) for _ in range(6))
        return otp

    def log(self, request):
        current_date = datetime.now().strftime('%Y.%m.%d')
        log_file_name = f"{current_date}-request.log"
        log_dir = os.path.join(BASE_DIR, 'utils/logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, log_file_name)
        log_string = f"[{datetime.now().strftime('%Y.%m.%d %I.%M.%S %p')}] => method: {request.method} uri: {request.path} queryString: {request.GET.urlencode()} protocol: {request.scheme} remoteAddr: {request.META.get('REMOTE_ADDR')} remotePort: {request.META.get('REMOTE_PORT')} userAgent: {request.META.get('HTTP_USER_AGENT')}"
        if os.path.exists(log_file_path):
            mode = 'a'
        else:
            mode = 'w'
        with open(log_file_path, mode) as log_file:
            log_file.write(log_string + '\n')


    def generate_unique_student_id(self, school):
        current_year = datetime.now().year
        schools = Students.objects.filter(school=school)
        if schools.count() == 0:
            uniqueNumber = f"{school.school_code}/{current_year}/001"
        else:
            school_obj = schools.last()
            last_uniqueNumber = school_obj.uniqueNumber.split('/')[-1]
            next_invoice_number = int(last_uniqueNumber) + 1
            uniqueNumber = f"{school.school_code}/{current_year}/{next_invoice_number:03d}"
        return uniqueNumber

    def generate_receipt_number(self):
        current_year = datetime.now().year
        receipts = Receipts.objects.all()
        if receipts.count() == 0:
            receipt_number = f"RCPT/{current_year}/001"
        else:
            re = receipts.last()
            last_receipt_number = re.receipt_number.split('/')[-1]
            next_invoice_number = int(last_receipt_number) + 1
            receipt_number = f"RCPT/{current_year}/{next_invoice_number:03d}"
        return receipt_number