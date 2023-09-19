# -*- coding: utf-8 -*-#
import os
import re
import linecache
#NOTE：本文件输入要处理的文件夹目录和输出位置，将输出文件夹下所有.c文件的所有函数位置和起始行以及结尾行
#如 /Users/tingyun/Desktop/graduate/tool/res/hello.c;2;6

outputfile = "all_funcs.txt"
filepath = "/Users/tingyun/Desktop/graduate/wrk_remove_comment"


fp = open(outputfile, "w")
fp.truncate(0)
files = []
rgl = r'\w+(\s|\n|\*)+\w+(\s|\n)*\((\s|\n|!|%|&|\(|\)|\*|\+|,|-|\/|\w|\[|\\|\]|\^|\||~|<{2}|>{2})*?\)(\n|\s)*\{'
rgl_exclude_list = [r'&&', r'\|\|', '->']
pattern = re.compile(rgl)

def getfuncname(line):
    newline = line.replace('\n',' ') #replace不会改变原字符串内容
    words = newline.split("(")
    w = words[0].split(" ")
    funcname1 = w[len(w)-1]
    ##去除开头的如*字符
    f = funcname1.split('*')
    funcname = f[len(f)-1]
    return funcname

def getfilelist(filepath):
    filelist = os.listdir(filepath)  # 得到文件夹下的所有文件名称
    for num in range(len(filelist)):
        filename = filelist[num]
        if os.path.isdir(filepath + "/" + filename):  # 如果是子目录，遍历
            getfilelist(filepath + "/" + filename)
        else:
            if filename.endswith(".c") or filename.endswith(".cpp"):
                files.append(filepath + '/' + filename)
    return files
#
# def newgetline(filename,linenum):
#     #去注释 此步骤在运行前 此函数不可用 使用去注释工具
#     line = linecache.getline(filename, linenum)
#     #while len(line) >= 2 and line[0] == '/' and (line[1] == '/' or line[1] == '*'):
#     while '/' in line or (line and line[0] == '*'):
#         linenum = linenum+1
#         line = linecache.getline(filename, linenum)
#     return line, linenum

def printfilename(filename):
    #判断是否是C文件
    if (filename.endswith(".c") or filename.endswith(".cpp")) == False:
        return
    funcnames = []
    linenum = 1
    while linecache.getline(filename, linenum):
        line = linecache.getline(filename, linenum)
        if line == "" or line == "\n":
            linenum += 1
            continue
        #p1 = "\w+(.*)\("
        line2 = linecache.getline(filename, linenum + 1)
        line3 = linecache.getline(filename, linenum + 2)
        matcher = re.search(pattern, line+line2+line3)
        if matcher:
            #print(line) #输出结果格式如 void authCommand(client *c) {
            #TODO：现已确定函数开头行，找到函数的结尾行
            funcname = getfuncname(line+line2+line3)
            startline = linenum
            endline = startline
            linenum = linenum + 1
            leftnum = line.count('{')
            rightnum = line.count('}')
            while linecache.getline(filename, linenum):
                if leftnum != 0 and leftnum == rightnum :
                    endline = linenum
                    break
                line = linecache.getline(filename, linenum)
                leftnum += line.count('{')
                rightnum += line.count('}')
                if leftnum != 0 and leftnum == rightnum :
                    endline = linenum
                    break
                linenum += 1

            if funcname: #去除部分无法识别的lua函数
                fp.write(filename + ";" + str(startline) + ";" + str(endline) + ";"+funcname +"\n")
            #fp.write(filename+";"+ str(linenum)+"\n")
            # print matcher.group(0)[:-1]
            # functionname = (matcher.group(0)[:-1]).split()[-1]
            # funcnames.append(functionname)
            #print("filename:", filename)


        linenum = linenum + 1
    #print(funcnames)





cfiles = getfilelist(filepath)
for cfile in cfiles:
    print(cfile)
#print("cfiles:", cfiles)
for item in cfiles:
    printfilename(item)

fp.close()

#TODO: 提取文件名和函数开头行
