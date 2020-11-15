## [GET] /api/group

* 接口：获取所有的队伍

* 接口测试地址：/api/group/?grouptype=1&leader=2

* 描述：可携带参数`grouptype`,`leader`进行筛选，member_detail为组员的列表（不包含队长自己，下同）

* 接口示例：
  
  * 调用成功
  
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
            "id": 14,
            "leader": {
                "id": 2,
                "username": "testtest",
                "stuid": "000000",
                "stuname": "test",
                "role": 0
            },
            "grouptype": 1,
            "groupname": "miaomiaomiao"
            "member_detail": [
                {
                    "id": 1,
                    "username": "littlefisher",
                    "stuid": "",
                    "stuname": "",
                    "role": 0
                }
            ]
        }
    ]
}
```
## [POST] /api/group/create

* 接口：创建队伍

* 描述：POST对应的组类型创建队伍，当已经加入其它队伍或者是其它队伍的队长的时候不能创建。队伍名最小五个字符

* 接口示例：

```json
{
    "grouptype": 2,
    "groupname": "miaomiaomiao"
}
```
	
	* 调用成功：
	
```http request
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": true,
    "message": "创建成功",
    "data": {
        "id": 16,
        "leader": {
            "id": 1,
            "username": "littlefisher",
            "stuid": "",
            "stuname": "",
            "role": 0
        },
        "groupname": "miaomiaomiao"
        "grouptype": 2,
        "member_detail": [ ]
    }
}
```
	
	* 调用失败
	
```http request
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": false,
    "message": "你已经是当前队伍类型的某个组的组员，不能再创建新的队伍"
}
```

## [GET] /api/group/<id>/join

* 接口：加入队伍

* 描述：加入指定id的组

* 接口示例：

  * 调用成功
  
```http request
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": true,
    "message": "加入成功",
    "data": {
        "id": 14,
        "leader": {
            "id": 2,
            "username": "testtest",
            "stuid": "000000",
            "stuname": "test",
            "role": 0
        },
        "groupname": "miaomiaomiao"
        "grouptype": 1,
        "member_detail": [
            {
                "id": 1,
                "username": "littlefisher",
                "stuid": "",
                "stuname": "",
                "role": 0
            }
        ]
    }
}
```
  
  * 调用失败
  
```http request
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "success": false,
    "message": "你已经是当前队伍类型的某个组的组员，不能再加入其它队伍"
}
```

## [POST] /api/group/<id>/verifytoken

* 接口：验证Token

* 描述：验证Token是否正确，无需登录，调用成功时返回验证是否成功，以success字段表示正确与否，若未找到返回404状态码

* 接口示例：

```json
{
  "token": "12345"
}
```

  调用成功示例：
  
```json
{
  "success": true
}
```

  失败示例
  
```json
{
  "detail": "未找到"
}
```