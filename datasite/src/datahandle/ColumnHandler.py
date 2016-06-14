# -*- coding:utf-8 -*-
'''
@author: wulin
'''
import sys
from DBCUtils import DBOperation
from PinYinUtils import PinYin
from UnicodeUtils import Unicode

reload(sys)

print sys.getdefaultencoding()

showColumnsMetaSQL = 'select COLUMN_NAME, ORDINAL_POSITION, COLUMN_TYPE from \
                     information_schema.columns where table_name= \'{0}\''

showColumnMetaSQL = 'select COLUMN_NAME, ORDINAL_POSITION, COLUMN_TYPE from \
                     information_schema.columns where table_name= \'{0}\' and column_name = \'{1}\''
                     
showColumnSQL = 'select a.c1,a.c2,a.c3,a.c4,a.c5,a.c6,a.c7,a.c8,a.c9,a.c10,a.c11,a.c12,a.c13,a.c14,a.c15 from ( \
                    select @rownum:=@rownum+1 rownum, t.* from ( \
                        select @rownum:=0, {0}.* from {0}) t) a where a.rownum = 1;'
    
updateColumnNameSQL = 'alter table {0} change {1} {2} {3}'
    
deleteSQL = 'delete from {0} where c1 = (select a.c1 from ( \
                select @rownum:=@rownum+1 rownum, t.* from ( \
                    select @rownum:=0, {0}.* from {0}) t) a where a.rownum = 1)'
                    
def handle(tableName, columns, isDeleted = False):
    columnsMeta = DBOperation.readList(showColumnsMetaSQL.format(tableName))
    columnNTMap = {}
    for columnMeta in columnsMeta :
        columnNTMap[columnMeta[0]] = columnMeta[2]
    
    columnData = DBOperation.readOne(showColumnSQL.format(tableName))
    
    if isDeleted :
        DBOperation.execute(deleteSQL.format(tableName))

    index = 0
    pinYin = PinYin()
    pinYin.load_word()
    for columnMeta in columnsMeta :
        oldColumn = columnMeta[0]
        columnType = columnMeta[2]
        
        if columns.has_key(oldColumn) :
            newColumn = columns[oldColumn]
        else :
            if columnData[index] is None : continue
            convertString = []
            ustring = Unicode.uniform(unicode(columnData[index]))
            for uchar in ustring :
                if Unicode.is_chinese(uchar) :
                    convertString.append(pinYin.hanzi2pinyin(uchar)[0])
                else :
                    convertString.append(uchar)
            newColumn = "".join(convertString)
        print '%s %s %s' %(oldColumn, newColumn, columnType)
        DBOperation.execute(updateColumnNameSQL.format(tableName, oldColumn, newColumn, columnType))
        index = index + 1
    

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
    
    