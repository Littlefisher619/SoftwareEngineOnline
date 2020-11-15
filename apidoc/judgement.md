# 评分相关

## [GET] /api/judgement

* 接口：评分列表

* 接口测试地址：/api/judgement/?homework=4&judger=&group=&student=

* 接口描述：查看系统上所有评分，GET即可，接受`hoemwork`、`judger`、`group`、`student`四个查询参数作为筛选，接受`ordering=字段名`作为数据排序，例如`ordering=id-`是以`id`降序，`ordering=id`是以`id`升序。支持模糊搜索学生姓名、、学号、组名。

* 调用成功：

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
            "id": 1,
            "student": 2,
            "group": null,
            "judger": {
                "id": 2,
                "username": "testtest",
                "email": "test@test.com",
                "stuid": "000000"
            },
            "homework": 4,
            "scoredetail": {
                "count": 2,
                "scorepoints" : [
                    "1.1": 10,
                    "2.1": 20
                ],
                "bonus": 0.2,
                "score": 36
            }
            "createat": "2020-09-10T17:46:27.950909"
        },
        {
            "id": 3,
            "student": null,
            "group": 16,
            "judger": {
                "id": 1,
                "username": "littlefisher",
                "email": "i@abc.me",
                "stuid": "1234567"
            },
            "homework": 4,
            "scoredetail": {
                "count": 2,
                "scorepoints" : [
                    "1.1": 10,
                    "2.1": 20
                ],
                "bonus": -0.2,
                "score": 24
            }
            "createat": "2020-09-10T18:21:36.939747"
        }
    ]
}
```

## [POST] /api/judgement/create

* 接口：创建评分

* 接口描述：创建评分需指定评分的对应作业、若评分的对应作业为单人类型，那么只能填写`student`字段，若作业类型为结对/团队作业，那么只能填写`group`字段，`scoredetail`为得分详情

* 接口示例：
  
  对Homework_id为1，学生id为1添加评分
  
```json
{
    "student": 1,
    "group": null,
    "homework": 1,
    "scoredetail": {
          "count": 2,
          "scorepoints" : {
              "1.1": 10,
              "2.1": 20
          },
          "bonus": -0.2,
          "score": 24
    }
}
```

  成功：
  
```http request
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": true,
    "message": "创建成功",
    "data": {
        "id": 4,
        "student": 2,
        "group": null,
        "judger": {
            "id": 1,
            "username": "littlefisher",
            "email": "i@littlefisher.me",
            "stuid": "1234567"
        },
        "homework": 1,
        "scoredatail": {
            "test": "test"
        },
        "createat": "2020-09-10T18:57:07.586828"
    }
}
```

  失败：
  
```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "non_field_errors": [
        "对当前学生的这一项单人作业评分已经存在"
    ]
}
```

  `non_field_errors`所有可能值：

 * 需指定一个作业才能进行评分
 * 作业为单人作业时，必须指定student关键字以创建评分对象
 * 作业为单人作业时，只能指定student关键字
 * 对当前学生的这一项单人作业评分已经存在
 * 作业为结对/团队作业时，必须指定group关键字以创建评分对象
 * 作业为结对/团队作业时，只能指定group关键字
 * 对当前队伍的这一项结对/团队作业评分已经存在

 如果权限不足，若是非测试组成员访问此接口，返回403状态码：
 
```json
{
 "success": False,
 "message": "不是测试组的成员不能创建评分诶"
}
```

## [UPDATE] /api/judgement/<id>/

* 接口：修改评分

* 接口描述：修改评分只能修改自己创建的评分的评分详情（也就是具体的评分）

* 接口示例：用UPDATE的HTTP方法向接口提交如下数据：

```json
{
  "scoredetail": {
      "count": 2,
      "scorepoints" : {
          "1.1": 10,
          "2.1": 20
      },
      "bonus": -0.2,
      "score": 24
    }
}
```
  
  调用成功时返回修改后的judgement实例信息，状态码200，若找不到评分数据而失败返回404，更新了不是自己创建的评分返回403