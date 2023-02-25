import subprocess

cmdline=['docker', 'exec', 'etcdclient', 'etcdctl', '--endpoints=http://etcd:2379', 'get', 'usersigroup', '--prefix']
result=subprocess.run(cmdline,stdout=subprocess.PIPE)
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
print(cleaner(result))