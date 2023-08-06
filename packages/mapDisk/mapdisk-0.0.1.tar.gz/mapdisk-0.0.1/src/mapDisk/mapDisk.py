import os
# import mmap
BLOCK_SIZE = 4096
class MapD:
    def __init__(self,name="test.mpd",path="."):
        self.file = None
        self.filePath = os.path.join(path,name)
        if os.path.exists(os.path.join(path,name)):
            self.file = open(os.path.join(path,name),"r+")
            #self.file.write(0)
            return
        os.makedirs(os.path.basename(path),exist_ok=True)
        self.file = open(self.filePath,"w+")
        self.file.write("0")
        self.file.flush()
        return
    
    def add(self,key,value=None):
        if(not key):
            raise "Please Provide Key"
        key=str(key)
        hashID=MapD.hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return MapD.vtp(self.file, maxID, hashID, len(key), isWrite=True, data=value)
    
    def read(self,key):
        if(not key):
            raise "Please Provide Key"
        key=str(key)
        hashID=MapD.hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return MapD.vtp(self.file, maxID, hashID, len(key))

    def delete(self, key):
        if(not key):
            raise "Please Provide Key"
        key=str(key)
        hashID=MapD.hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return MapD.vtp(self.file, maxID, hashID, len(key), isWrite=False, delete=True)
        
    def close(self):
        self.file.close()
        #self.__del__()

    def shrink(self):
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return MapD.vtp(self.file, maxID, None, isWrite=False, delete=True, shrink=True, path=self.filePath)
    """def seekTo(self,key):
        self.file.seek(0)
        for i in range(len(key)):
            reqGroup = key[0:i]
            group = ""
            groupEndPos = 0
            while (group != reqGroup and group in reqGroup):
                self.file.seek(offset,1)
                groupEndPos=self.file.tell()
                self.file.seek(1,1)
                char = ""
                group = ""
                while(char!=","):
                    group+=char
                    char = self.file.read(1)
                offset = 0
                char = ""
                while(char!=","):
                    offset+=char
                    char = self.file.read(1)
                offset = int(offset)
            if(group!=reqGroup){
                self.file.seek(groupEndPos)
                self.addGroup(reqGroup)
            }
    """
    @staticmethod

    def hash(key):
        hashID = 0
        for char in key:
            hashID+=12000*hashID+ord(char)
        return hashID+1321
            
    def vtp(fd, maxID, hashID=None, keylen=1, isWrite=False, data=0, delete=False, shrink = False, path=None, blockSize=BLOCK_SIZE):
        mod = 3001
        inc = 803
        inc_change = 1.1
        phyAdr=0
        if hashID!=None:
            #mod = (hashID%(10**keylen))+1
            phyAdr = hashID%(mod)
            inc=503
            #phyAdr = hashID%mod
        #blockSize = BLOCK_SIZE
        maxID=int(maxID)
        if(isWrite and hashID!=None):
            #mm = mmap.mmap(fd.fileno(),0,prot=mmap.ACCESS_WRITE)
            fd.seek(phyAdr*blockSize)
            while(fd.read(2)=="1d"):#(mm[blockSize*phyAdr:blockSize*phyAdr+2].decode("utf-8")=="1d"):
                fd.seek(phyAdr*blockSize+2)
                if str(hashID) == fd.read(len(str(hashID))):
                    break  
                mod+=inc
                inc=int(inc*inc_change)
                phyAdr = hashID%mod #if (hashID>mod or not mm[blockSize*(hashID%mod):blockSize*(hashID%mod)+2]=="1d") else mod+1
                hashID+=mod-inc
                if phyAdr>maxID-1:
                    #end = (mod if (mod>phyAdr) else (phyAdr+1))
                    end = phyAdr
                    fd.seek(blockSize*maxID)
                    for i in range(maxID,end):
                        fd.seek(blockSize*i)
                        fd.write("0e")
                    fd.seek(blockSize*end)
                    fd.write("0e")
                    fd.seek(blockSize*end+blockSize-2)
                    fd.write("0")
                    fd.flush()
                    #mm.close()
                    #mm = mmap.mmap(fd.fileno(),0,prot=mmap.ACCESS_WRITE)
                    maxID = end+1
                fd.seek(phyAdr*blockSize)
            try:
                fd.seek(blockSize*phyAdr)
                fd.write("1d")
                fd.seek(blockSize*phyAdr+2)
                fd.write((blockSize-2)*"\0")
                fd.seek(blockSize*phyAdr+2)
                fd.write(str(hashID))
                fd.write(str(data))
                fd.flush()
            except:
                return None
            fd.seek(blockSize*phyAdr+2+len(str(hashID)))
            dataWritten = fd.read(blockSize-2-len(str(hashID)))
            #mm.close()
            return dataWritten.rstrip("\x00")
        elif(hashID!=None):
            #mm = mmap.mmap(fd.fileno(),0,prot=mmap.ACCESS_READ)
            while(True):
                fd.seek(phyAdr*blockSize)
                if (fd.read(2)=="1d" and str(hashID) == fd.read(len(str(hashID)))):
                    if(delete):
                        try:
                            fd.seek(blockSize*phyAdr)
                            fd.write("0e")
                            fd.flush()
                            continue
                            #mm.close()
                            return True
                        except:
                            #mm.close()
                            return None

                    fd.seek(blockSize*phyAdr+2+len(str(hashID)))
                    dataRead = fd.read(blockSize-2-len(str(hashID)))
                    #mm.close()
                    return dataRead.rstrip("\x00")
                mod+=inc
                inc=int(inc*inc_change)
                phyAdr = hashID%mod #if (hashID>mod) else mod+1
                hashID+=mod-inc
                if phyAdr>maxID-1:
                    #mm.close()
                    return None
            return None
        elif(shrink):
            if (not path):
                return None
            #mm = mmap.mmap(fd.fileno(),0,prot=mmap.ACCESS_READ)
            fd.seek(blockSize*(maxID-1))
            while(fd.read(2)!="1d"):#mm[blockSize*(maxID-1):blockSize*(maxID-1)+2].decode("utf-8")!="1d"):
                try:
                    os.truncate(path, (maxID-1)*blockSize)
                    maxID-=1
                except OSError as error:
                    #mm.close()
                    return None
                if maxID>1:
                    fd.seek((maxID-1)*blockSize)
                else:
                    break
                fd.seek(blockSize*(maxID-1))
            #mm.close()
            return True
            
        
