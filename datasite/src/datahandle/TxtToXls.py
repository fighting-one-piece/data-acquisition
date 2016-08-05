# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import os
import sys
import xlwt
#import codecs
import datetime

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    #sys.setdefaultencoding(default_encoding)
    

if __name__=='__main__':  
    startTime = datetime.datetime.now()
    
    #if len(sys.argv)!=2:
    #    print "Usage:cmd file.xls(x)"
    #    sys.exit(1)

    #path=os.path.join(os.getcwd(), sys.argv[1])

    path = "F://2.txt"
    if not os.path.exists(path):
        print "ERROR: %s can not find" %path
        sys.exit(1)
        
    xlsxPath = os.path.join(os.path.dirname(path), 
        os.path.splitext(os.path.basename(path))[0] + '.xls')
        
    workbook = xlwt.Workbook(encoding='utf-8')  
    
    BUFSIZE = 1024
    with open(path, 'r') as f:
        nrows, total_rows = 0, 0
        lines = f.readlines(BUFSIZE)
        while lines:
            for line in lines:
                if (nrows % 20000 == 0) :
                    wsheet = workbook.add_sheet('sheet' + str(total_rows), cell_overwrite_ok = True)
                    nrows = 0
                values = line.split(',')
                for ncol in xrange(len(values)):
                    print '%s %s %s' %(nrows, ncol, values[ncol])
                    wsheet.write(nrows, ncol, values[ncol])  
                nrows = nrows + 1
                total_rows = total_rows + 1
            lines = f.readlines(BUFSIZE)
    
    
    
    #with codecs.open(path, 'r', 'utf-8') as text:
    #with open(path, 'r') as text:
    #    nrows, total_rows = 0, 0
    #    for line in text.readlines():
    #        if (nrows % 100 == 0) :
    #            wsheet = workbook.add_sheet('sheet' + str(total_rows), cell_overwrite_ok = True)
    #            nrows = 0
    #        values = line.split(',')
    #        for ncol in xrange(len(values)):
    #            print '%s %s %s' %(nrows, ncol, values[ncol])
    #            wsheet.write(nrows, ncol, values[ncol])  
    #        nrows = nrows + 1
    #        total_rows = total_rows + 1
            
    workbook.save(xlsxPath)  
    endTime = datetime.datetime.now()
    print "import database success ! spend time %s seconds" %((endTime - startTime).seconds)
           
