# webspider
webspider is used to crawl all things of network.
By far, I use this to crawl jon information in order to get latest data.

###I ignore all setting file because of security,so you can not see them.but
###what you should know is my setting file is according to django setting style.


At first,you must add the project path into global environment variable of system


In /etc/profile:
set PYTHONPATH as your/path/to/Package

#Sysytem Introduction

##1、MySQL：
有几张表：
1、 company。保存公司名称，为unique索引；
2、 website.
3、 职位基本信息，jobs,公司名称,website是外键；


##2、Redis：
Redis用来保存每个公司的最新职位，每天进行更新，key为公司名称。如果遇到一个公司发布了不同的职位，且时间相同，那也要随机选一个保存。
要设置更新机制，如果一个公司的职位在一个月内没有更新，也要删除该职位信息。

##3、项目结构
###1、 Config
各种配置文件
###2、 Baseclass
定义各种基类，数据库客户端，爬虫基类等等。
###3、 Tests
该文件包用来做单元测试
###4、 Utils
该Python包保存各种通用的函数和类，类似工具。
###5、 各种spider
存储各种具体的spider。
###6、 Crontab文件
定时任务
###7、 脚本
各种脚本
###8、Template
存储用来发送邮件的模板。

###9、 Manage.py
主文件，用来管理工程项目，启动，停止，配置等等。


###10、da
data statistic and analysize