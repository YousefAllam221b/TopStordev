import sys, docker, time, json, subprocess
from etcdgetlocalpy import etcdget  as get
from etcdput import etcdput as put

client = docker.from_env()
cifsWGsIDs = client.containers.list(all=True, filters={"name":"CIFS-"})
#cifsWGsNames = [container.name for container in cifsWGsIDs]


for WG in cifsWGsIDs:
    container = client.containers.get(WG.id)
    #status = container.stats(decode=None, stream = False)
    #print(str(status["memory_stats"]["usage"]) + " " + str(status["memory_stats"]["limit"]))
    #print(status)
    #print(status["name"] + " " + status['cpu_stats'])
#print(cifsWGsNames)

def sizeof_fmt(num, isByteUnits = False, suffix="B"):
    ibyteUnits = ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi")
    byteUnits = ("", "K", "M", "G", "T", "P", "E", "Z")
    units = ibyteUnits
    conversion = 1024.0
    if isByteUnits:
        units = byteUnits
        conversion = 1000.0
    for unit in units:
        if abs(num) < conversion:
            return f"{num:3.1f}{unit}{suffix}"
        num /= conversion
    return f"{num:.1f}Yi{suffix}"

def dockerLog(leaderip):
    cifsWGsIDs = client.containers.list(all=True, filters={"name":"CIFS-"})
    try:
            containers = cifsWGsIDs
            for container in containers:
                status = container.stats(decode=None, stream = False)
                try:
                    # Calculate the change for the cpu usage of the container in between readings
                    # Taking in to account the amount of cores the CPU has
                    cpuDelta = status["cpu_stats"]["cpu_usage"]["total_usage"] - status["precpu_stats"]["cpu_usage"]["total_usage"]
                    systemDelta = status["cpu_stats"]["system_cpu_usage"] - status["precpu_stats"]["system_cpu_usage"]
                    #print("systemDelta: "+str(systemDelta)+" cpuDelta: "+str(cpuDelta))
                    cpuPercent = (cpuDelta / systemDelta) * (status["cpu_stats"]["online_cpus"]) * 100
                    cpuPercentRounded = round(cpuPercent,2)
                    cpuPercent = int(cpuPercent)
                    #Fetch the memory consumption for the container
                    mem = status["memory_stats"]["usage"]
                    mem = int(mem/1000000)
                    # Fetch Network I/O
                   # interfacesCount = 0
                    rx = 0
                    tx = 0 
                    for interface in status["networks"].keys():
                        rx += status["networks"][interface]["rx_bytes"]
                        tx += status["networks"][interface]["tx_bytes"]
                        #interfacesCount += 1
                    read = 0
                    write = 0
                    for service in status["blkio_stats"]["io_service_bytes_recursive"]:
                        if service["op"] == "read":
                            read += service["value"]
                        else:
                            write += service["value"]
                            
                    containerStats = {"volname": status["name"][1:],"mem":mem,"cpu":cpuPercentRounded, "networkInput": rx, "networkOutput": tx, "diskRead": read, "diskWrite": write}
                    put(leaderip, "statsvol/" + containerStats["volname"], json.dumps(containerStats))
                except Exception as e:
                    break
    except Exception as e:
            print("Error: "+str(e))
            pass
if __name__=='__main__':
    leaderip = sys.argv[1]
    #cmdline = 'docker exec etcdclient /TopStor/etcdgetlocal.py leaderip'
    #leaderip = subprocess.run(cmdline.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '').replace(' ', '')
    dockerLog(leaderip)
