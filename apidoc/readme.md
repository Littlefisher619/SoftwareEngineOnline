# 后端API接口

所有的查询接口基本都支持排序，可以在Django-RestFramework的API测试页面查看具体可以进行排序的字段

[用户相关](/apidoc/users.md)

* 注册、登录、修改密码、重置密码
* 个人资料、我的组队信息
* 作业(被)评分记录
* 系统排行榜
* 用户列表

[作业相关](/apidoc/homework.md)

* 作业列表、作业待评分列表（支持模糊搜索和精确搜索）
* 对指定作业进行统计，支持对过滤器过滤后的数据进行统计

[组队相关](/apidoc/groups.md)

* 所有组队（支持精确搜索）、创建组队、加入组队

[评分相关](/apidoc/judgement.md)

* 已评分列表（支持模糊搜索和精确搜索）、创建评分、修改评分

[组内评分相关](/apidoc/rate.md)

* 创建组内评分、查询组内评分列表（支持精确搜索）