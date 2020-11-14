# SoftwareEnginline

基于Django开发的，为软件工程课程提供方便，结合博客园平台，定制开发的自动化平台。侧重的功能是查分、评分、以及成绩统计功能，至于作业提交功能简便起见目前没有实现，需要使用博客园班级功能进行辅助。

基本的设定：

* 用户角色：学生、教师、评测组、超级管理员(Django)
* 作业类型：单人作业、结对作业、团队项目
* 组队类型：结对队伍、团队队伍

## Features

基本功能：

* 作业需由后台进行导入，可以指定作业类型与评分点细则
* 评测组可以对不同作业的评分，评分时支持传入每个评分点的具体分值、以及奖励分值比例`bonus`（也可以为负值）
* 作业支持设定权重，可以由组长将团队作业获得的加权总分分配给组员（称为组内评分）
* 每个学生的分数由：单人作业的加权得分 + 结对作业的加权得分 + 分配得到的团队项目的加权得分 组成
* 支持对每个作业的评分点的分布、均值、最大值、最小值进行统计
* 支持查询所有学生的总分排名

权限控制：

* 只有评测组才可以对作业进行评分，每个作业只能有一个评分，且评分创建后只有超级管理员或创建者自己可以修改
* 用户只有在查询总分的接口才可以看见所有人的得分，但是每个人/组的不同作业的得分详情仅自己可见，且不展示评分者
* 拥有组长权限且自己是某个组组长，才可以创建对某次作业进行评分。
* 超级管理员可以为用户重置密码，新密码将发送至用户的注册邮箱


## Usage

后端：Python(Venv) + Uwsgi + Nginx

配置后端运行环境(建议使用venv)：

```shell script
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

创建uwsgi_params，填入以下内容

```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```

配置uwsgi.ini

```ini
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /path/to/src/
# Django's wsgi file
module          = SoftwareEngineOnline.wsgi
# the virtualenv (full path)
home            = /path/to/src/venv

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 4
# multi-threads
enable-threads = true
# the socket (use the full path to be safe
socket          = /path/to/src/seonline.sock
pidfile          = /path/to/src/seonline.pid
# ... with appropriate permissions - may be needed
chmod-socket    = 644
# clear environment on exit
vacuum          = true
uid = www-data
gid = www-data
daemonize = /path/to/src/uwsgi.log

```

在nginx配置目录下的sites-available创建配置文件seonline，将/api、/admin、/static转发给django，其他交由前端处理。
然后在sites-enabled指向sites-available/seonline的符号链接，重启nginx服务

```
# the upstream component nginx needs to connect to
upstream django {
    server unix:///path/to/src/seonline.sock; # for a file socket
    # server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}
# configuration of the server
server {
    # the port your site will be served on
    listen 80;
    listen 443 ssl;
    server_name seonline.littlefisher.me;
    ssl_certificate      /etc/nginx/ssl/yoursslcert.crt;
    ssl_certificate_key  /etc/nginx/ssl/yoursslcert.key;

    ssl_protocols        TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers          ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers  on;
    ssl_session_cache    shared:SSL:10m;
    ssl_session_timeout  10m;
    # the domain name it will serve for
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    #root /path/to/frontend;
    # Finally, send all non-media requests to the Django server.
    location ~ ^/(api|admin) {
        uwsgi_pass  django;
        include     /path/to/src/uwsgi_params; # the uwsgi_params file you installed
    }

    location /static {
        alias /path/to/src/static; # your Django project's static files - amend as required
    }

    # Frontend is employed in another computer

    location / {
        proxy_set_header Host $host;
        proxy_pass http://frontend:port;
        #try_files $uri @vuerouter;
        # index  index.html;
    }

    location @vuerouter{
        rewrite ^.*$ /index.html last;
        proxy_set_header Host $host;
        proxy_pass http://frontend:port;
        # rewrite ^.*$ /index.html last;
    }
}

```

然后启动uwsgi：

```
uwsgi --ini uwsgi.ini
```

重启命令：

```
uwsgi --reload seonline.pid
```

停止命令：

```
uwsgi --stop uwsgi.ini
```