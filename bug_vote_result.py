import linecache
import json
import copy
all_func_file = "/Users/tingyun/Desktop/graduate/tool/all_funcs.txt"
bug_func_file = "/Users/tingyun/Desktop/graduate/tool/new_bug_funcs.txt"
filepath = "/Users/tingyun/Desktop/graduate/wrk_remove_comment"
product_name = "wrk"
download_link = "https://github.com/wg/wrk.git"
commit_version = "a211dd5a7050b1f9e8a9870b95513060e72ac4a0"
parent_commit = "2d433a9b43cfdabe4a76a29a4a352b6eb93be3a2"

nullpointer = "CWE-476"#CWE-476: NULL Pointer Dereference
nullpointer_bug_names = ["Dereference of null pointer","nullPointerRedundantCheck","Null Dereference","Called function pointer is null (null dereference)","nullPointer"]
deadstore = "CWE-563" #CWE-563: Assignment to Variable without Use
deadstore_bug_names = ["Dead Store", "Dead assignment", "uselessAssignmentArg", "unreadVariable", "redundantAssignment", "Dead initialization", "redundantInitialization"]
bug_dict = {all: {}, nullpointer: {}, deadstore: {}, "others":{}}
outputjson = "bug_funcs.json"
jsonfp = open(outputjson, "w")
jsonfp.truncate(0)

bug_func_dict = {}
all_func_dict = {}

func_piece = {
            "id": "",
            "cwe": "None",
            "product": product_name,
            "functions": [
                {
                    "file": "",
                    "name": "",
                    "line_range": [

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
        #func_dict[id] = func_piece


'''
CPP check report handle done! id =  1799
infer report handle done! id =  2244
CSA report handle done! id =  2529

'''

linenum = 1
id = 0
while linecache.getline(bug_func_file, linenum):
    line = linecache.getline(bug_func_file, linenum)
    #print(line)
    #notes.c;814; Uninitialized Value;init_notes;786;824
    words = line.split(";")
    words[5] = words[5].replace("\n", "")
    words[2] = words[2].replace("\n", "")
    if words[2][0] == ' ':
        words[2] = words[2][1:]
    #print(words[2])
    #if words[2] in nullpointer_bug_names:
    key = words[0]+";"+words[1]
    #print(key)
    #录入总bug
    func_piece["functions"][0]["file"] = words[0]
    func_piece["functions"][0]["name"] = words[3]
    func_piece["functions"][0]["line_range"] = [int(words[4]), int(words[5])]
    func_piece["functions"][0]["def_range"] = [int(words[1]), int(words[1])]
    if key in bug_dict[all]:
        bug_dict[all][key] += 1
    else:
        bug_dict[all][key] = 1

    if words[2] in nullpointer_bug_names:
        if key in bug_dict[nullpointer]:
            bug_dict[nullpointer][key] += 1
            if bug_dict[nullpointer][key] == 3:
                id += 1
                func_piece["id"] = id
                func_piece["cwe"] = nullpointer
                all_func_dict[id] = func_piece
        else:
            bug_dict[nullpointer][key] = 1
    elif words[2] in deadstore_bug_names:
        if key in bug_dict[deadstore]:
            bug_dict[deadstore][key] += 1
            if bug_dict[deadstore][key] == 3:
                id += 1
                func_piece["id"] = id
                func_piece["cwe"] = deadstore
                all_func_dict[id] = copy.deepcopy(func_piece)
        else:
            bug_dict[deadstore][key] = 1
    else:
        if key in bug_dict["others"]:
            bug_dict["others"][key] += 1
        else:
            bug_dict["others"][key] = 1

    linenum += 1

print("all bugs:")
for key in bug_dict[all]:
    if bug_dict[all][key] >= 3:
        print( key, bug_dict[all][key])

print("\n \n null pointer")
for key in bug_dict[nullpointer]:
    if bug_dict[nullpointer][key] >= 3:
        print( key, bug_dict[nullpointer][key])

print("\n \n dead store")
for key in bug_dict[deadstore]:
    if bug_dict[deadstore][key] >= 3:
        print( key, bug_dict[deadstore][key])

print("\n \n others")
for key in bug_dict["others"]:
    if bug_dict["others"][key] >= 3:
        print( key, bug_dict["others"][key])


json.dump(all_func_dict, jsonfp, indent=4, ensure_ascii=False)
#print (bug_dict)
jsonfp.close()