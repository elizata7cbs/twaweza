from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from core.settings import *
from users.models import CustomUser
from schools.models import Schools
import sys

if 'runserver' in sys.argv:
    required_groups = ['admin', 'superuser', 'accountant']
    for group_name in required_groups:
        if not Group.objects.filter(name=group_name).exists():
            Group.objects.create(name=group_name)

    # Check and create school if it does not exist
    if not Schools.objects.exists():
        print("Creating dummy school")
        school = Schools.objects.create(
            name=SCHOOL_NAME,
            school_code=SCHOOL_CODE,
            country=COUNTRY,
            country_code=COUNTRY_CODE,
            county=COUNTY,
            sub_county=SUB_COUNTY,
            city=CITY,
            street_address=STREET_ADDRESS,
            postal_code=POSTAL_CODE,
            phone_number1=PHONE_NUMBER1,
            phone_number2=PHONE_NUMBER2,
            phone_number_country_code=PHONE_NUMBER_COUNTRY_CODE,
            email_address=EMAIL_ADDRESS,
            website=WEBSITE,
            registration_number=REGISTRATION_NUMBER,
            school_type=SCHOOL_TYPE,
            boarding_status=BOARDING_STATUS,
            currency=CURRENCY,
        )

    # Check and create superuser if it does not exist
    if not CustomUser.objects.filter(is_superuser=True).exists():
        print("Creating dummy Supseruser")
        group = Group.objects.get(name='superuser')
        user = CustomUser.objects.create(
            first_name=SUPERUSER_FIRST_NAME,
            last_name=SUPERUSER_LAST_NAME,
            username=SUPERUSER_USERNAME,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_verified=True,
            schools=None,
            email=SUPERUSER_EMAIL,
            usergroup=group,
            address="N/A",
            phone_number=SUPERUSER_PHONE_NUMBER,
            password=make_password(SUPERUSER_PASSWORD),
        )
        user.groups.add(group)

    if not CustomUser.objects.filter(usergroup=Group.objects.get(name='admin')).exists():
        school = Schools.objects.get(id=1)
        group = Group.objects.get(name='admin')
        print("Creating dummy Administrator")
        user = CustomUser.objects.create(
            first_name="Test",
            last_name="Admin",
            username="admin",
            is_superuser=False,
            is_active=True,
            schools=school,
            email="titusmbole9@gmail.com",
            usergroup=group,
            address="N/A",
            is_verified=True,
            phone_number="0799886633",
            password=make_password("admin"),
        )
        user.groups.add(group)

    if not CustomUser.objects.filter(usergroup=Group.objects.get(name='accountant')).exists():
        school = Schools.objects.get(id=1)
        group = Group.objects.get(name='accountant')
        print("Creating dummy Accountant")

        user = CustomUser.objects.create(
            first_name="John",
            last_name="Accountant",
            username="accountant",
            is_superuser=False,
            is_active=True,
            schools=school,
            email="encodetechologies@gmail.com",
            usergroup=group,
            address="N/A",
            is_verified=True,
            phone_number="0755443311",
            password=make_password("accountant"),
        )
        user.groups.add(group)



