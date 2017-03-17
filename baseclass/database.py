#!/usr/bin/python
# -*-coding:utf-8 -*-
import MySQLdb
import cPickle as pickle
from webspider.utils.get_project_setting import get_project_setting



class Database():

    def __init__(self):
        self._connect()
    
    def _connect(self):
        self.setting = get_project_setting()
        config = self.setting['DATABASES']['mysql']
        self.con = MySQLdb.connect(config['HOST'],
                                   config['USER'],
                                   config['PASSWORD'],
                                   config['NAME'],
                                   config['PORT'],
                                   charset='utf8')
        self.cursor = self.con.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor.execute('SET NAMES utf8')
    
    def query(self,sql,where=None):
        if where:
            sql = "%s where %s" % (sql,where)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        
    def insert_by_dic(self,table,data):
        """
        the method is used to insert data into table ,
        the paramater data must be dict .

        :param table:
        :param data:
        :return:
        """
        if not isinstance(data,dict):
            return None
        keys=data.keys()
        values=[]
        keystr = ','.join('`' + x + '`' for x in keys)
        for key in keys:
            values.append(data[key])
        valstr = ','.join( "'" + x + "'" if isinstance(x,unicode) \
                           else "'" + str(x).decode('utf8') +"'" for x in values )   
        sql="INSERT INTO  %s (%s) VALUES (%s) " % (table,keystr,valstr)
        self.cursor.execute(sql)
        self.con.commit()
        return True

    def update_(self,table,key,value,ref_key,ref_value):
        sql = 'update %s set %s="%s" where %s="%s" ' \
              % (table,key,value,ref_key,ref_value)
        #print sql
        self.sql_exec(sql)
        
    def update_by_dic(self,table,ref_key,ref_value,data):
        keys = data.keys()
        values=[]
        keystr = ['`' + x + '`' for x in keys]
        for key in keys:
            values.append(data[key])
        valstr = [ "'" + x + "'" if isinstance(x,unicode) \
                           else "'" + str(x).decode('utf8') +"'" for x in values]
        obj = ','.join(str(keystr[index])+"=%s"%valstr[index] \
                       for index in range(0,len(keys)))
        sql = 'UPDATE %s set %s where %s="%s"'%(table,obj,ref_key,ref_value)
        self.cursor.execute(sql)
        self.con.commit()

    def load_file_to_db(self, table, file_name):
        sql_load = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s \
                FIELDS TERMINATED BY ',' \
                ENCLOSED BY '' LINES TERMINATED BY '\n' " % ( 
            file_name, table)
        self.cursor.execute(sql_load)
        self.con.commit()




if __name__ == "__main__":
    db = Database()
    item = {'salary': u'3-4\u4e07/\u6708', 'requirement': u'<div class="bmsg job_msg inbox">\r\n\t\t\t\t\t\t<span class="label">\u804c\u4f4d\u63cf\u8ff0\uff1a</span><br>\r\n\t\t\t\t\t\t\u804c\u4f4d\u63cf\u8ff0:<br>1\u3001\u8d1f\u8d23\u4eca\u65e5\u5934\u6761\u6c9f\u901a\u7cfb\u7edf\u7814\u53d1\uff0c\u5305\u62ec\u4f46\u4e0d\u9650\u4e8e\u5373\u65f6\u901a\u8baf(IM)\u5de5\u5177\uff1b<br>2\u3001\u8d1f\u8d23\u9ad8\u8d28\u91cf\u7684\u8bbe\u8ba1\u548c\u7f16\u7801\uff1b<br>3\u3001\u627f\u62c5\u91cd\u70b9\u3001\u96be\u70b9\u7684\u6280\u672f\u653b\u575a\uff1b<br>4\u3001\u4e3b\u8981\u8bed\u8a00\u4e3aPython/Golang\u3002<br>\u804c\u4f4d\u8981\u6c42:<br>1\u3001\u826f\u597d\u7684\u8bbe\u8ba1\u548c\u7f16\u7801\u54c1\u5473\uff0c\u70ed\u7231\u5199\u4ee3\u7801\u80fd\u4ea7\u51fa\u9ad8\u8d28\u91cf\u7684\u8bbe\u8ba1\u548c\u4ee3\u7801\uff1b<br>2\u3001\u638c\u63e1WEB\u540e\u7aef\u5f00\u53d1\u6280\u672f: \u534f\u8bae\u3001\u67b6\u6784\u3001\u5b58\u50a8\u3001\u7f13\u5b58\u3001\u5b89\u5168\u7b49\uff1b<br>3\u3001\u6709\u826f\u597d\u7684\u4ea7\u54c1\u610f\u8bc6\uff1b<br>4\u3001\u79ef\u6781\u4e50\u89c2\uff0c\u8ba4\u771f\u8d1f\u8d23\uff0c\u4e50\u4e8e\u534f\u4f5c\u3002<br>\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t<div class="mt10">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p class="fp f2">\r\n\t\t\t\t\t\t\t\t<span class="label">\u804c\u80fd\u7c7b\u522b\uff1a</span>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<span class="el">\u4e92\u8054\u7f51\u8f6f\u4ef6\u5f00\u53d1\u5de5\u7a0b\u5e08</span>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</p>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t<a class="icon_b i_note" href="javascript:void(0);" onclick="UserReport(\'86651951\',\'c\',\'http://search.51job.com/\',\'http://my.51job.com/\',this);return false;">\u4e3e\u62a5</a>\r\n\t\t\t\t\t\t<a class="icon_b i_share" href="javascript:void(0);" id="fenxiang">\u5206\u4eab</a>\r\n\t\t\t\t\t\t<div class="clear"></div>\r\n\t\t\t\t\t</div>', 'pub_time': u'2017-03-07', 'title': u'\u9ad8\u7ea7\u670d\u52a1\u7aef\u5f00\u53d1\u5de5\u7a0b\u5e08-Python/Golang (\u804c\u4f4d\u7f16\u53f7\uff1a5003)', 'website_id': 4, 'company_id': 216L, 'link': 'http://jobs.51job.com/beijing-hdq/86651951.html?s=01&t=0', 'welfare': ''}
    html = """
            <div class="bmsg job_msg inbox">
						<span class="label">职位描述：</span><br>
						职位描述:<br>1、负责今日头条沟通系统研发，包括但不限于即时通讯(IM)工具；<br>2、负责高质量的设计和编码；<br>3、承担重点、难点的技术攻坚；<br>4、主要语言为Python/Golang。<br>职位要求:<br>1、良好的设计和编码品味，热爱写代码能产出高质量的设计和代码；<br>2、掌握WEB后端开发技术: 协议、架构、存储、缓存、安全等；<br>3、有良好的产品意识；<br>4、积极乐观，认真负责，乐于协作。<br>
												<div class="mt10">
														<p class="fp f2">
								<span class="label">职能类别：</span>
																	<span class="el">互联网软件开发工程师</span>
																</p>
																				</div>
						<a class="icon_b i_note" href="javascript:void(0);" onclick="UserReport('86651951','c','http://search.51job.com/','http://my.51job.com/',this);return false;">举报</a>
						<a class="icon_b i_share" href="javascript:void(0);" id="fenxiang">分享</a>
						<div class="clear"></div>
					</div>
            """
    from scrapy.selector import Selector
    sel = Selector(text=html,type='html')
    for item in sel.xpath("//div/text()").extract():
        print item
    """
    ry:
        db.insert_by_dic('jobs', item)
    except Exception,e:
        print str(e)
        for key in item:
            print key,item[key]
    """
