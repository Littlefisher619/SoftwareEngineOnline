# 作业相关

## [GET] /api/homework/

* 接口：作业列表

* 接口示例-调用成功
  
```http request
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "title": "aaa",
            "homeworktype": 2,
            "scorerules": [
                {
                    "point": "1.1",
                    "max": 100
                }
            ],
            "author": 1
        }
    ]
}
```
	

## [GET] /api/homework/<id>/tasklist

* 接口：获取指定作业id的待评分列表

* 目标作业为个人作业，支持指定`search`参数模糊搜索学号、姓名
  以及支持精确搜索`stuname`,`stuid`,`id`

* 目标作业为结对/团队作业，支持指定`search`参数进行模糊搜索组名、组长名、组长学号
  以及支持精确搜索`grouptype`,`leader__stuname`,`groupname`,`id`,`leader`


* 接口示例：

  请求成功：
  
```http request
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "username": "testtest",
            "email": "test@test.com",
            "stuid": "000000"
        },
        {
            "id": 1,
            "username": "littlefisher",
            "email": "i@aaa.me",
            "stuid": "1234567"
        }
    ]
}
```
  
  请求失败(非测试组成员访问时)：
  
```json
{
    "success": false,
    "message": "你走错地方惹，这儿啥也没有~"
}
```

## [GET] /api/homework/<id>/statistics/

* 接口：对指定作业进行统计，返回去除0分作业/评分点的均值、最大值、最小值，以及每个评分点除去了没得分的人的平均、最大、最小得分比。

* 过滤器：`homework`, `judger`, `group`, `student`, `student__stuname`, `student__stuid`, `group__leader__stuname`

* 接口返回数据示例：

```json
{
    "totalscore": {
        "min": 11.0,
        "max": 93.0,
        "avg": 67.79,
        "exclude": 15,
        "ranges": [
            {
                "name": ">100",
                "from": 100,
                "to": null,
                "count": 0
            },
            {
                "name": "[0,20)",
                "from": 0,
                "to": 19,
                "count": 17
            },
            {
                "name": "[20,40)",
                "from": 20,
                "to": 39,
                "count": 10
            },
            {
                "name": "[40,60)",
                "from": 40,
                "to": 59,
                "count": 11
            },
            {
                "name": "[60,65)",
                "from": 60,
                "to": 64,
                "count": 7
            },
            {
                "name": "[65,70)",
                "from": 65,
                "to": 69,
                "count": 13
            },
            {
                "name": "[70,75)",
                "from": 70,
                "to": 74,
                "count": 16
            },
            {
                "name": "[75,80)",
                "from": 75,
                "to": 79,
                "count": 16
            },
            {
                "name": "[80,85)",
                "from": 80,
                "to": 84,
                "count": 10
            },
            {
                "name": "[85,90)",
                "from": 85,
                "to": 89,
                "count": 8
            },
            {
                "name": "[90,95)",
                "from": 90,
                "to": 94,
                "count": 10
            },
            {
                "name": "[95,100)",
                "from": 95,
                "to": 99,
                "count": 0
            }
        ]
    },
    "points": [
        {
            "point": "1.1",
            "max": 1.0,
            "min": 0.33,
            "avg": 0.83,
            "exclude": 0
        },
        {
            "point": "1.2",
            "max": 1.0,
            "min": 0.17,
            "avg": 0.61,
            "exclude": 1
        },
        {
            "point": "1.3",
            "max": 1.0,
            "min": 0.11,
            "avg": 0.68,
            "exclude": 0
        },
        {
            "point": "1.4",
            "max": 1.0,
            "min": 0.25,
            "avg": 0.61,
            "exclude": 12
        },
        {
            "point": "1.5",
            "max": 1.0,
            "min": 0.17,
            "avg": 0.65,
            "exclude": 5
        },
        {
            "point": "1.6",
            "max": 1.0,
            "min": 0.17,
            "avg": 0.61,
            "exclude": 13
        },
        {
            "point": "1.7",
            "max": 1.0,
            "min": 0.17,
            "avg": 0.59,
            "exclude": 1
        },
        {
            "point": "2.1",
            "max": 1.0,
            "min": 0.2,
            "avg": 0.64,
            "exclude": 1
        },
        {
            "point": "2.2",
            "max": 1.0,
            "min": 0.2,
            "avg": 0.7,
            "exclude": 1
        },
        {
            "point": "2.3",
            "max": 1.0,
            "min": 0.5,
            "avg": 0.71,
            "exclude": 1
        },
        {
            "point": "2.4",
            "max": -2,
            "min": -40,
            "avg": -12.0,
            "exclude": 66
        }
    ]
}
```