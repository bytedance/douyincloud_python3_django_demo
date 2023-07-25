# django_python3_demo
本项目是抖音云平台基于 Python 语言 Django 框架的开发模版，模版实现了简单的云调用与获取openID的功能。
抖音云平台支持 Git 代码仓库授权和 Docker 镜像部署两种方式。代码工程对于哪种部署方式没有根本性的差别。

## 目录结构
~~~
django_python3_demo
├── READEME.md
├── db.sqlite3
├── django_python3_demo
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── polls
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_initial.py
    │   ├── __init__.py
    ├── models.py
    ├── templates
    │   └── polls
    │       ├── index.html
    │       ├── question.html
    │       └── results.html
    ├── tests.py
    ├── urls.py
    └── views.py
~~~

## 工程说明


### 日志配置
打开django_python3_demo/django_python3_demo/settings.py，添加 *LOGGING* 配置：
```python3
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
```
日志通过标准输出到 console 后，抖音云平台会自动收集日志，开发者可以在日志菜单进行日志查看，同时支持基于日志的分析和告警。

## 接口说明
本 DEMO 实现了 2 个接口，返回 JSON 结果。

### `GET /api/get_open_id`
获取openid，当未绑定用户时会返回获取openid失败的错误


### 响应结果
```json
{
    "err_no": 0,
    "err_msg": "success",
    "data": "719f****-****-4c**-a0**-*********"
}
```

### `POST /api/text/antidirt`
云调用示例，调用抖音开放平台的OpenApi进行脏词检测

### 请求参数
- `content`:`string` 待检测的内容

### 响应结果
```json
{
    "err_no": 0,
    "err_msg": "success",
    "data": ""
}
```

### 页面例子
浏览器输入路径`https://<开发者域名>/polls`就能打开页面

## 镜像打包部署
本 DEMO 使用 uwsgi 来作为 web 服务器。**可执行文件需要放置在/opt/application下才能保证正确部署运行**，所以本 DEMO 镜像打包目录是/opt/application。

### 导出依赖包
进入项目根目录执行命令：
```bash
pip3 freeze > requirements.txt
```
执行完之后会在项目根目录下生成 *requirements.txt* 文件，文件记录了依赖包以及依赖包的版本。

### 创建 uwsgi 配置文件
在项目根目录下创建 *uwsgi.ini* 文件，文件内容如下：
```properties
[uwsgi]
project=django_python3_demo
chdir=/opt/application
module=%(project).wsgi:application
master=True

http=:8000
buffer-size=65536

pidfile=/tmp/%(project)-master.pid
vacuum=True
max-requests=5000
#这个配置打开后可能会出现镜像启动后实例退出，需要关闭，日志通过前面介绍的方式标准输出到console就能在抖音云控制台查看
#daemonize=/tmp/%(project)-uwsgi.log

#设置一个请求的超时时间(秒)，如果一个请求超过了这个时间，则请求被丢弃
harakiri=30
#当一个请求被harakiri杀掉会，会输出一条日志
harakiri-verbose=true
```
在进行配置时注意修改 `django_python3_demo/django_python3_demo/settings.py` 里的 ALLOW_HOST 配置，默认只允许本机访问，需要修改如下：
```python3
ALLOWED_HOSTS = ['*']
```

## License

This project is licensed under the [Apache-2.0 License](LICENSE).