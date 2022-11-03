#!/bin/bash

#1.生成数据库迁移文件
python3 /opt/application/manage.py makemigrations&&
#2.根据数据库迁移文件来修改数据库
python3 /opt/application/manage.py migrate&&
#3.用uwsgi启动django服务
uwsgi --ini /opt/application/uwsgi.ini
