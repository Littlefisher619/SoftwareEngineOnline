import requests
import json
import csv


def fetch_json():
    url = input('HOSTNAME: ').strip()
    token = input('Authorization(JWT): ').strip()
    data = requests.get(url='https://' + url + '/api/user/rank/', headers={
        'Authorization': 'Bearer ' + token
    })
    # print(data.text)
    json_file = open('total_score.json', 'wb')
    json_file.write(
        data.content
    )
    json_file.close()


def get_homework_desc():
    url = 'https://' + input('HOSTNAME: ').strip() + '/api/homework/'
    token = input('Authorization(JWT): ').strip()
    homeworks = [None] * 23
    while url is not None:
        data = requests.get(url=url, headers={
            'Authorization': 'Bearer ' + token
        })
        json_data = json.loads(data.content)

        for item in json_data['results']:
            homeworks[item['id'] - 1] = item['title']

        url = json_data['next']

    print(homeworks)
    return homeworks

def export():

    json_file = open('total_score.json', 'r', encoding='utf-8')
    csv_file = open('export.csv', 'w', newline='')
    scores = json.loads(json_file.read())
    json_file.close()
    writer = csv.writer(csv_file)


    writer.writerow(
        ['学号', '姓名', '总成绩'] + get_homework_desc()
    )

    for student in scores:
        row = []
        row.append("'" + student['stuid'])
        # For excel
        row.append(student['stuname'])
        row.append(student['totalscore'])

        scoredetail = [-1] * 23
        for detail in student['scoredetail']:
            scoredetail[detail['homework'] - 1] = detail['score']

        if -1 in scoredetail:
            print('error:', student)

        row += scoredetail

        writer.writerow(row)

    csv_file.close()

if __name__ == '__main__':
    export()