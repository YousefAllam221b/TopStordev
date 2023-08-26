#!/usr/bin/python3
import sys, pandas as pd
from etcdget import etcdget as get 

def getUsersInfo(allInfo):
    collectedUsers = {}

    for value in allInfo:
        code = value[0].split("/")[0]
        name = value[0].split("/")[1]
        info = value[1]
        if (code != "usersinfo" and code != "usershash" and code != "usersigroup"):
            continue
        if (code == "usershash"):
            if (name not in collectedUsers):
                collectedUsers[name] = {}
            collectedUsers[name]["name"] = name
            collectedUsers[name]["password"] = info
        elif (code == "usersinfo"):
            if (name not in collectedUsers):
                collectedUsers[name] = {}
            collectedUsers[name]["userid"] = info.split("/", 4)[0].split(":")[0]
            collectedUsers[name]["usergd"] = info.split("/", 4)[0].split(":")[1]
            collectedUsers[name]["pool"] = info.split("/", 4)[1]
            collectedUsers[name]["size"] = info.split("/", 4)[3]
            collectedUsers[name]["permissions"] = info.split("/",4)[-1]
        elif (code == "usersigroup"):
            usersInGroup = info.split("/", 4)[2].split(",")
            for user in usersInGroup:
                if (user == "NoUser"):
                        continue
                if (user not in collectedUsers):
                    collectedUsers[user] = {"groups": name}
                else:
                    if ("groups" in collectedUsers[user].keys()):
                        collectedUsers[user]["groups"] = collectedUsers[user]["groups"] + "," + name
                    else:
                        collectedUsers[user]["groups"] = name
    return collectedUsers

def createFile(leaderip):
    allInfo = get(leaderip, "users", "--prefix")
    allUsers = getUsersInfo(allInfo) 

    columns = ["name", "password", "userid", "usergd", "pool", "size", "permissions"]
    usersList = [{col: user.get(col, '') for col in columns} for user in allUsers.values()]

    df = pd.DataFrame(usersList)
    df.to_excel("/TopStor/TopStordata/allUsers.xlsx", index=False)


if __name__=='__main__':
    createFile(*sys.argv[1:])