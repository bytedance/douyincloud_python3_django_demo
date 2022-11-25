# django_python3_demo
本项目是抖音云平台基于 Python 语言 Django 框架的开发模版，模版通过使用 Redis 和 Mysql 实现了简单的 HelloWorld (django官方polls) 功能。
抖音云平台支持 Git 代码仓库授权和 Docker 镜像部署两种方式。代码工程对于哪种部署方式没有根本性的差别，例子特别基于镜像部署进行说明。

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
### 数据库配置
打开django_python3_demo/django_python3_demo/settings.py，添加 *DATABASES* 配置：
```python3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'polls',
        'USER': os.environ.get('MYSQL_USERNAME'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_ADDRESS').split(':')[0],
        'PORT': int(os.environ.get('MYSQL_ADDRESS').split(':')[1]),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```
抖音云支持控制台配置环境变量，在 DEV 和 PROD 环境的数据库配置信息会不同，所以建议使用环境变量的方式。

### Redis 配置
打开django_python3_demo/django_python3_demo/settings.py，添加 *CACHES* 配置：
```python3
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://' + os.environ.get('REDIS_ADDRESS'),
        'OPTIONS': {
            'username': os.environ.get('REDIS_USERNAME'),
            'password': os.environ.get('REDIS_PASSWORD')
        }
    }
}
```
抖音云支持控制台配置环境变量，在 DEV 和 PROD 环境的 Redis 配置信息会不同，所以建议使用环境变量的方式。

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
本 DEMO 实现了 7 个接口，其中四个使用了 Django 模版页面，剩余三个返回 JSON 结果。

### `POST /polls/redis/<key>/<value>`
验证 Redis Set 功能
#### 请求例子
- `key: platform`
- `value: douyincloud`

```shell
POST /polls/redis/platform/douyincloud
```
##### 响应结果
```JSON
{
  "err_no": 0,
  "err_msg": "success"
}
```

### `GET /polls/redis/<key>`
验证 Redis GET 功能
#### 请求例子
- `key: platform`

```shell
GET /polls/redis/platform
```
##### 响应结果
```JSON
{
  "err_no": 0,
  "err_msg": "success",
  "data": {
    "key": "platform",
    "value": "douyincloud"
  }
}
```

### `GET /polls/openid`
验证小程序 OPENID HEADER 传递功能
#### 请求例子
打开抖音云控制台-接口调试-小程序模拟调试，绑定抖音账号，勾选模拟用户态登录
```shell
GET /polls/openid
```
##### 响应结果
```JSON
{
  "err_no": 0,
  "err_msg": "success",
  "data": {
    "openid": "719f****-****-4c**-a0**-*********"
  }
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

### 创建启动脚本文件
在项目根目录下创建 *run.sh* 文件，内容如下：
```bash
#!/bin/bash

#1.生成数据库迁移文件
python3 /opt/application/manage.py makemigrations&&
#2.根据数据库迁移文件来修改数据库
python3 /opt/application/manage.py migrate&&
#3.用uwsgi启动django服务
uwsgi --ini /opt/application/uwsgi.ini
```

### 创建 *Dockerfile*
```Dockerfile
FROM python:3.10.6

MAINTAINER douyincloud

COPY ./ /opt/application

WORKDIR /opt/application

RUN pip3 install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn/simple
RUN chmod 777 run.sh

ENTRYPOINT ["/bin/sh", "/opt/application/run.sh"]
EXPOSE 8000
```

### 打包上传
**Step 1**: 在项目根目录下执行如下命令进行镜像打包
```bash
docker build -f Dockerfile -t django_python3_demo:1.0 .
```

**Step 2**: 执行 `docker images`，拷贝 REPOSITORY 为 django_python3_demo 的 *IMAGE ID*(本地镜像ID)。

**Step 3**: 上传镜像
```bash
USAGE
  $ dycloud container:push [--tag <value>] [--remark <value>] [--image-id <value>] [--service-name <value>]

FLAGS
  --image-id=<value>      本地镜像ID
  --remark=<value>        镜像备注
  --service-name=<value>  服务名称
  --tag=<value>           设置镜像的 TAG
```
上面命令只是一个例子，每个服务的仓库 ID 都不一样，开发者可以登录控制台``部署发布-发布设置-镜像仓库``页面进行拷贝命令。这里使用了抖音云 CLI **dycloud**，开发者本地需要安装抖音云 CLI 来上传镜像。
抖音云 CLI 安装命令：``` npm install -g @open-dy/cloud-cli```

### 部署
打开抖音云控制台进行发布，在发布前检查项目中用到的环境变量是否都已经在``控制台-部署运行-发布设置-基础设置-环境变量``设置好，否则可能启动失败。

## License

This project is licensed under the [Apache-2.0 License](LICENSE).