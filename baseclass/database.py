#!/usr/bin/python
# -*-coding:utf-8 -*-
import MySQLdb
from utils.get_project_setting import get_project_setting

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
    
    def query_dic(self,sql,where=None):
        if where:
            sql = "%s where %s" % (sql,where)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        
    def insert_by_dic(self,table,data):
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
        self.conn.commit()




