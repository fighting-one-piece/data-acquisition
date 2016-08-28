# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import os
import re
import sys
import xlrd
import time
import datetime
import MySQLdb as mysql


DBNAME = "data"
HOST = "192.168.0.114"
USER = "root"
PASSWORD = "123"

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    #sys.setdefaultencoding(default_encoding)
    
def createDB(cur, db, dbname):
    sql = "CREATE DATABASE IF NOT EXISTS "+dbname+" DEFAULT CHARSET utf8"
    cur.execute(sql)
    db.commit()
    print "===========DBNAME:%s========="%dbname

def createTable(cur,db,dbname,tbname,bCreate):
    if not bCreate:
        return
    try:
        dbname = str(dbname).replace('-','').replace('(','').replace(')','')
        tbname = str(tbname).replace('-','').replace('(','').replace(')','')
        sql = "CREATE DATABASE IF NOT EXISTS "+dbname+" DEFAULT CHARSET utf8"
        cur.execute(sql)
        db.commit()
        sql="USE "+dbname
        cur.execute(sql)
        db.commit()
        sql = """CREATE TABLE IF NOT EXISTS %s(c1 varchar(40),c2 varchar(40),c3 varchar(40),
        c4 varchar(40),c5 varchar(40),c6 varchar(40),
        c7 varchar(40),c8 varchar(40),c9 varchar(40),
        c10 varchar(40),c11 varchar(40),c12 varchar(40),
        c13 varchar(40),c14 varchar(40),c15 varchar(40),
         c16 varchar(40),c17 varchar(40),c18 varchar(40),
        c19 varchar(40),c20 varchar(40),
        sourceFile varchar(200),updateTime varchar(40) );"""%tbname
        cur.execute(sql)
        db.commit()
    except BaseException as e:
        db.rollback()
        print "**create table error**"
        print e
        sys.exit(-1)
        
sqlFront = 'insert into {0} (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15, \
            c16,c17,c18,c19,c20,sourceFile,updateTime) values '
            
sqlBack = '(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\', \
            \'{11}\',\'{12}\',\'{13}\',\'{14}\',\'{15}\',\'{16}\',\'{17}\',\'{18}\',\'{19}\',\'{20}\',\'{21}\')'

    
def writetoDB(cur, db, dbname, tbname, sourceFile, updateTime, argsList):
    tbname = str(tbname).replace('-','').replace('(','').replace(')','')
    sql = sqlFront.format(tbname)
    values = []
    for args in argsList :
        for i,v in enumerate(args):
            args[i] = str(v).replace("'",'_').replace("\\","")
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
    startTime = datetime.datetime.now()
    
    conn = mysql.connect(host = HOST, user = USER, passwd = PASSWORD)
    conn.set_character_set('utf8')
    cur = conn.cursor()

    #if len(sys.argv)!=2:
    #    print "Usage:cmd file.xls(x)"
    #    sys.exit(1)

    #path=os.path.join(os.getcwd(),sys.argv[1])

    #if not os.path.exists(path):
    #    print "====ERROR:%s can not find"%path
    #    sys.exit(1)
    path = u"F://2008年10月北京市阀门配件产品生产销售企业名录数据库(二次开发).xls"
    #path = u"F://2008年10月北京市阀门配件产品生产销售企业名录数据库(二).xls"
        
    basenames = os.path.basename(path).split('.')
    if len(basenames) == 2 :
        basename = basenames[0]
    else :
        basename = ''.join(basenames[0:len(basenames) - 1])
    #basename = os.path.basename(path).split('.')[0]
    sourceFile = os.path.basename(path)

    mtime = os.stat(path).st_mtime
    stTime = time.localtime(int(mtime))
    updateTime = time.strftime('%Y-%m-%d %H:%M:%S',stTime)

    now = time.time()

    dbname = DBNAME + time.strftime('%Y%m%d',time.localtime(now))
    createDB(cur, conn, dbname)
    
    workbook = xlrd.open_workbook(path)
    for sheet in workbook.sheets() :
        print "==========sheetname:%s========" %(sheet.name)
       
        bCreate = True
        sheetName = str(sheet.name).replace('.','').replace(' ', '')
        tbname = "tb" + basename + "_" + sheetName
        tbname = str(tbname).replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('、','')
        
        tbname_len = len(tbname.decode('utf-8'))
        if tbname_len >= 54 :
            tbname = tbname.decode('utf-8')[tbname_len - 54 : tbname_len].encode('utf-8')
            tbname = "tb" + tbname
            print tbname
        '''
        if len(tbname) >= 120 :
            tmp_tbname = []
            for i in xrange(len(tbname)):
                print tbname[i]
                tmp_tbname.append(tbname[i])
            tmp_tbname.reverse()  
            print  ''.join(tmp_tbname)
            total_len = 0
            new_tbname = []
            for tmp_name in tmp_tbname :
                if re.compile(u"[\u4e00-\u9fa5]").match(tmp_name) :
                    total_len = total_len + 3
                else :
                    total_len = total_len + 1
                if total_len > 130 : break
                new_tbname.append(tmp_name)
            tbname = "tb" + ''.join(new_tbname)
        '''    
        
        row = 0
        colsList = []
        
        nrows = sheet.nrows
        ncols = sheet.ncols
        print 'rows : %s -- cols : %s' %(nrows, ncols)
        for r in range(nrows) :
            createTable(cur,conn,dbname,tbname,bCreate)
            bCreate = False
            cols = [""]*20
            i = 0
            for c in range(ncols) :
                if i >= 20:
                    break
                if sheet.row(r)[c].ctype == 1:
                    try :
                        cvalue=str(sheet.row(r)[c].value)
                        if cvalue.startswith('+'):
                            cvalue=float(cvalue.replace('+', ''))
                        cols[i]=cvalue
                    except Exception as e :
                        print '%s rows %s cols error value: %s' %(r, c, sheet.cell_value(r, c))
                elif sheet.row(r)[c].ctype == 2:
                    cols[i]=int(sheet.row(r)[c].value)
                elif sheet.row(r)[c].ctype == 3:
                    try :
                        date_tuple = xlrd.xldate_as_tuple(sheet.cell_value(r, c), workbook.datemode)  
                        cols[i] = datetime.date(*date_tuple[:3]).strftime('%Y/%m/%d')
                    except Exception as e :
                        print '%s rows %s cols error value: %s' %(r, c, sheet.cell_value(r, c))
                else :
                    cols[i]=sheet.row(r)[c].value
                i+=1
            colsList.append(cols)
            row = row + 1
            if (row % 100 == 0) or (row == nrows) :
                writetoDB(cur, conn, dbname, tbname, sourceFile, updateTime, colsList)
                colsList = []
    cur.close()  
    conn.close() 
    endTime = datetime.datetime.now()
    print "import database success ! spend time %s seconds" %((endTime - startTime).seconds)
           
