import os

def createDir(name):
    if os.path.exists(name):
        print("createDir error at name:"+name)
    else:
        os.makedirs(name)
def createFile(name):
    if not os.path.exists(name):
        with open(name, 'w') as f:
            f.write('')
    else:
        pass

def file2list(name):
    res=[]
    with open(name,'r') as f:
        for line in f:
            res.append(line,replace('\n',''))
    return res

def list2file(name,lis):
    with open(name,'w') as f:
        for iterm in lis:
            f.write(iterm+'\n')