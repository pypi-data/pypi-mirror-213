"""An amazing flit templates package!"""
__version__ = "0.1"

import argparse
import re
import os

input_file = ''
project=''

def cAPtree():
    global input_file
    parser = argparse.ArgumentParser(prog='mkfstree')
    parser.add_argument('-v','--name', help='Nome do ficheiro',required=True)
    args = parser.parse_args()
    input_file = args.name

def readF(input_file):
    with open(input_file,'r+') as f:
        text = f.read()
        f.close()
    return text

def rmEmptyLines(txt):
    return re.sub(r'\n(\s*\n)+', '\n', txt)

def meta(txt):
    txt = [t.strip() for t in txt]
    d = {}
    for t in txt:
        kv = t.split(':',1)
        v = kv[1].split('//')[0].strip()
        d[kv[0]] = v
    return d

def tree(txt):
    global project
    if not os.path.exists(project):
        os.mkdir(project)
    os.chdir(project)
    os.system('rm -rf *')
    dir = ''
    txt = [t.strip() for t in txt]
    tre = []
    for t in txt:
        if t.startswith('-'):
            t = t[1:].strip()
            if t.endswith('/'):
                os.mkdir(dir+t)
                dir = dir+t
            else:
                os.mknod(dir+t)
                tre.append(dir+t)
        elif t.endswith('/'):
            os.mkdir(t)
            dir = t
        else:
            os.mknod(t)
            tre.append(t)
    return tre

def ficheiro(nome,conteudo):
    with open(nome,'w+') as f:
        f.write('\n'.join(conteudo))
        f.close()

def subVars(d,txt):
    for k,v in d.items():
        txt = txt.replace(r'{{'+k+r'}}',v)
    ts = txt.split('===')[1:]
    ts = [t.split('\n') for t in ts]
    for i in range(0,len(ts)):
        ts[i][0] = ts[i][0].strip()
        if ts[i][0]=='meta':
            ts.pop(i)
            break
    txt = '==='+'\n=== '.join(['\n'.join(t) for t in ts])
    return txt

def mkfstreeA(txt):
    global project, input_file
    mF = False
    if txt == '':
        txt = readF(input_file)
    else:
        mF = True
    ts = txt.split('===')[1:]
    ts = [t.split('\n') for t in ts]
    tre = []
    files = {}
    tF = False
    for t in ts:
        t[0] = t[0].strip()
        if re.match(r'^\s*$',t[0]):
            pass
        elif t[0] == 'meta':
            mF = True
            t = rmEmptyLines('\n'.join(t)).strip().split('\n')
            d = meta(t[1:])
            if 'name' in d:
                project = d['name']
            else:
                # ask for project name
                project = input('Nome do projecto: ')
                d['name'] = project
            t2 = subVars(d,txt)
            mkfstreeA(t2)
            return
        elif t[0] == 'tree':
            if mF:
                t = rmEmptyLines('\n'.join(t)).strip().split('\n')
                tre = tree(t[1:])
                tF = False
            else:
                tF = True
                tre = rmEmptyLines('\n'.join(t)).strip().split('\n')
        else:
            files[t[0]] = t[1:]
    if tF:
        tre = tree(tre[1:])
    for k,v in files.items():
        tre2 = [e for e in tre if e.endswith(k)]
        if len(tre2) == 0:
            ficheiro(k,v)
        else:
            for e in tre2:
                ficheiro(e,v)
    
def mkfstree():
    cAPtree()
    mkfstreeA('')

######################################
fo = ''

def cAPtemplate():
    global input_file, fo
    parser = argparse.ArgumentParser(prog='mktemplateskel')
    parser.add_argument('-v','--name', help='Nome do projecto',required=True)
    parser.add_argument('-f','--file', help='Nome do template')
    args = parser.parse_args()
    input_file = args.name
    if args.file:
        fo = args.file

def getToDir(project):
    os.chdir(project)

def handleFiles(files):
    d = {}
    for f in files:
        if f in 'directory':
            getToDir(f)
            files2 = os.listdir()
            d.update(handleFiles(files2))
            getToDir('..')
        else:
            d[f] = readF(f)
    return d

def getDirFile(line):
    # regex to match a name of a directory
    expD = r'^(.+\/)?([^\/]+)?$'
    m = re.match(expD,line)
    if m:
        dir = m.group(1) if m.group(1) else ''
        file = m.group(2) if m.group(2) else ''
    return dir,file

def getAuthors(txt):
    txt = txt.replace(' ','')
    content = r'\[(.*?)\]'
    obj = r'\{(.*?)\}'
    atr = r'(\w+)=\"(\w+)\"'
    c = re.search(content,txt).group(1)
    o = re.finditer(obj,txt)
    d = {}
    i=0
    t2 = '['
    for t in o:
        t2 += '{'
        i2 = 0
        atrs = re.finditer(atr,t.group(1))
        for a in atrs:
            if i2 > 0:
                t2 += ','
            d[a.group(1)+'_'+str(i)] = a.group(2)
            t2 += a.group(1)+' = "{{'+a.group(1)+'_'+str(i)+'}}"'
            i2+=1
        i+=1
        t2 += '}'
    t2 += ']'
    d['authors'] = t2
    return d

def getNameAuthor(txt):
    txt = txt.split('\n')
    t2 = ''
    d = {}
    for t in txt:
        kv = t.split('=',1)
        if kv[0].strip() == 'name':
            if len(kv) >1:
                d['name'] = kv[1].replace('"','').strip()
                t2 += 'name = "'+d['name']+'"\n'
        elif kv[0].strip() == 'authors':
            if len(kv) >1:
                t2 += 'authors = '
                aD = getAuthors(kv[1])
                t2 += aD['authors']+'\n'
                for k,v in aD.items():
                    if k != 'authors':
                        d[k] = v
        else:
            t2 += t+'\n'
    d['[project]'] = t2
    return d

def getMeta(txt):
    txt = '\n'+txt
    txt = re.split(r'\n(?:\[)',txt)[1:]
    t2 = ''
    d = {}
    metaTxt = ''
    for t in txt:
        title = t.split(']',1)
        if title[0] == 'project':
            d = getNameAuthor(title[1])
            title[1] = d['[project]']
        t2 += '\n['+title[0]+']'+title[1]
    for k,v in d.items():
        if k != '[project]':
            metaTxt += k+': '+v+'\n'
    d2 = {}
    d2['meta']=metaTxt
    d2['project']=t2
    d2['vars']=d
    return d2

def getTreeAndFiles():
    di = {}
    tree = ''
    for root, dirs, files in os.walk(".", topdown=False):
        for d in dirs:
            tree += os.path.join(root, d)+'/\n'
        for f in files:
            tree += os.path.join(root, f)+'\n'
    # ordena a arvore
    tree ='\n'.join(sorted(tree.split('\n'))[1:])
    # remove o ./ do inicio de cada linha
    tree = re.sub(r'(^|\n)\./',r'\1',tree)
    t2 = ''
    prev_dir = ''
    for line in tree.split('\n'):
        dir,file = getDirFile(line)
        if file == '' and dir != '':
            if dir != prev_dir:
                t2 += dir+'\n'
                prev_dir = dir
        elif file != '':
            if dir != '':
                if dir == prev_dir:
                    t2 += '\t-'+file+'\n'
            else:
                t2 += file+'\n'
            fn = ''+dir+file
            di[file] = readF(fn)
            if file == 'pyproject.toml':
                d2 = getMeta(di[file])
                di['meta'] = d2['meta']
                di[file]=d2['project']
                di['[vars]']=d2['vars']
    di['tree'] = t2
    return di

def mktemplateskel():
    global project, fo, input_file
    cAPtemplate()
    project = input_file
    getToDir(project)
    d = {}
    d=getTreeAndFiles()
    txt= ''
    used = []
    for k,v in d.items():
        if k not in used and k != '[vars]' and k != 'meta':
            used.append(k)
            txt += '=== '+k+'\n'+v+'\n'
    d2 = d['[vars]']
    for k,v in d2.items():
        txt = re.sub(v,r'{{'+k+r'}}',txt)
    os.chdir('..')
    if fo == '':
        print('=== meta\n'+d['meta']+'\n')
        print(txt)
    else:
        with open(fo,'w+') as f:
            f.write('=== meta\n'+d['meta']+'\n')
            f.write(txt)
            f.close()
    

    #files = os.listdir()
    #print(files)
    #d.update(handleFiles(files))
    #d = {'meta':'','tree':''}


#mkfstree() # python3 template.py -v exemplo.txt
#mktemplateskel() # python3 template.py -v yakari144 -f output.txt

