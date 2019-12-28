import csv, sys, os

project_dir = r"C:\Users\a.dmytrenko\Downloads\Project\dj-acs-env_37"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

from django.contrib.auth.models import User
from medoc.models import Profile

data = csv.reader(open(r"C:\Users\a.dmytrenko\Downloads\Project\Import\profile_list.csv", encoding='utf-8'), delimiter=";")

for row in data:
    if row[0] != 'username':
        user = User()

        user.username = row[0]
        user.last_name = row[1]
        user.first_name = row[2]
        user.email = row[4]
        # user.is_active = row[6]
        user.save()
        user = User.objects.get(username=user.username)

        profile = Profile.objects.get(user=user.id)
        profile.middle_name = row[3]
        profile.password = row[5]
        profile.job_title = row[7]
        profile.department = row[8]
        profile.company = row[9]
        profile.personal_mobile_phone = row[10]
        profile.phisical_delivery_office_name = row[11]
        # profile.external_user = row[12]
        profile.save()

