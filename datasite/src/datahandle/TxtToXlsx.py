# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import os
import sys
import datetime
import xlsxwriter

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    # sys.setdefaultencoding(default_encoding)
    

if __name__ == '__main__':  
    startTime = datetime.datetime.now()
    
    # if len(sys.argv)!=2:
    #    print "Usage:cmd file.xls(x)"
    #    sys.exit(1)

    # path=os.path.join(os.getcwd(), sys.argv[1])

    path = "F://3.txt"
    if not os.path.exists(path):
        print "ERROR: %s can not find" % path
        sys.exit(1)
        
    xlsxPath = os.path.join(os.path.dirname(path),
        os.path.splitext(os.path.basename(path))[0] + '.xlsx')
        
    workbook = xlsxwriter.Workbook(xlsxPath)
    
    BUFSIZE = 1024
    with open(path, 'r') as f:
        nrows, total_rows, sheet_num = 0, 0, 0
        lines = f.readlines(BUFSIZE)
        while lines:
            for line in lines:
                if (total_rows % 1000000 == 0) :
                    worksheet = workbook.add_worksheet(name = 'sheet' + str(sheet_num))
                    nrows = 0
                    sheet_num = sheet_num + 1
                values = line.split(',')
                for ncol in xrange(len(values)):
                    #print '%s %s %s' %(nrows, ncol, values[ncol])
                    worksheet.write(nrows, ncol, values[ncol])  
                nrows = nrows + 1
                total_rows = total_rows + 1
            lines = f.readlines(BUFSIZE)
    
    
    #worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    #worksheet.set_column('A:A', 20)

    # Add a bold format to use to highlight cells.
    #bold = workbook.add_format({'bold': True})

    # Write some simple text.
    #worksheet.write('A1', 'Hello')

    # Text with formatting.
    #worksheet.write('A2', 'World', bold)

    # Write some numbers, with row/column notation.
    #worksheet.write(2, 0, 123)
    #worksheet.write(3, 0, 123.456)

    # Insert an image.
    #worksheet.insert_image('B5', 'logo.png')

    workbook.close()

    endTime = datetime.datetime.now()
    print "import database success ! spend time %s seconds" % ((endTime - startTime).seconds)
           
