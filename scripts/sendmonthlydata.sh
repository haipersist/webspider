#!/bin/sh

source /etc/profile

python $PackagePath/spider/webspider/manage.py initenv


python $PackagePath/spider/webspider/manage.py senddata -c monthly_jobs







