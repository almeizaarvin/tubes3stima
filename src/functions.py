global types
types = ["Tucil", "Tubes", "Tugas", "PR", "Kuis", "Quiz", "Milestone"]

global taskList
taskList = []

global deadline
deadline = ["Undur", "Maju"]

global finishkeywords
finishkeywords = ["Sudah", "Selesai", "Selesai", "Done", "Finished", "Kelar", "Beres"]

global helpkeywords
helpkeywords = ["Bisa", "Apa", "Asisten", "Assistant", "Help"]

##============================FUNGSI ALGORITMA BOYERMOORE=======================
def lastOcc(arr, c):
    n = len(arr) - 1 #pengecekan dari paling belakang
    while(n != 0):
        if(arr[n] != c):
            n -= 1
        else:
            return n
    return -1


def boyerMoore(line, pattern):
    if(len(pattern) > len(line)):
        return -1
    else:
        n = len(line)
        m = len(pattern)
        i = j = m - 1
        while(i != n):
            if line[i].lower() == pattern[j].lower():
                if j == 0:
                    return i
                else:
                    i -= 1
                    j -= 1
            else:
                c = line[i]
                l = lastOcc(line, c)
                i = i + m - min(j, 1+l)
                j = m - 1 

        return -1





##==========================KELAS DAN FUNGSI TASK==================================
class Task:
    def __init__(self, types, line):
        self.id= len(taskList) + 1
        self.date= extractDate(line)
        self.subject= extractSubject(line)
        self.type= extractType(types, line)
        self.topic= extractTopic(line)
        self.status="Unfinished"

def isTask(types, line):
    if(extractDate(line)!=None and extractSubject(line)!=None and extractType(types, line)!=None):
        return True
    else:
        return False

def addTask(Task):
    taskList.append(Task)

def printAllTask():
    for Task in taskList:
        print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.status)

def extractDate(line):
    re = __import__('re')
    pattern = re.findall(r'\b\d{2}[/]\d{2}[/]\d{4}\b', line)

    if(len(pattern)==1):
        return pattern[0]
    elif(len([pattern])>1):
        return pattern

def extractSubject(line):
    re = __import__('re')
    pattern = re.search(r'\b[a-zA-z]{2}\d{4}\b', line)

    start = pattern.span()[0]
    stop = pattern.span()[1]
    subject = line[start:stop]

    return subject

def extractType(types, line):
    re = __import__('re')
        
    idx = -1
    for t in types:
        if (boyerMoore(line, t) != -1):
            idx = boyerMoore(line, t)
            keyword = t
            break

    if(idx != -1):
        return line[idx:idx+len(keyword)]
 

def extractTopic(line):
    return ""





#==================================FUNGSI UPDATE TASK=======================================
def isUpdate(deadline, line):
    re = __import__('re')
    for w in deadline:
        if(boyerMoore(line, w) != -1):
            return True
    return False

def updateDL(taskList, line, id_):
    if (isIDValid(taskList, id_)):
        new_date = extractDate(line)
        taskList[id_-1].date = new_date
        print("Deadline Task " + str(id_) + " berhasil di-update")
    else:
        print("ID tidak valid")

def isIDValid(taskList, id_):
    if (id_>0) and (id_-1 < len(taskList)):
        return True
    return False

def findID(line):
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



#==================================FUNGSI DLFINDER=======================================
def isDLFinder(line):
    if(boyerMoore(line, "Deadline")!=-1 and extractSubject(line)!=None):
        return True
    else:
        return False

def DLFinder(taskList, line):
    subjectkey = extractSubject(line)
    for t in taskList:
        if t.subject == subjectkey:
            return t.date
    return "Deadline tidak ditemukan"




#===================================FUNGSI MARKFINISHED ========================================

def isMarkFinished(line):
    re = __import__('re')
    for w in finishkeywords:
        if(boyerMoore(line, w) != -1):
            return True
    return False

def markFinished(line):
    taskID = findID(line)
    for t in taskList:
        if(t.id == taskID):
            t.status = "Finished"
            return("Status task berhasil diperbaharui")
            break
    return("ID task tidak ditemukan!")





#===================================FUNGSI HELP ========================================
def isHelpMenu(line):
    re = __import__('re')
    for w in helpkeywords:
        if(boyerMoore(line, w) != -1):
            return True
    return False

def helpMenu():
    print("[FITUR]")
    print("1. Menambahkan task baru"+
    "\n2. Melihat daftar task yang harus dikerjakan"+
    "\n3. Menampilkan deadline dari suatu task tertentu"+
    "\n4. Memperbaharui task tertentu"+
    "\n5. Menandai bahwa suatu task sudah selesai dikerjakan\n")

    print("[DAFTAR KEYWORD]")
    print("Tipe task : ", end="")
    for i in range (0, len(types)):
        print(types[i], end="")
        if i != len(types)-1 :
            print(", ", end="")

    print("\nDeadline task : ", end="")
    for i in range (0, len(deadline)):
        print(deadline[i], end="")
        if i != len(deadline)-1 :
            print(", ", end="")
    print("\nSelesai task : ", end="")
    for i in range (0, len(finishkeywords)):
        print(finishkeywords[i], end="")
        if i != len(finishkeywords)-1 :
            print(", ", end="")
    print("\nNeed BoboBot Help ? ", end="")
    for i in range (0, len(helpkeywords)):
        print(helpkeywords[i], end="")
        if i != len(helpkeywords)-1 :
            print(", ", end="")
