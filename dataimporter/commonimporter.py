import os
import sys
import csv
import django
import json
pwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.append(pwd)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftwareEngineOnline.settings') # VueSt是自己的项目名称
django.setup()

HOMEWORK_ID = 5
JUDGER_ID = 6
GROUP_ID_COL = 0
BLOG_URL_COL = 1
SCOREPOINT_COL_FROM = 2
SCOREPOINT_COL_TO = 7
CSV_FILENAME = 'score_hw5.csv'

from backend.models import *
if __name__ == '__main__':
    file = open(CSV_FILENAME, 'r', encoding='utf-8')
    csvdata = csv.reader(file)

    count = 0
    fixed_row = None
    for i in csvdata:
        if fixed_row is None:
            fixed_row = i
            continue
        groupid = int(i[GROUP_ID_COL])
        score = 0
        scoredetail = {
            "scorepoints": [],
            "bonus": 0,
            "score": 0,
        }
        for col in range(SCOREPOINT_COL_FROM, SCOREPOINT_COL_TO + 1):
            scoredetail['scorepoints'].append(
                {
                    "point": fixed_row[col],
                    "score": float(i[col]),
                }
            )
            scoredetail['score'] += float(i[col])

        jsonstr = json.dumps(scoredetail)

        try:
            group = Group.objects.get(id=groupid)
            try:
                judgement = Judgement.objects.get(homework_id=HOMEWORK_ID, group_id=groupid)
                print(groupid, 'judged yet! Now updating...')
                judgement.scoredetail = jsonstr
                judgement.totalscore = scoredetail['score'] * (1.0 + scoredetail['bonus'])
                judgement.blogurl = i[BLOG_URL_COL]
                judgement.save()
            except Judgement.DoesNotExist:
                Judgement(
                    group_id = groupid,
                    scoredetail = jsonstr,
                    totalscore = scoredetail['score'] * (1.0 + scoredetail['bonus']),
                    homework_id = HOMEWORK_ID,
                    blogurl = i[GROUP_ID_COL],
                    judger_id = JUDGER_ID,
                ).save()
        except Group.DoesNotExist:
            print(groupid, ' does not exist!')

        count += 1

