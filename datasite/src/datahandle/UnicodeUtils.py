# -*- coding:utf-8 -*-

"""
汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。
"""

class Unicode(object): 
    
    @staticmethod
    def is_chinese(uchar):
            """判断一个unicode是否是汉字"""
            if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                    return True
            else:
                    return False
                
    @staticmethod 
    def is_number(uchar):
            """判断一个unicode是否是数字"""
            if uchar >= u'\u0030' and uchar<=u'\u0039':
                    return True
            else:
                    return False
     
    @staticmethod
    def is_alphabet(uchar):
            """判断一个unicode是否是英文字母"""
            if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                    return True
            else:
                    return False
     
    @staticmethod
    def is_other(uchar):
            """判断是否非汉字，数字和英文字符"""
            if not (Unicode.is_chinese(uchar) or Unicode.is_number(uchar) or Unicode.is_alphabet(uchar)):
                    return True
            else:
                    return False
     
    @staticmethod
    def B2Q(uchar):
            """半角转全角"""
            inside_code=ord(uchar)
            if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
                    return uchar
            if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                    inside_code=0x3000
            else:
                    inside_code+=0xfee0
            return unichr(inside_code)
    
    @staticmethod
    def Q2B(uchar):
            """全角转半角"""
            inside_code=ord(uchar)
            if inside_code==0x3000:
                    inside_code=0x0020
            else:
                    inside_code-=0xfee0
            if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                    return uchar
            return unichr(inside_code)
     
    @staticmethod
    def stringQ2B(ustring):
            """把字符串全角转半角"""
            return "".join([Unicode.Q2B(uchar) for uchar in ustring])
     
    @staticmethod
    def uniform(ustring):
            """格式化字符串，完成全角转半角，大写转小写的工作"""
            return Unicode.stringQ2B(ustring).lower()
    
    @staticmethod
    def string2List(ustring):
            """将ustring按照中文，字母，数字分开"""
            retList=[]
            utmp=[]
            for uchar in ustring:
                    print uchar
                    if Unicode.is_other(uchar):
                            if len(utmp)==0:
                                    continue
                            else:
                                    retList.append("".join(utmp))
                                    utmp=[]
                    else:
                            utmp.append(uchar)
            print utmp
            if len(utmp)!=0:
                    retList.append("".join(utmp))
            return retList
        
from PinYinUtils import PinYin
 
if __name__=="__main__":
        #test Q2B and B2Q
        #for i in range(0x0020,0x007F):
        #        print Q2B(B2Q(unichr(i))),B2Q(unichr(i))
 
        #test uniform
        ustring=u'中国ａ高频Ａ'
        ustring=Unicode.uniform(ustring)
        print ustring
        for uchar in ustring :
            print Unicode.is_chinese(uchar)
            
        pinYin = PinYin()
        pinYin.load_word()
        convertString = []
        ustring = Unicode.uniform(unicode('手机Email'))
        for uchar in ustring :
            if Unicode.is_chinese(uchar) :
                convertString.append(pinYin.hanzi2pinyin(uchar)[0])
            else :
                convertString.append(uchar)
        print convertString
        newColumn = "".join(convertString)
        print newColumn
        
