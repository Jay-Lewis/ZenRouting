__author__ = 'Justin'

from math import ceil

tuple = ['1',[[1,2,3,4],[1,1,1,1],[2,2,2,2]]]
paths = tuple[1]

finalpaths = []
for path in paths:
    if(not(path in finalpaths)):
        finalpaths.append(path)

paths = finalpaths
print(paths)

finalpaths = []
for path in paths:
    for j in range(0,paths.index(path)):
        samenodes = 0
        for element in path:
            if(element in paths[j]):
                samenodes +=1
        if(samenodes < ceil(len(path)/2)):
            finalpaths.append(path)
            break
print(finalpaths)
paths = finalpaths



# paths = finalpaths
# for path in paths:
#     print('PATH',path)
#     print('RANGE',range(0,paths.index(path)))
#     for j in range(0,paths.index(path)):
#         print('PATH compare',paths[j])
#         samenodes = 0
#         for element in path:
#             if(element in paths[j]):
#                 samenodes +=1
#         if(samenodes >= ceil(len(path)/2)):
#             paths.remove(path)
#             print('REMOVED',path)
#             break

print('LENGTH AFTER',len(paths))
print('PATHS AFTER',paths)