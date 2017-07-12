#!/usr/bin/env python3
import os
import zipfile
import time
import configparser
import multiprocessing

def unzip_dir(srcpath,dstPath):
    os.chdir(srcpath)
    file_list = os.listdir(srcpath)
    for file_name in file_list:
        fi_d=srcpath+'/'+file_name
        if os.path.isdir(fi_d):
            print ('fi_d',fi_d) 
            unzip_dir(fi_d,dstPath)     
        else:
            r = zipfile.is_zipfile(srcpath+'\\'+file_name)
            #print ('fi_d2',fi_d) 
            print ("zipfile",r)
            if r:
                mm=os.path.join(dstPath,os.path.splitext(file_name)[0])
                fileszippath=srcpath+'/'+file_name
                print (fileszippath) 
                if not os.path.exists(os.path.join(dstPath,os.path.splitext(file_name)[0])):
                    #在指定目录创建解压后的目标文件夹
                    os.mkdir(os.path.join(dstPath, os.path.splitext(file_name)[0]))
                    ziphandle = zipfile.ZipFile(os.path.join(srcpath, file_name), "r")
                    #开始解压缩文件
                    try:
                        file_size_first = 0
                        file_size_second = 0
                        file_size_first = os.path.getsize(os.path.join(srcpath, file_name))
                        #暂停0.2秒
                        time.sleep(0.2)
                        file_size_second = os.path.getsize(os.path.join(srcpath, file_name))
                        #判断是不是在传输文件
                        if (file_size_first == file_size_second) and file_size_second > 0:
                            #调用ziphandle进行解压程序
                            ziphandle.extractall(os.path.join(dstPath, os.path.splitext(file_name)[0]))
                            fileszippath=srcpath+'/'+file_name
                            print (fileszippath)
                    except:
                         print('文件损坏' + file_name)
                    ziphandle.close()
                    os.remove(fileszippath)
        
def call_unzipprocess(srcpath, dstPath):
    i = 0
    while i<1:
        unzip_dir(srcpath, dstPath)
        time.sleep(5)

if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("uzf.conf")
    cf.sections()
    sourcestr = cf.get('zipdir', 'sourcelist')
    sourceslist = sourcestr.split(',')
    poolnum = len(sourceslist)
    pool = multiprocessing.Pool(processes = poolnum)
    for sourcename in sourceslist:
        srcp = cf.get(sourcename, 'srcpath')
        dstp = cf.get(sourcename, 'dstpath')
        pool.apply_async(call_unzipprocess, (srcp, dstp,))
    pool.close()
    pool.join()


