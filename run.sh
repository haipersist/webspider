#!/bin/sh

source /etc/profile

python $PackagePath/spider/webspider/manage.py initenv


python $PackagePath/spider/webspider/manage.py runspiders

python $PackagePath/spider/webspider/manage.py load_online_data







