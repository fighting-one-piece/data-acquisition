# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import pyexcel as pe
import MySQLdb as mysql
import os
import sys
import time
DBNAME="data"
HOST="192.168.0.114"
PASSWORD="123"

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
#     sys.setdefaultencoding(default_encoding)
    
def createDB(cur,db,dbname):
    sql="CREATE DATABASE IF NOT EXISTS "+dbname+" DEFAULT CHARSET utf8"
    cur.execute(sql)
    db.commit()
    print "===========DBNAME:%s========="%dbname

def createTable(cur,db,dbname,tbname,bCreate):
    if not bCreate:
        return
    try:
        dbname = str(dbname).replace('-','').replace('(','').replace(')','')
        tbname = str(tbname).replace('-','').replace('(','').replace(')','')
        sql="CREATE DATABASE IF NOT EXISTS "+dbname+" DEFAULT CHARSET utf8"
        cur.execute(sql)
        db.commit()
        sql="USE "+dbname
        cur.execute(sql)
        db.commit()
        sql="""CREATE TABLE IF NOT EXISTS %s(c1 varchar(40),c2 varchar(40),c3 varchar(40),
        c4 varchar(40),c5 varchar(40),c6 varchar(40),
        c7 varchar(40),c8 varchar(40),c9 varchar(40),
        c10 varchar(40),c11 varchar(40),c12 varchar(40),
        c13 varchar(40),c14 varchar(40),c15 varchar(40),
         c16 varchar(40),c17 varchar(40),c18 varchar(40),
        c19 varchar(40),c20 varchar(40),
        sourceFile varchar(200),updateTime varchar(40) );"""%tbname
        # print "create tb=>%s"%sql
        cur.execute(sql)
        db.commit()
    except BaseException as e:
        db.rollback()
        print "**create table error**"
        print e
        sys.exit(-1)
        
insertSQL = 'insert into {0} (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,sourceFile,updateTime) \
            values (\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\',\'{11}\',\'{12}\', \
            \'{13}\',\'{14}\',\'{15}\',\'{16}\',\'{17}\',\'{18}\',\'{19}\',\'{20}\',\'{21}\',\'{22}\')'

sqlFront = 'insert into {0} (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15, \
            c16,c17,c18,c19,c20,sourceFile,updateTime) values '
            
sqlBack = '(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\', \
            \'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',\'{16}\',\'{17}\',\'{18}\',\'{19}\',\'{20}\',\'{21}\')'

    
def writetoDB(cur,db,dbname,tbname,sourceFile,updateTime,argsList):
#def writetoDB(cur,db,dbname,tbname,sourceFile,updateTime,args):
    tbname = str(tbname).replace('-','').replace('(','').replace(')','')
#     for i,v in enumerate(args):
#         args[i] = v.replace("'",'_').replace("\\","")
#     sql = "insert " + tbname +\
#         " set c1='%s',c2='%s',c3='%s',c4='%s',c5='%s',c6='%s',c7='%s',c8='%s',c9='%s',c10='%s',c11='%s',c12='%s',c13='%s',c14='%s',c15='%s',c16='%s',c17='%s',c18='%s',c19='%s',c20='%s',sourceFile='%s',updateTime='%s'"\
#         %(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],args[12],args[13],args[14],args[15],args[16],args[17],args[18],args[19],sourceFile,updateTime)
  
#     sql = insertSQL.format(tbname, args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],args[12],args[13],args[14],args[15],args[16],args[17],args[18],args[19], sourceFile, updateTime)
    sql = sqlFront.format(tbname)
    values = []
    for args in argsList :
        for i,v in enumerate(args):
            args[i] = v.replace("'",'_').replace("\\","")
        values.append(sqlBack.format(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],args[12],args[13],args[14],args[15],args[16],args[17],args[18],args[19], sourceFile, updateTime))
    sql = sql + ",".join(values)
    try:
        cur.execute(sql)
        db.commit()
    except BaseException as e:
        db.rollback()
        print "write db error:%s"%e
        sys.exit(-1)
        

if __name__=='__main__':  
    startTime = time.time()
    
    conn=mysql.connect(host=HOST,user="root",passwd=PASSWORD)
    conn.set_character_set('utf8')
    cur=conn.cursor()
    

#     if len(sys.argv)!=2:
#         print "Usage:cmd file.xls(x)"
#         sys.exit(1)
# 
#     path=os.path.join(os.getcwd(),sys.argv[1])
    path = 'F:\\gd.xlsx'


    if not os.path.exists(path):
        print "====ERROR:%s can not find"%path
        sys.exit(1)
        
    basename=os.path.basename(path).split('.')[0]
    sourceFile=os.path.basename(path)

    mtime=os.stat(path).st_mtime
    stTime=time.localtime(int(mtime))
    updateTime=time.strftime('%Y-%m-%d %H:%M:%S',stTime)

    now=time.time()

    dbname=DBNAME+time.strftime('%Y%m%d',time.localtime(now))
    createDB(cur,conn,dbname)

    sheetnames=pe.get_book(file_name=path).sheet_names()
    print sheetnames
    for sheetname in sheetnames:
        sheet=pe.get_sheet(file_name=path,sheet_name=sheetname)
        print "==========sheetname:%s========"%sheetname
                   
        bCreate=True
        tbname="tb"+basename+"_"+sheetname
        row = 0
        colsList = []
        for line in sheet:
            createTable(cur,conn,dbname,tbname,bCreate)
            bCreate=False
            cols=[""]*20
#             for i in xrange(1,21):
#                 cols.append(" ") 
            i=0
            for field in line:
                if i>=20:
                    break
                cols[i]=field
                i+=1
            colsList.append(cols)
            row = row + 1
            if row == 100 :
                writetoDB(cur,conn,dbname,tbname,sourceFile,updateTime,colsList)
                row = 0
                colsList = []
#             writetoDB(cur,conn,dbname,tbname,sourceFile,updateTime,cols)
    
    cur.close()  
    conn.close() 
    print "============success===" + str(time.time() - startTime) + "========="
           
