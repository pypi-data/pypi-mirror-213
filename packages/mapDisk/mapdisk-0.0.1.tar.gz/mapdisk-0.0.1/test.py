from src.mapDisk.mapDisk import MapD
import os
import time
from src.mapDisk.mapDisk import BLOCK_SIZE
import numpy as np
if __name__=="__main__":
    timeAdd=[]
    timeRead=[]
    timeDel=[]
    for n in [8000, 17000, 42000, 60000]:
        md = MapD("HashMapName.mpd",".")
        time_add=[]
        time_read=[]
        time_del=[]
        for i in range(n):
            print(i)
            t1=time.time()
            x=md.add(str(i),i)
            t= time.time()-t1
            time_add.append(t)
            print(len(x),"test length")
            if str(i) not in x:
                print("Failed at, ",i)
                raise "Addition Failed"
        for i in range(n):
            t1=time.time()
            x=md.read(str(i))
            t=time.time()-t1
            time_read.append(t)
            if str(i) not in x:
                raise "Retrival Failed"
        for i in range(int(n*5/8),n):
            t1=time.time()
            md.delete(str(i))
            t=time.time()-t1
            time_del.append(t)
        for i in range(int(n*5/8),n):
            t1=time.time()
            x=md.read(str(i))
            t=time.time()-t1
            time_read.append(t)
            if x!=None:
                raise "Delete Failed"
        for i in range(int(n*5/8),n):
            t1=time.time()
            x=md.add(str(i),i+1000)
            t= time.time()-t1
            time_add.append(t)
            if str(i+1000) not in x:
                print("Failed at, ",i)
                raise "Addition Failed"
        print("size before shrink ", os.path.getsize(md.filePath)/BLOCK_SIZE)
        md.shrink()
        print("size after shrink", os.path.getsize(md.filePath)/BLOCK_SIZE)
        md.close()
        time_add=np.array(time_add)
        time_del=np.array(time_del)
        time_read=np.array(time_read)
        timeAdd.append(time_add.mean())
        timeRead.append(time_read.mean())
        timeDel.append(time_del.mean())
        print(f"time complexities add:{time_add.mean()} ,read:{time_read.mean()} ,del:{time_del.mean()}")
        os.system("rm HashMapName.mpd")
    print("add: ", timeAdd)
    print("read: ", timeRead)
    print("Del: ", timeDel)