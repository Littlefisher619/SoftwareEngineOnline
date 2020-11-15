# 组内评分相关

## [POST] /api/rate/create

* 接口：创建评分

* 接口描述：创建评分需指定评分的对应作业，需指定`homework`为指定的作业，`group`为指定组，`ratedetail`为包含所有包括自己在内的队员的分值分配比，`member`代表组员的id，`rate`表示评分（需要是[0,100]的整数总和需要等于100），接口会验证是否已经评过分、是否有权限评分、数据是否合法等情况。

* 接口示例：
  
  对Homework_id为4，组id为1添加评分
  
```json
{
    "homework": 4,
    "group": 1,
    "ratedetail": [
        {
            "member": 6,
            "rate": 90
        },
        {
            "member": 55,
            "rate": 10
        }
    
    ]
}
```

## [GET] /api/rate

* 接口：评分列表

* 返回所有的组内评分列表，根据`homework`、`group`查询参数可以进行筛选。

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "createat": "2020-10-14T18:41:04.247495",
            "homework": 4,
            "group": 1,
            "ratedetail": [
                {
                    "member": 6,
                    "rate": 90
                },
                {
                    "member": 55,
                    "rate": 10
                }
            ]
        }
    ]
}
```