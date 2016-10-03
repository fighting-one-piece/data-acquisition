# -*- encoding: utf-8 -*-

'''
@author: wulin
'''

path = 'f:\\document\\temp'

import os

file_map = {}
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames :
        file_path = os.path.join(dirpath, filename)
        file_size = os.path.getsize(file_path)
        key = filename + '_' + str(file_size)
        if file_map.has_key(key) :
            print file_path
        else :
            file_map[key] = file_path
        #os.remove(f)
print file_map
for k, v in file_map.items() :
    print v
    
