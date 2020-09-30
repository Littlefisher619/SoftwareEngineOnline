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
    file = open('第一次博客作业.csv', 'r', encoding='utf-8')
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
        score = int(i[5])
        if score == 0:
            continue
        scoredetail = {
            "scorepoints": [],
            "bonus": 0,
            "score": score,
        }
        for point in range(6, 15):
            scoredetail['scorepoints'].append(
                {
                    "point": fixed_row[point],
                    "score": int(i[point]),
                }
            )
        jsonstr = json.dumps(scoredetail)
        try:
            userid = User.objects.get(pk=stuid).pk
            if Judgement.objects.filter(homework_id=1, student_id=userid).exists():
                print(stuid, 'judged yet!')
                continue
            Judgement(
                student_id=userid,
                scoredetail=jsonstr,
                homework_id=1,
                judger_id=6,
            ).save()
        except User.DoesNotExist:
            print(stuid, 'is not registered yet!')








        count += 1

