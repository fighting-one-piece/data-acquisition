# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import MySQLdb  
  
from DBUtils.PooledDB import PooledDB  
  
class DBOperation(object):  
      
    __pool = None  
     
    @staticmethod  
    def getConnection():  
        if DBOperation.__pool is None :  
            __pool = PooledDB(creator = MySQLdb,  
                              mincached = 1,  
                              maxcached = 20,  
                              host = '192.168.0.114',  
                              port = 3306,  
                              user = 'root',  
                              passwd = '123',  
                              db = 'wl20160607',  
                              charset = 'utf8')  
  
        return __pool.connection()  
 
    @staticmethod  
    def getCursor():  
        connection = DBOperation.getConnection()  
        return connection.cursor()  
 
    @staticmethod  
    def execute(sql, parameter=None):  
        dbConnection = DBOperation.getConnection()  
        cursor = dbConnection.cursor()
        if parameter is None:  
            cursor.execute(sql)  
        else :  
            cursor.execute(sql, parameter)  
        dbConnection.commit() 
        cursor.close() 
        dbConnection.close()  
     
    @staticmethod  
    def readOne(sql, parameter=None):  
        dbConnection = DBOperation.getConnection()  
        cursor = dbConnection.cursor()
        if parameter is None :  
            count = cursor.execute(sql)  
        else :  
            count = cursor.execute(sql, parameter)  
        if count > 0:  
            return cursor.fetchone()  
        else :  
            return None  
        dbConnection.commit()  
        cursor.close()
        dbConnection.close()  
         
    @staticmethod  
    def readList(sql, parameter=None):  
        dbConnection = DBOperation.getConnection() 
        cursor = dbConnection.cursor() 
        if parameter is None :  
            count = cursor.execute(sql)  
        else :  
            count = cursor.execute(sql, parameter)  
        if count > 0:  
            return cursor.fetchall()  
        else :  
            return None  
        dbConnection.commit()  
        cursor.close()
        dbConnection.close()  
     
    @staticmethod  
    def commitConnection(connection):  
        if connection :  
            connection.commit()  
             
    @staticmethod  
    def closeConnection(connection):  
        if connection :  
            connection.close() 


