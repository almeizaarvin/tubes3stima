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

    def addTask(self, Task):
        self.taskList.append(Task)

    def printAllTask(self):
        for Task in self.taskList:
            print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type)


S = Status()

while(input!=0):
    line = input()
    T = Task(line, S)
    S.addTask(T)
    S.printAllTask()