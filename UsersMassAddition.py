import subprocess

# Replacement for etcdgetjson
def cleaner(result):
    mylist=str(result.stdout.decode()).replace('\n\n','\n').split('\n')
    mylist=zip(mylist[0::2],mylist[1::2])
    hostid=0
    hosts=[]
    for x in mylist:
        ll=[]
        xx=x[1]
        ll.append(xx)
        hostsdic={'id':str(hostid),'name':x[0],'prop':xx}
        hostid=hostid+1
        hosts.append(hostsdic)
    return hosts

def poolsCleaner(result):
    z=[]
    mylist=str(result.stdout.decode()).replace('\n\n','\n').split('\n')
    zipped=zip(mylist[0::2],mylist[1::2])
    for x in zipped:
        z.append(x) 
    return z

def getusers():
    cmdline = ['docker', 'exec', 'etcdclient', 'etcdctl', '--endpoints=http://etcd:2379', 'get', 'usersinfo', '--prefix']
    userlst = cleaner(subprocess.run(cmdline,stdout=subprocess.PIPE))
    uid = 0
    users = []
    for user in userlst:
        username = user['name'].replace('usersinfo/','')
        users.append([username,str(uid)]) 
        uid += 1
    return users

def getgroups():
    cmdline = ['docker', 'exec', 'etcdclient', 'etcdctl', '--endpoints=http://etcd:2379', 'get', 'usersigroup', '--prefix']
    groupslst = cleaner(subprocess.run(cmdline,stdout=subprocess.PIPE))
    gid = 0
    groups = []
    for group in groupslst:
        grpusers = group['prop'].split('/')[2]
        groupname = group['name'].replace('usersigroup/','')
        groups.append([groupname,str(gid), grpusers]) 
        gid += 1
    return groups

def getpools():
    cmdline=['docker', 'exec', 'etcdclient', 'etcdctl', '--endpoints=http://etcd:2379', 'get', 'pools/', '--prefix']
    pools= poolsCleaner(subprocess.run(cmdline,stdout=subprocess.PIPE))
    poolinfo = []
    pooldict = dict()
    pid = 0
    for pool in pools:
        poolinfo.append({'id':pid, 'owner': pool[1], 'text':pool[0].split('/')[1]})
        pid += 1
        pooldict[pool[0].split('/')[1]] = {'id': pid, 'owner': pool[1] }
    return poolinfo
print(getusers())
print('#############')
print(getgroups())
print('#############')
print(getpools())
