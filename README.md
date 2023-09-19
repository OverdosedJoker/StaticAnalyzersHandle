# StaticAnalyzersHandle

## 工作流程
<img width="758" alt="流程图" src="https://github.com/OverdosedJoker/StaticAnalyzersHandle/assets/55365803/84a04cf7-7994-4165-8e5d-df73c5178419">


## RemoveComment.py
去除源码注释
## report_handle.py 
处理三个静态分析工具的报告，生成包含bug信息表的中间文件
## func_judge.py 
扫描去注释后的源码，提取出所有函数，生成函数信息表的中间文件
## unbuged_result.py 
分析中间文件输出无bug函数的json
<img width="968" alt="unbuged_func" src="https://github.com/OverdosedJoker/StaticAnalyzersHandle/assets/55365803/ca5b2373-6eac-4597-86c7-f76eb016a314">

## bug_vote_result.py 
分析中间文件输出有bug函数的json， 投票的bug可以继续自定义
<img width="661" alt="bug_dict" src="https://github.com/OverdosedJoker/StaticAnalyzersHandle/assets/55365803/ef181aa4-40f0-4fe9-81da-04705cdc9103">
<img width="965" alt="buged_func" src="https://github.com/OverdosedJoker/StaticAnalyzersHandle/assets/55365803/17d2dede-177e-4b8f-b95f-8307c2c825ba">


## 操作note
几个文件都需要指定文件路径

具体信息下班有空再补充
