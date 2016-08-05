# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import os
import sys
import xlrd
import xlwt
import datetime
import ConfigParser

class file_openate(object):
    
    def __init__(self):
        #初如化读取数据库配置
        dir_config = ConfigParser.ConfigParser()
        file_config = open('config.ini', "rb")
        dir_config.readfp(file_config)
        self.dir1 = str(dir_config.get("global", "dir1"))
        self.dir1 = unicode(self.dir1, 'utf8')
        self.dir2 = str(dir_config.get("global", "dir2"))
        self.dir2 = unicode(self.dir2, 'utf8')
        file_config.close()
        
    def file_list(self):
        input_name_han = "软件有不确认性,前期使用最好先备份,以免发生数据丢失,确认备份后,请输入要分割的字节大小,按b来计算".decode('utf-8')
        print input_name_han
        while 1:
            input_name=raw_input("number:")
            if input_name.isdigit():
                input_name = int(input_name)
                os.chdir(self.dir1)
                for filename in os.listdir(self.dir1):
                    os.chdir(self.dir1)
                    #print filename
                    name, ext = os.path.splitext(filename)
                    file_size = int(os.path.getsize(filename))
                    f = open(filename, 'r')
                    chu_nmuber = 0
                    while file_size >= 1:
                        #print file_size
                        chu_nmuber = chu_nmuber + 1
                        if file_size >= input_name:
                            file_size = file_size - input_name
                            a = f.read(input_name)
                            os.chdir(self.dir2)
                            filename1 = name + '-' + str(chu_nmuber) + ext
                            new_f = open(filename1, 'a')
                            new_f.write(a)
                            new_f.close()
                            #print file_size
                        else:
                            a = f.read()
                            os.chdir(self.dir2)
                            filename1 = name + '-' + str(chu_nmuber) + ext
                            new_f = open(filename1, 'a')
                            new_f.write(a)
                            new_f.close()
                            break
                    print "分割成功".decode('utf-8') + filename
                    f.close()
            else:
                print "请输入正确的数字,请重新输入".decode('utf-8')
                
        
class SplitFiles():
    """按行分割文件"""
    def __init__(self, file_name, line_count=200):
        """初始化要分割的源文件名和分割后的文件行数"""
        self.file_name = file_name
        self.line_count = line_count
        
    def split_file(self):
        if self.file_name and os.path.exists(self.file_name):
            try:
                with open(self.file_name) as f : # 使用with读文件
                    temp_count = 0
                    temp_content = []
                    part_num = 1
                    for line in f:
                        if temp_count < self.line_count:
                            temp_count += 1
                        else :
                            self.write_file(part_num, temp_content)
                            part_num += 1
                            temp_count = 1
                            temp_content = []
                        temp_content.append(line)
                    #else : # 正常结束循环后将剩余的内容写入新文件中
                        self.write_file(part_num, temp_content)
            except IOError as err:
                print(err)
        else:
            print("%s is not a validate file" % self.file_name)
            
    def get_part_file_name(self, part_num):
        """"获取分割后的文件名称：在源文件相同目录下建立临时文件夹temp_part_file，然后将分割后的文件放到该路径下"""
        temp_path = os.path.dirname(self.file_name) # 获取文件的路径（不含文件名）
        part_file_name = temp_path + "temp_part_file"
        if not os.path.exists(part_file_name) : # 如果临时目录不存在则创建
            os.makedirs(part_file_name)
        part_file_name += os.sep + "temp_file_" + str(part_num) + ".part"
        return part_file_name
    
    def write_file(self, part_num, *line_content):
        """将按行分割后的内容写入相应的分割文件中"""
        part_file_name = self.get_part_file_name(part_num)
        #print(line_content)
        try :
            with open(part_file_name, "w") as part_file:
                for line in line_content :
                    part_file.writelines(line)
        except IOError as err:
            print(err)
            
def readSheet(filePath, sheetIndex = 0):  
    if not os.path.exists(filePath):  
        print '%s is not exist' %filePath  
        sys.exit(0)  
    startTime = datetime.datetime.now()  
    workbook = xlrd.open_workbook(filePath)  
    sheet = workbook.sheet_by_index(sheetIndex)  
    nrows = sheet.nrows  
    if nrows == 0:  
        print '%s no data need to read' %filePath  
        sys.exit(0)  
    trow = 2 if nrows > 1 else 1  
    ncols = sheet.ncols  
    types = [sheet.row(trow)[i].ctype for i in xrange(ncols)]  
    datas = [[] * ncols for i in xrange(nrows)]  
    for r in xrange(nrows):  
        for c in xrange(ncols):  
            if (sheet.cell(r, c).ctype == 3):  
                date_tuple = xlrd.xldate_as_tuple(sheet.cell_value(r, c), workbook.datemode)  
                date_value = datetime.date(*date_tuple[:3]).strftime('%Y/%m/%d')  
                datas[r].append(date_value)  
            else :  
                datas[r].append(sheet.row(r)[c].value)  
    endTime = datetime.datetime.now()  
    print 'read %s spend time %s seconds' %(filePath, (endTime - startTime).seconds)  
    return (sheet.name, types, datas)  
      
def writeSheet(sheet, fileDir):  
    startTime = datetime.datetime.now()  
    if not os.path.exists(fileDir):  
        os.mkdir(fileDir)  
    filePath = fileDir + os.sep + 'tmp.xls'  
    workbook = xlwt.Workbook(encoding='utf-8')  
    wsheet = workbook.add_sheet(sheet[0], cell_overwrite_ok = True)  
    #style = xlwt.easyxf('font: height 300, name SimSun, bold 1, color red;')  
    font = xlwt.Font()  
    font.name = 'Times New Roman'  
    font.bold = True  
    font.height = 300  
    font.colour_index = 2  
    style = xlwt.XFStyle()  
    style.font = font  
    #style.num_format_str= 'YYYY-MM-DD'  
    #style.num_format_str = '$#,##0.00'  
    datas = sheet[2]  
    nrows = len(datas)  
    ncols = len(datas[0])  
    for ncol in xrange(ncols):  
        wsheet.col(ncol).width = 256 * 30  
        #wsheet.col(ncol).collapse = 1  
        #wsheet.col(ncol).best_fit = 1  
    for r in xrange(nrows):  
        for c in xrange(ncols):  
            wsheet.write(r, c, datas[r][c], style)  
    workbook.save(filePath)  
    endTime = datetime.datetime.now()  
    print 'write data to %s spend time %s seconds' %(fileDir, (endTime - startTime).seconds)  

            
if __name__ == "__main__":
#     file_name = file_openate()
#     file_name.file_list()
    
    sf = SplitFiles(r"F:\a.txt", 20)
    sf.split_file()

       
                