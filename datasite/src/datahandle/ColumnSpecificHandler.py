# -*- coding:utf-8 -*-
'''
@author: wulin
'''
import sys
from DBCUtils import DBOperation


showColumnMetaSQL = 'select COLUMN_NAME, ORDINAL_POSITION, COLUMN_TYPE from \
                     information_schema.columns where table_name= \'{0}\' and column_name = \'{1}\''
    
updateColumnNameSQL = 'alter table {0} change {1} {2} {3}'
    
deleteSQL = 'delete from {0} where c1 = (select a.c1 from ( \
                select @rownum:=@rownum+1 rownum, t.* from ( \
                    select @rownum:=0, {0}.* from {0}) t) a where a.rownum = 1)'

def handle(tableName, columns, isDeleted = False):
    if isDeleted :
        DBOperation.execute(deleteSQL.format(tableName))
    for column in columns.keys() :
        result = DBOperation.readOne(showColumnMetaSQL.format(tableName, column))
        DBOperation.execute(updateColumnNameSQL.format(tableName, column, columns[column], result[2]))

if __name__ == '__main__' :
    print 'args %s' %len(sys.argv)
    print 'arg1 %s' %sys.argv[1]
    print 'arg2 %s' %sys.argv[2]
    argvLen = len(sys.argv)
    tableName = sys.argv[1]
    columnChangeInfos = sys.argv[2]
    columns = {}
    if columnChangeInfos.find(',') == -1 :
        columnKV = str(columnChangeInfos).split(":")
        columns[columnKV[0]] = columnKV[1]
    else :
        columnKVSS = str(columnChangeInfos).split(",")
        for columnKVS in columnKVSS :
            columnKV = str(columnKVS).split(":")
            columns[columnKV[0]] = columnKV[1]
    isDeleted = False if '0' == sys.argv[3] else True if argvLen > 3 else False
    print 'columns %s' %columns
    print 'isDeleted %s' %isDeleted
    handle(tableName, columns, isDeleted)
    
    
    