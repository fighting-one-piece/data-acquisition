#-*- coding:utf-8 -*-

'''
@author: wulin
'''

from DBCUtils import DBOperation

selectTableCountSQL = 'select count(*) from {0}'

def readDatabaseNames():
    databaseNames = []
    results = DBOperation.readList('show databases')
    for result in results :
        databaseName = str(result[0])
        if databaseName.startswith('hj') or databaseName.startswith('hzj') \
             or databaseName.startswith('jsq') or databaseName.startswith('wse') \
                or databaseName.startswith('sb') or databaseName.startswith('wx') \
                    or databaseName.startswith('xx') :
            print 'database %s' %databaseName
            databaseNames.append(databaseName)
    return databaseNames

def readDatabaseTableTotalDatasCount(databaseName):
    tableTotalCount = 0
    useDatabaseSQL = 'use {0}'.format(databaseName)
    DBOperation.execute(useDatabaseSQL)
    print useDatabaseSQL
    results = DBOperation.readList('show tables')
    for result in results :
        tableName = str(result[0])
        print tableName
        tableCount = DBOperation.readOne(selectTableCountSQL.format(tableName))
        #print '%s -- %s' %(tableName, tableCount[0])
        tableTotalCount = tableTotalCount + tableCount[0]
    print '%s total datas count %s' %(databaseName, tableTotalCount)
    return tableTotalCount
    
    
if __name__ == '__main__':
    totalDatasCount = 0;
    databaseNames = readDatabaseNames()
    for databaseName in databaseNames :
        totalDatasCount = totalDatasCount + readDatabaseTableTotalDatasCount(databaseName)
    print 'all database total datas count %s' %totalDatasCount
        
        
        