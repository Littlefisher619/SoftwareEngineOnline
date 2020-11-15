# 用户相关

## [POST] /api/signup/

* 接口：注册接口

* 描述：用户名、密码要求6位字符以上，且不能是简易密码或纯数字密码，要求邮箱和用户名均唯一。已登录的用户不能使用此接口。

* 接口示例：

```json
{
    "username": "testaccount",
    "password": "testaccount",
    "email": "testaccount@test.com"
}
```

* 调用成功（将返回`JWT-Token`，可以直接作为凭据使用，无需再次访问/login接口）：

```http request
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": true,
    "message": "注册成功",
    "token": "(JWT Token)"
}
```

* 调用失败

  * JSON数据格式错误

```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "JSON parse error - Expecting ',' delimiter: line 4 column 15 (char 65)"
}
```

  * 数据字段格式不正确

```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "username": [
        "该字段不能为空。"
    ],
    "password": [
        "该字段不能为空。"
    ],
    "stuid": [
        "该字段不能为空。"
    ]
}
```

    密码长度不够（用户名长度不够、邮箱格式不正确时也类似）

```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
  "password": [
      "请确保这个字段至少包含 6 个字符。"
  ]
}
```

	  学号已被注册（用户名已被注册类似）

```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
  "non_field_errors": [
      "学号已经被注册了"
  ]
}
```

## [POST] /api/login/

* 接口：登录接口

* 描述：使用用户名或学号之一以及与之相匹配的密码可登录系统，登录成功时返回用户信息和JWT Token。已登录的用户不能使用此接口。

* 接口示例：

  使用用户名登录

```json
  {
    "username": "testaccount",
    "password": "testaccount"
  }
```

  使用学号登录

```json
{
    "stuid": "00000",
    "password": "testtest"
}
```

* 调用成功（将返回JWT-Token和用户名）：

```http request
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
  "token": "(JWT Token)",
  "username": "testtest"
}
```

* 调用失败

  * 只能用用户名或邮箱之一登录

```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "non_field_errors": [
        "只能使用用户名或者学号之一进行登录"
    ]
}
```

  * 登录失败

```http request
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "non_field_errors": [
        "提供的凭据信息无效"
    ]
}
```

  * 其他错误类型，如格式错误等，参见前面写的文档

## [GET] /api/user/

* 接口：用户列表

* 描述：使用用户名或邮箱之一以及与之相匹配的密码可登录系统，登录成功时返回用户信息和JWT Token。已登录的用户不能使用此接口。

* 接口示例：
  
  （直接使用GET进行请求）
  
  * 调用成功
  
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
            "stuid": "000000",
            "stuname": "test",
            "role": 0
        },
        {
            "id": 1,
            "username": "littlefisher",
            "stuid": "",
            "stuname": "",
            "role": 0
        }
    ]
}
```
  
  * 调用失败
  
```http request
HTTP 401 Unauthorized
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
WWW-Authenticate: Bearer realm="api"

{
    "detail": "身份认证信息未提供。"
}
```

## [GET] /api/user/updatepassword

* 接口：修改密码

* 描述：直接POST新密码就行了

* 接口示例：
  
  （直接使用GET进行请求）
  
  * 调用成功
  
```json
{
    "password": ""
}
```

## [GET] /api/user/<id>/resetpassword

* 接口：重置密码

* 描述：重置指定用户的密码，新密码随机生成发至对方邮箱

* 接口示例-调用成功
  
```json
{
    "success": true,
    "message": "密码重置成功！"
}
```

## [GET] /api/user/me

* 接口：我的个人资料


* 接口示例-调用成功
  
```http request
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "username": "littlefisher",
    "stuid": "",
    "stuname": "",
    "role": 0
}
```

## [GET] /api/user/mygroup

* 接口：我的组队

* 描述：获取我的组队信息（含结对作业组和团队作业组）

* 接口返回成功示例：

```http request
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "double": {
        "id": 2,
        "leader": {
            "id": 5,
            "username": "7888888",
            "stuid": "9999999",
            "stuname": "stu2",
            "role": 2
        },
        "grouptype": 1,
        "groupname": "圆圆圆组队作业",
		"token": "aaa-bbb-ccc-ddd"
        "member_detail": []
    },
    "big": {
        "id": 1,
        "leader": {
            "id": 5,
            "username": "7888888",
            "stuid": "9999999",
            "stuname": "stu2",
            "role": 2
        },
        "grouptype": 2,
        "groupname": "小猪佩奇队",
		"token": "aaa-bbb-ccc-ddd",
        "member_detail": []
    }
}
```



## [GET] /api/user/judgements

* 获取我的所有作业（被）评分记录

* 返回数据：

```json
{
    "big": [
        {
            "id": 293,
            "student": null,
            "group": {
                "id": 1,
                "leader": {
                    "id": 6,
                    "username": "littlefisher",
                    "stuid": "12345678",
                    "stuname": "name",
                    "role": 2
                },
                "grouptype": 2,
                "groupname": "123",
                "member_detail": [
                    {
                        "id": 55,
                        "username": "liettes",
                        "stuid": "333333333",
                        "stuname": "yyy",
                        "role": 0
                    }
                ]
            },
            "homework": 4,
            "scoredetail": {
                "scorepoints": [
                    {
                        "point": "1.1",
                        "score": 100
                    }
                ],
                "score": 100,
                "bonus": 0.0
            },
            "createat": "2020-10-14T20:27:54.481796",
            "totalscore": 100.0,
            "blogurl": "http://baidu.com"
        }
    ],
    "double": [],
    "single": []
}
```

## [GET] /api/user/rank

* 接口描述：排行榜（懒得分页的接口）

* 接口描述：按顺序返回排行榜，除去教师和测试组成员。包含用户的学号`stuid`、姓名`stuname`、具体的得分情况列表`scoredetail`（包含`homework`作业的id，`weight`作业权重、`factor`乘积因子、`score`作业算上乘积因子和权重后的得分）以及`totalscore`总分、`rank`排名

* 接口返回实例：

```json

[
    {
        "id": 55,
        "stuid": "333333333",
        "stuname": "yyy",
        "scoredetail": [
            {
                "homework": 1,
                "weight": 1,
                "factor": 1.0,
                "score": 9.0
            },
            {
                "homework": 2,
                "weight": 5,
                "factor": 1.0,
                "score": 515.0
            },
            {
                "homework": 3,
                "weight": 10,
                "factor": null,
                "score": null
            },
            {
                "homework": 4,
                "weight": 2,
                "factor": 1.0,
                "score": 200.0
            }
        ],
        "totalscore": 724.0,
        "rank": 1
    }
]
```