class Task:
    def extractDate(self, line):
        re = __import__('re')
        pattern = re.search(r'\b\d{2}[/]\d{2}[/]\d{4}\b', line)

        start = pattern.span()[0]
        stop = pattern.span()[1]
        date = line[start:stop]
        return date

    def extractSubject(self, line):
        re = __import__('re')
        pattern = re.search(r'\b[a-zA-z]{2}\d{4}\b', line)

        start = pattern.span()[0]
        stop = pattern.span()[1]
        subject = line[start:stop]

        return subject

    def extractType(self, words, line):
        re = __import__('re')
        
        pattern=""
        for w in words:
            pattern = re.search(w, line, re.IGNORECASE)
            if pattern != None:
                break
        
        start = pattern.span()[0]
        stop = pattern.span()[1]
        tipe = line[start:stop]

        return tipe

    def extractTopic(self, line):
        return ""

    def __init__(self, line, Status):
        self.id= len(Status.taskList) + 1
        self.date= self.extractDate(line)
        self.subject= self.extractSubject(line)
        self.type= self.extractType(Status.words, line)
        self.topic= self.extractTopic(line)
    


class Status:
    def __init__(self):
        self.words = ["Tucil", "Tubes", "Tugas", "PR", "Kuis", "Quiz", "Milestone"]
        self.taskList = []
        self.deadline = ["undur", "majuin"]

    def addTask(self, Task):
        self.taskList.append(Task)

    def printAllTask(self):
        for Task in self.taskList:
            print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type)
    
    def findID(self,line):
        re = __import__('re')
        pattern = re.search("task \d+", line, re.IGNORECASE)
        start = pattern.span()[0]
        stop = pattern.span()[1]
        string = line[start:stop]
        angka = re.findall("\d", string)
        id = 0
        satuan = 10**(len(angka)-1)
        for i in range (len(angka)):
            id += int(angka[i])*satuan
            satuan/10
        return id
    
    def isUpdate(self, line):
        re = __import__('re')
        for w in self.deadline: 
            found = re.findall(w, line, re.IGNORECASE)
            if (found):
                return True
        return False
    
    def updateTask(self, line, id_):
        if (self.isIDValid(id_)):
            new_date = self.taskList[id_-1].extractDate(line)
            self.taskList[id_-1].date = new_date
            print("Deadline Task " + str(id_) + " berhasil di-update")
        else:
            print("ID tidak valid")

    def isIDValid(self, id_):
        if (id_>0) and (id_-1 < len(self.taskList)):
            return True
        return False


S = Status()
def toString(arr):
    list_string = []
    for angka in arr:
        list_string.append(str(angka))
    return list_string
print(toString([100,56,85,2711,9]))
while(input!=0):
    line = input()
    if (S.isUpdate(line)):
        idx = S.findID(line)
        S.updateTask(line, idx)
    else:
        T = Task(line, S)
        S.addTask(T)
    S.printAllTask()

def toString(arr):
    list_string = []
    for angka in arr:
        list_string.append(str(angka))
    return list_string
