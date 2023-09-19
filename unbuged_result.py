import linecache
import json
#TODO:在这里确定文件位置，文件输出位置和pythonfile在同一个文件夹下就不用管
all_func_file = "/Users/tingyun/Desktop/graduate/tool/all_funcs.txt"
bug_func_file = "/Users/tingyun/Desktop/graduate/tool/bug_funcs.txt"
filepath = "/Users/tingyun/Desktop/graduate/wrk_remove_comment"
outputfile = "nobug_funcs.txt"
outputjson = "nobug_funcs.json"
product_name = "wrk"
download_link = "https://github.com/wg/wrk.git"
commit_version = "a211dd5a7050b1f9e8a9870b95513060e72ac4a0"
parent_commit = "2d433a9b43cfdabe4a76a29a4a352b6eb93be3a2"
newbug_file = "new_bug_funcs.txt"

newbug_fp = open(newbug_file, "w")
newbug_fp.truncate(0)

fp = open(outputfile, "w")
fp.truncate(0)

fp = open(outputfile, "w")
fp.truncate(0)
jsonfp = open(outputjson, "w")
jsonfp.truncate(0)
func_dict = {}

bug_dict = {}
linenum = 1
while linecache.getline(bug_func_file, linenum):
    line = linecache.getline(bug_func_file, linenum)
    #print(line)
    #deps/hdr_histogram/hdr_histogram.c;98;knownConditionTrueFalse
    words = line.split(";")
    words[2] = words[2].replace("\n","")
    if words[0] in bug_dict:
        bug_dict[words[0]].append(words[1]+";"+words[2])
    else:
        bug_dict[words[0]] = [(words[1]+";"+words[2])]

    linenum += 1

#print(bug_dict)

id = 1
while linecache.getline(all_func_file, linenum):
    line = linecache.getline(all_func_file, linenum)
    #print(line)
    #/Users/tingyun/Desktop/graduate/tool/res/hello.c;2;6;funcname
    words = line.split(";")
    #print(line)
    filename = words[0][len(filepath)+1:]
    startline = int(words[1])
    endline = int(words[2])
    #funcname = words[3]
    #print(filename)
    bug_list = []
    if filename in bug_dict:
        bug_list = bug_dict[filename]
    ifbug = False
    # if filename == "builtin/fsck.c" and startline == 466:
    #     a = 1
    for num in bug_list:
        nums = num.split(";")
        if int(nums[0]) in range(startline,endline):
            newbug_fp.write(filename+";"+nums[0]+";"+ nums[1] + ";"+ words[3].replace('\n', '')+";" + str(startline)+";"+str(endline)+"\n")
            ifbug = True
            #break
    if ifbug == False:
        #print(filename+";"+words[1]+";"+words[2])
        func_piece = {
            "id": id,
            "cwe": "None",
            "if_buged":False,
            "product": product_name,
            "functions": [
                {
                    "file": filename,
                    "name": words[3].replace('\n', ''),
                    "line_range": [
                        words[1],
                        words[2]
                    ],
                    "def_range": [

                    ]
                }
            ],
            "CommitVersion": commit_version,
            "ParentCommit": parent_commit,
            "Repo_url": download_link,
            #"DownloadLink": download_link
        }
        func_dict[id] = func_piece
        id += 1
        fp.write(filename+";"+words[1]+";"+words[2]+";"+words[3])

    linenum += 1

json.dump(func_dict, jsonfp, indent=4, ensure_ascii=False)
fp.close()
jsonfp.close()
newbug_fp.close()
print("done!")
