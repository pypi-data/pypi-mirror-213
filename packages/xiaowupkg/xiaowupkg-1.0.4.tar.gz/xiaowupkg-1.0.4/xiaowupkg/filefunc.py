import os

def readfilename(path, filetype):     #获取ktr文件
    L=[]
    for root,dirs,files in os.walk(path):
        if root == path:
            for i in files:
                if os.path.splitext(i)[1] == filetype:
                    print(i)
                    L.append(i)
    return L

'''
功能：清除当前路径下所有的python缓存文件
'''
def cleanPycache(path):
    for root,dirs,file in os.walk(path):
        print(root)
        print(dirs)
        for dir in dirs:
            if dir == '__pycache__':
                os.system('rm -rf ' + root + os.sep + dir)
                print('clear finished:' + root + os.sep + dir)
        print('\n')