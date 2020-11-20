import os
import sys
import csv
import django
import json
pwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.append(pwd)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftwareEngineOnline.settings') # VueSt是自己的项目名称
django.setup()


CSV_FILENAME = 'score_hw5.csv'

from backend.models import *

def import_data():
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
                    blogurl = i[BLOG_URL_COL],
                    judger_id = JUDGER_ID,
                ).save()
        except Group.DoesNotExist:
            print(groupid, ' does not exist!')

        count += 1

def resolve_args(argv):
    global HOMEWORK_ID, JUDGER_ID, GROUP_ID_COL, BLOG_URL_COL, SCOREPOINT_COL_FROM, SCOREPOINT_COL_TO, CSV_FILENAME
    CSV_FILENAME = sys.argv[1]
    HOMEWORK_ID = sys.argv[2]

    resolve = lambda key, default = None : int(argv[argv.index(key)] + 1) if key in argv else default

    GROUP_ID_COL = resolve('--groupid', 0)
    BLOG_URL_COL = resolve('--blog', 1)
    JUDGER_ID = resolve('--judger', 6)
    SCOREPOINT_COL_FROM = resolve('--from', 2)
    SCOREPOINT_COL_TO= resolve('--to', 4)

if __name__ == '__main__':
    resolve_args(argv=sys.argv)
    import_data()
