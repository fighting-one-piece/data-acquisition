# -*- coding:utf-8 -*-

'''
@author: wulin
'''

from DBCUtils import DBOperation

def showTableMetaInfo(tableName) :
    sql = 'select * from ' + tableName
    connection = DBOperation.getConnection()
    cursor = connection.cursor()
    count = cursor.execute(sql)
    if count > 0 :
        result = cursor.fetchone()
#         print '%s-%s-%s-%s-%s-%s-%s-%s-%s-%s' \
#             %(result[0], result[1], result[2], result[3], 
#               result[4], result[5], result[6], result[7], 
#               result[8], result[9])
        key = '{0}-{1}-{2}-{3}-{4}-{5}-{6}-{7}-{8}-{9}'.format(
                    result[0], result[1], result[2], result[3], 
                    result[4], result[5], result[6], result[7], 
                    result[8], result[9])
        print key + ' || ' + tableName
    cursor.close()  
    cursor.close()

sql = 'show tables'
connection = DBOperation.getConnection()
cursor = connection.cursor()
count = cursor.execute(sql)
if count > 0 :
    results = cursor.fetchall()
    for result in results :
        showTableMetaInfo(result[0])
cursor.close()  
cursor.close()

