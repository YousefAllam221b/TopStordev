#!/usr/bin/python3
import subprocess,sys,socket
import json
from ast import literal_eval as mtuple
from etcdgetpy import etcdget as get
from etcdgetlocalpy import etcdget as getlocal
from etcdput import etcdput as put
from etcddel import etcddel as dels 
import logmsg
disksvalue=[]
leaderip = getlocal('leaderip')[0]
def delall(*args):
 global leaderip
 if len(args) > 1:
  dels(leaderip, args[1]+'/lists/'+args[0])
 else:
  dels(leaderip, 'lists/'+args[0])

def getall(*args):
 global leaderip
 if len(args) > 1:
  alls=get(leaderip, args[1]+'/lists/'+args[0])
 else:
  alls=get(leaderip, 'lists/'+args[0])
 if len(alls) > 0 and alls[0] != -1:
  alls=mtuple(alls[0])
  return alls
 else:
  return [-1]

def putall(*args):
 global leaderip
 alls=getall(args[0])
 put(leaderip, args[1]+'/lists/'+args[0],json.dumps(alls))

def norm(val):
 units={'B':1/1024**2,'K':1/1024, 'M': 1, 'G':1024 , 'T': 1024**2 }
 if type(val)==float:
  return val
 if val[-1] != 'B':
  return float(val) 
 else:
  if val[-2] in list(units.keys()):
   return float(val[:-2])*float(units[val[-2]])
  else:
   return float(val[:-1])*float(units['B'])

if __name__=='__main__':
 getall(*sys.argv[1:])
