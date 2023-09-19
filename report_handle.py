#coding=utf-8
import  xml.dom.minidom
import xml.etree.ElementTree as ET
import linecache
from pyquery import PyQuery as pq
from xml.etree.ElementTree import Element
#TODO：在这里确认report文件路径
dom = ET.parse('cpp_check_result.xml') #CPPcheck的XML结果
infer_report = '/Users/tingyun/Desktop/graduate/tool/infer_result.txt' #infer TXT结果
csa_result = '/Users/tingyun/Desktop/graduate/tool/index.html'
outputfile = "bug_funcs.txt"

fp = open(outputfile, "w")
fp.truncate(0)

#CPPcheck结果处理
root = dom.getroot()
id = 0
bug_dict = {}
for child in root:
    print("tag:", child.tag)
    print("text:", child.text)
    print("attrib:", child.attrib)
    if child.tag == "errors":
        for error_elements in child: # [0]error [1]location [2]...
            errortype = error_elements.attrib['id']
            #print(errortype)
            for error_element in error_elements:
                if error_element.tag == "location": # 只读取所有的错误location信息 file 和 line
                    #print("tag:", error_element.tag)
                    #print("attrib:", error_element.attrib)
                    #print(error_element.attrib['file']+";"+error_element.attrib['line']+";"+errortype)
                    #TODO: 输出到文件
                    key = (error_element.attrib['file']+";"+error_element.attrib['line']+";"+errortype).replace("\n", "")
                    if key not in bug_dict:
                        id += 1
                        bug_dict[key] = 1
                        fp.write(error_element.attrib['file']+";"+error_element.attrib['line']+";"+errortype+"\n")

print("CPP check report handle done! id = ", id)

#infer结果处理
linenum1 = 1
while linecache.getline(infer_report, linenum1):
    line = linecache.getline(infer_report, linenum1)
    if line and line[0] == '#':
        linenum1 = linenum1 + 1
        line2 = linecache.getline(infer_report, linenum1)
        #src/sort.c:40: error: Null Dereference
        info = line2.split(':')
        errorfile = info[0]
        errorline = info[1]
        errortype = info[3]
        #print(errorfile+";"+errorline+";"+errortype)
        # TODO: 输出到json文件
        id += 1
        fp.write(errorfile+";"+errorline+";"+errortype)
    linenum1 = linenum1 + 1

print("infer report handle done! id = ", id)


with open(csa_result, encoding='utf-8') as f:
    html = f.read()

# 直接在 pyQuery 里面导入本地文件，可能会存在 GBK 编码错误，所以这里使用 with open 方法打开文件，传递给 pyQuery
html = pq(html)('tr')
#print(html)
res = html.items()

#由于scan-build报告只有文件名不带路径，因此需要手动确认唯一路径
path_dict = {'t_zset.c': 'src/t_zset.c', 'acl.c': 'src/acl.c', 'quicklist.c': 'src/quicklist.c', 'sha1.c': 'src/sha1.c',
             't_string.c': 'src/t_string.c', 'server.c': 'src/server.c', 'config.c': 'src/config.c', 'redis-cli.c': 'src/redis-cli.c',
             'sort.c': 'src/sort.c', 'debug.c': 'src/debug.c', 'listpack.c': 'src/listpack.c', 'db.c': 'src/db.c',
             'redis-check-rdb.c': 'src/redis-check-rdb.c', 'cluster.c': 'src/cluster.c',  'sentinel.c': 'src/sentinel.c',
             't_stream.c': 'src/t_stream.c', 'dict.c': 'judge', 'module.c': 'src/module.c', 'rax.c': 'src/rax.c',
             'redis-check-aof.c': 'src/redis-check-aof.c', 'setproctitle.c': 'src/setproctitle.c', 'util.c': 'src/util.c',
             'sds.h':'judge', 'bitops.c': 'src/bitops.c', 'aof.c': 'src/aof.c'}
# dict.c sds.h
#print(res)
for r in res:
    t = r.text()
    words = t.split("\n")
    #['Logic error', 'Result of operation is garbage or undefined', 'aof.c', 'loadAppendOnlyFiles', '1660', '17', 'View Report']

    if len(words) >= 6:
        #path line errortype
        #print(words[2]+";"+words[4]+";"+words[1])
        id += 1
        fp.write(words[2]+";"+words[4]+";"+words[1]+"\n")


f.close()
fp.close()

print("CSA report handle done! id = ", id)