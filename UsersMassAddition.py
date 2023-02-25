import subprocess, pandas as pd
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

# Replacement for etcdget
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

def checker(user, usersNames, poolNames, groupNames):
    flag = False
    if (user['name'] in usersNames or  pd.isnull(user['name']) or user['name'] == ''):
        flag = True
    if ( pd.isnull(user['Password']) or len(user['Password']) < 3):
        flag = True
    # Checks if the user selected a Pool.
    if (not (user['Volpool'] == pd.isnull(user['Volpool']) or user['Volpool'] == '')):
        # Checks that the Pool is valid.
        if (not (user['Volpool'] in poolNames)):
            flag = True
    
    # Checks if the user selected a group.
    if (not (pd.isnull(user['groups']) or user['groups'] == '')):
        # Checks that each group selected is valid.
        print(not pd.isnull(user['groups']))
        for group in user['groups'].split(','): 
            if (not (group in groupNames)):
                flag = True
        print('nonono')
        
    # Checks if the user selected a HomeAddress.
    if (not(pd.isnull(user['HomeAddress']) or user['HomeAddress'] == '')):
        # Checks if the HomeAddress is in the correct form.
        if (len(user['HomeAddress'].split('.')) == 4):
            # Checks that each number is valid.
            for number in user['HomeAddress'].split('.'):
                if (int(number) > 255 or int(number) < 0):
                    flag = True
        else:
            flag = True
    return flag

def excelParser():
    df = pd.read_excel('Sample.xlsx', dtype = str)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    usersNames = getusers()
    groupNames = getgroups()
    poolNames = getpools()
    goodUsers = []
    badUsers = []
    for index, user in df.iterrows():
        flag = checker(user, usersNames, poolNames, groupNames)
        if flag:
            badUsers.append(user)
        else:
            goodUsers.append(user)
    print(goodUsers)
    print('############################')
    print(badUsers)
excelParser()