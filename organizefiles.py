import os
from shutil import move as shutilMove
import sys

record_file = "directory_list.txt"

class Organize():
    def __init__(self, folder, fileName):
        self.fileName = fileName
        if(folder[0] == '~'):
            self.folder= os.path.expanduser(folder)
        else:
            self.folder= os.path.join(os.getcwd(),folder)
        self.fullFileName = os.path.join(self.folder,fileName)
        self.dirName = ""
        self.fullDirName = ""
        self.text_file = os.path.join(self.folder, record_file)

    def dirExist(self):
        return os.path.isdir(self.fullDirName)

    def findExtDir(self):
        fileNickname, fileExt = os.path.splitext(self.fileName)
        ext = fileExt[1::]
        self.dirName = ext.upper() + 's'
        self.fullDirName = os.path.join(self.folder, self.dirName)
        
    def makeDir(self):
        os.mkdir(self.fullDirName)
        #print("making and the directory name is: "+self.fullDirName)

    def moveFile(self):
        os.rename(self.fullFileName, os.path.join(self.fullDirName, self.fileName))

    def moveDirectory(self):
        #print("moving and the directory name is: " +self.fullDirName)
        shutilMove(self.fullFileName, os.path.join(self.fullDirName, self.fileName))

    def checkDirRecordforSelf(self):
        with open(self.text_file) as f:
            for line in f:
                if line.strip() == self.fullFileName:
                    return True
        return False

    def dirRecordExist(self):
        if (os.path.exists(self.text_file) == True):
            return True
        else:
            return False
    
    def checkDirRecordforDir(self):
        with open(self.text_file) as f:
            for line in f:
                if line.strip() == self.fullDirName:
                    return True
        return False

    def addDirRecord(self):
        file = open(self.text_file, "a")
        file.write(self.fullDirName+"\n")
        file.close()

    def fullDoDir(self):
        if(self.dirRecordExist()==True):
            if (self.checkDirRecordforSelf() == True):
                return
        self.fullDirName = os.path.join(self.folder, "DIRECTORIES")
        if(self.dirExist() == False):
            self.makeDir()
        self.moveDirectory()
        if(self.dirRecordExist()==True):
            if (self.checkDirRecordforSelf() == True or self.checkDirRecordforDir()):
                return
        self.addDirRecord()
        return

    def fullDoFile(self):
        self.findExtDir()
        if(self.dirExist() == True):
            self.moveFile()
        else:
            self.makeDir()
            self.moveFile()
        if self.dirRecordExist() == True:
            if self.checkDirRecordforDir() == True:
                return
        self.addDirRecord()
        return

    def fullDo(self):
        if(os.path.isdir(self.fullFileName)==True):
            self.fullDoDir()
        else:
            if(self.fullFileName == self.text_file):
                return
            self.fullDoFile()

    def fullDoNoDir(self):
        if(os.path.isdir(self.fullFileName)==True):
            self.fullDirName= self.fullFileName
            self.addDirRecord()
        else:
            if(self.fullFileName == self.text_file):
                return
            self.fullDoFile()

def goThrough(folder, movedir):
    file_list = os.listdir(folder)
    if(movedir == True):
        for item in file_list:
            organize = Organize(folder, item)
            organize.fullDo()
    else:
        for item in file_list:
            organize = Organize(folder, item)
            organize.fullDoNoDir()
    return


def main():
    if (len(sys.argv) > 3):
        print("Too many arguments")
        return
    if (len(sys.argv) < 3):
        print("Too few arguments")
        return
    folder = sys.argv[1]
    if(folder[0] == '~'):
        dir = os.path.expanduser(folder)
    else:
        dir = folder
    if (os.path.exists(dir) == False):
        print("There does not exist a folder called " + dir)
        return
    if(sys.argv[2] == "keepdir"):
        goThrough(folder, False)
    elif(sys.argv[2] == "movedir"):
        goThrough(folder, True)
    else:
        print("Not eneough arguments")
    
    print("File organization complete")

main()
    
