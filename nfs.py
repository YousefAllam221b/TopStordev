#!/usr/bin/python3
import sys, subprocess, datetime
from logqueue import queuethis, initqueue
from etcdgetpy import etcdget as get
from sendhost import sendhost

def create(leader, leaderip, myhost, myhostip, etcdip, pool, name, ipaddr, ipsubnet, vtype,*args):
    volsip = get(etcdip,'volume',ipaddr)
    volsip = [ x for x in volsip if 'active' in str(x) ]
    nodesip = get(etcdip, 'Active',ipaddr) 
    notsametype = [ x for x in volsip if vtype not in str(x) ]
    if (len(nodesip) > 0 and 'Active' in str(nodesip))or len(notsametype) > 0:
        print(ipaddr)
        print(len(nodesip), nodesip)
        print(len(notsametype), notsametype)
        print(' the ip address is in use ')
        return
    cmdline='rm -rf /TopStordata/tempnfs.'+ipaddr
    subprocess.run(cmdline.split(),stdout=subprocess.PIPE)  
    mounts =''
    if len(volsip) < 1 :
        return
    who = volsip[0][1].split('/')[2]
    exports = ''
    for vol in volsip:
        if vol in notsametype:
           continue
        exp = '/'+vol[0].split('/')[3]+'/'+vol[0].split('/')[4]
        exports = exp +' '+ who+'('+','.join(vol[1].split('/')[3:8])+')\n'
        with open('/TopStordata/exportip.'+vol[0].split('/')[4]+'_'+ipaddr,'w') as fip:
            fip.write(exports)
    
    cmdline = '/TopStor/nfs.sh '+ipaddr+' '+ipsubnet
    subprocess.run(cmdline.split(),stdout=subprocess.PIPE)  

    return
    #if len(checkipaddr1) != 0 or len :

 

if __name__=='__main__':
 leader = sys.argv[1]
 leaderip = sys.argv[2]
 myhost = sys.argv[3]
 myhostip = sys.argv[4]
 etcdip = sys.argv[5]
 pool = sys.argv[6]
 name = sys.argv[7]
 ipaddr = sys.argv[8]
 ipsubnet = sys.argv[9]
 vtype = sys.argv[10]
 initqueue(leaderip, myhost)
 with open('/root/cifspytmp','w') as f:
  f.write(str(sys.argv))
 create(leader, leaderip, myhost, myhostip, etcdip, pool, name, ipaddr, ipsubnet, vtype,*sys.argv[11:])
