
import os
import sys
import csv
import django
import json
pwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.append(pwd)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftwareEngineOnline.settings') # VueSt是自己的项目名称
django.setup()

from backend.models import *
if __name__ == '__main__':
    file = open('个人编程作业.csv', 'r', encoding='utf-8')
    homeworkid = 2
    csvdata = csv.reader(file)

    count = 0
    fixed_row = None
    for i in csvdata:
        if fixed_row is None:
            fixed_row = i
            continue
        if i[0] == '':
            continue
        stuid = "%09d" % int(i[0])
        try:
            userid = User.objects.get(stuid=stuid).pk
            if Judgement.objects.filter(homework_id=homeworkid, student_id=userid).exists():
                print(stuid, 'judged yet! Now updating blogurl...')
                judgement = Judgement.objects.get(homework_id=homeworkid, student_id=userid)
                # print(i[3])
                judgement.blogurl = i[3] if i[3] not in ['NULL', ''] else '#'
                judgement.save()

        except User.DoesNotExist:
            print(stuid, 'is not registered yet!')

        count += 1

