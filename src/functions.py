import re
from datetime import *

global types
types = []

global taskList
taskList = []

global deadline
deadline = []

global finishkeywords
finishkeywords = []

global helpkeywords
helpkeywords = []

global months
months = []

global topickeywords
topickeywords = []

global datekeywords
datekeywords = []

global untilnowkeywords
untilnowkeywords = []

#============================FUNGSI READFILE DAN GENERATE KEYWORDS============================
# Membaca masukan dari file txt
def readFile(filename):
    filename='../test/'+filename
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def generateKeywords(types, deadline, finishkeywords, helpkeywords, months, topickeywords, datekeywords, untilnowkeywords):
    try:
        types = readFile('types.txt')
        deadline = readFile("deadline.txt")
        finishkeywords = readFile("finishkeywords.txt")
        helpkeywords = readFile("helpkeywords.txt")
        months = readFile("months.txt")
        topickeywords = readFile("topickeywords.txt")
        datekeywords = readFile("datekeywords.txt")
        untilnowkeywords = readFile("untilnowkeywords.txt")
        return types, deadline, finishkeywords, helpkeywords, months, topickeywords, datekeywords, untilnowkeywords
    except:
        types = []
        deadline = []
        finishkeywords = []
        helpkeywords = []
        months = []
        topickeywords = []
        datekeywords = []
        untilnowkeywords = []
        return types, deadline, finishkeywords, helpkeywords, months, topickeywords, datekeywords, untilnowkeywords

types, deadline, finishkeywords, helpkeywords, months, topickeywords, datekeywords, untilnowkeywords = generateKeywords(types, deadline, finishkeywords, 
                                                                                                            helpkeywords, months, topickeywords, datekeywords, untilnowkeywords)



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
        self.date= extractDate(line)[0]
        self.subject= extractSubject(line)
        self.type= extractType(line)
        if (extractTopic(line) != ""):
            self.topic= extractTopic(line).capitalize()
        else:
            self.topic="[Tidak spesifik]"
        self.status="Unfinished"

def isTask(types, line):
    try:
        if(extractDate(line)!= None and extractSubject(line)!=None and extractType(line)!=None):
            return True
        else:
            return False
    except:
        pass

def addTask(Task):
    if(not isTaskinTasklist(Task)):
        taskList.append(Task)
    else:
        print("Task sudah tercatat!")

def isTaskinTasklist(Task):
    for t in taskList:
        if (t.date == Task.date and t.subject == Task.subject and t.type == Task.type and t.topic == Task.topic):
            return True
    return False

def printAllTask():
    today_date = getTodayDate()
    empty = True
    for Task in taskList:
        if isBefore(today_date, Task.date):
            empty = False
            print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
    if(empty):
        print("Kamu tidak memiliki deadline task apapun!")

def printAllDeadline(line):
    type_ = extractType(line)
    today_date = getTodayDate()
    empty = True
    for Task in taskList:
        if Task.status == "Unfinished" and isBefore(today_date, Task.date):
            if (type_ != None and type_.lower() == Task.type.lower()):
                empty = False
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_ == None):
                empty = False
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
    if(empty):
        print("Kamu tidak memiliki deadline task yang belum selesai!")    

def extractDate(line):
    try:
        pattern = extractDateFormat1(line)
        if(len(pattern) == 0):
            pattern = extractDateFormat2(line)
        if (len(pattern) == 0):
            return
        if(len(pattern) > 0):
            for p in pattern:
                if (not isDateValid(p)):
                    print("Tanggal tidak valid")
                    return
            return pattern
    except:
        return None

def extractSubject(line):
    pattern = re.search(r'\b[a-zA-z]{2}\d{4}\b', line)
    if (pattern != None):
        start = pattern.span()[0]
        stop = pattern.span()[1]
        subject = line[start:stop]
        return subject
    return None

def extractType(line):
    for t in types:
        t_raw = r"{}".format(t)
        pattern = re.search(r'\b'+t_raw+r'\b', line, re.IGNORECASE)
        if (pattern != None):
            Startidx = pattern.span()[0]
            Stopidx = pattern.span()[1]
            return t
    return None

def extractTopic(line):
    try:
        found = False
        for w in topickeywords:
            if (boyerMoore(line, w) != -1):
                idx = boyerMoore(line, w)
                keyword = w
                startTopic = idx
                if (w != "BAB"):
                    startTopic = idx+len(w)+1
                break
        for w in datekeywords:
            if (boyerMoore(line, w) != -1):
                idx = boyerMoore(line, w)
                keyword = w
                stopTopic = idx
                found = True
                break
        if(not found):
            stopTopic = searchIdxDate(line)

        topic = line[startTopic:stopTopic-1]
        return topic
    except:
        return ""


#============================FUNGSI INISIASI DAN SIMPAN TASKLIST============================

def makeTaskList(lines):
    taskList = []
    for line in lines:
        pattern = re.split(r'[-]', line)
        topic = pattern[4]
        T = Task(types,line + " tentang "+ topic)
        T.status = pattern[5]
        T.id = int(pattern[0])
        T.topic = topic.capitalize()
        taskList.append(T)
    return taskList

def turnToArr(taskList):
    arr_task = []
    for Task in taskList:
        t = str(Task.id)+"-"+Task.date+"-"+Task.subject+"-"+Task.type+"-"+Task.topic+"-"+Task.status
        arr_task.append(t)
    return arr_task

def writeFile(arr_tasklist):
    f1=open('../test/taskList.txt', 'w')
    for task in arr_tasklist:
        f1.write(task + "\n")

#=================================FUNGSI-FUNGSI DATE==================================
#1. Getter

def getTodayDate():
    return datetime.now().date().strftime("%d/%m/%Y")

def getDay(date):
    day,month,year = date.split('/')
    return day

def getMonth(date):
    day,month,year = date.split('/')
    return month

def getYear(date):
    day,month,year = date.split('/')
    return year


def getNweeks(line):
    pattern = re.search("\d+ minggu", line, re.IGNORECASE)
    if(pattern==None):
        return -1
    else:
        start = pattern.span()[0]
        stop = pattern.span()[1]
        string = line[start:stop]

        angka = re.findall("\d", string)
        n = 0
        satuan = 10**(len(angka)-1)
        for i in range (len(angka)):
            n += int(angka[i])*satuan
            satuan//10
        return n

def getNdays(line):
    pattern = re.search("\d+ hari", line, re.IGNORECASE)
    if(pattern==None):
        return -1
    else:
        start = pattern.span()[0]
        stop = pattern.span()[1]
        string = line[start:stop]

        angka = re.findall("\d", string)
        n = 0
        satuan = 10**(len(angka)-1)
        for i in range (len(angka)):
            n += int(angka[i])*satuan
            satuan//10
        return n

    
#############
#2. Date operations

def isBefore(date1, date2):
    d1, m1, y1 = [int(x) for x in date1.split('/')]
    d2, m2, y2 = [int(x) for x in date2.split('/')]

    if date(y1, m1, d1) < date(y2, m2, d2):
        return True
    else:
        return False
  



#############
#3. Date format converter 

def extractDateFormat1(line):
    listofDate = []
    pattern = re.findall(r'\d+[/ -]\d+[/ -]\d{4}', line)
    for p in pattern:
        p = p.replace('-','/')
        p = p.replace(' ','/')
        p = changeFormatDate1(p)
        listofDate.append(p)
    return listofDate

def extractDateFormat2(line):
    listofDate = []
    for m in months:
        if (boyerMoore(line, m) != -1):
            raw_m = r"{}".format(m)
            pattern = re.findall(r'\d+[/ -]'+raw_m+r'[/ -]\d{4}', line, re.IGNORECASE)
            for p in pattern:
                p = changeFormatDate2(p)
                listofDate.append(p)
    return listofDate

def getMonthIdx(date):
    #mengembalikan nama bulan sebagai angka
    for i in range(12):
        pattern = re.findall(months[i], date, re.IGNORECASE)
        if (len(pattern) == 1):
            month = str(i+1)
            month = makeTwoDigits(month)
            return month

def changeFormatDate1(or_date):
    #get day,month,year
    day,month,year = or_date.split('/')
    month = makeTwoDigits(month)
    day = makeTwoDigits(day)
    #formating
    formatted_date = day+'/'+month+'/'+year
    return formatted_date

def makeTwoDigits(char_int):
    #formating angka biar dua digit
    if (int(char_int) < 10 and char_int[0] != '0'):
        number = '0'+char_int
    else:
        number = char_int
    return number

def changeFormatDate2(or_date):
    #get year
    year = or_date[-4:]
    #get month
    month = getMonthIdx(or_date)
    #get date
    day_raw = re.findall(r'\d+', or_date[0:2])
    date = makeTwoDigits(day_raw[0])
    #formating
    formatted_date = date+'/'+month+'/'+year
    return formatted_date

def isDateValid(date):
    isValid = True
    day,month,year = date.split('/')
    try :
        datetime(int(year),int(month),int(day))
    except ValueError :
        isValid = False
    return isValid

def searchIdxDate(line):
    pattern = re.search(r'\b\d+[/ -]\d+[/ -]\d{4}\b', line)
    if (pattern == None):
        for m in months:
            if (boyerMoore(line, m) != -1):
                raw_m = r"{}".format(m)
                pattern = re.search(r'\d+[/ -]'+raw_m+r'[/ -]\d{4}', line)
    return pattern.span()[0]


#==================================INISIASI TASKLIST =======================================
taskList = makeTaskList(readFile("taskList.txt"))

#==================================FUNGSI UPDATE TASK=======================================
def isUpdate(deadline, line):
    try:
        for w in deadline:
            if(boyerMoore(line, w) != -1):
                return True
        return False
    except:
        pass

def updateDL(taskList, line, id_):
    if (isIDValid(taskList, id_)):
        if(extractDate(line) != None):
            new_date = extractDate(line)[0]
            taskList[id_-1].date = new_date
            print("Deadline Task " + str(id_) + " berhasil di-update")
    else:
        print("ID tidak valid")

def isIDValid(taskList, id_):
    if (id_>0) and (id_-1 < len(taskList)):
        return True
    return False

def findID(line):
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
#1.  DLFINDER VALIDATORS
def isDLUntilNow(line):
    try:
        if(boyerMoore(line, "Deadline")!=-1):
            for w in untilnowkeywords:
                if (boyerMoore(line, w) != -1):
                    return True
        return False
    except:
        pass


def isDLFinderBySubject(line):
    try:
        if(boyerMoore(line, "Deadline")!=-1 and extractSubject(line)!=None):
            return True
        else:
            return False
    except:
        pass

def isDLFinderBetweenDates(line):
    try:
        dates = extractDate(line)
        if (boyerMoore(line, "Deadline") != -1 and len(dates) == 2):
            return True
        return False
    except:
        pass

def isDLFinderByWeeks(line):
    try:
        if (boyerMoore(line, "Deadline") != 1 and getNweeks(line) != -1):
            return True
        return False
    except:
        pass
    
def isDLFinderByDays(line):
    try:
        if(boyerMoore(line,"Deadline")!= -1 and getNdays(line)!= -1):
            return True
        return False
    except:
        pass

def isDLToday(line):
    try:
        if(boyerMoore(line, "Deadline")!=-1 and boyerMoore(line, "hari")!=-1 and boyerMoore(line, "ini")!=-1):
            return True
        return False   
    except:
        pass 


#########################
# 2. DL EXECUTORS

def DLFinderBySubject(line):
    subjectkey = extractSubject(line)
    typekey = extractType(line)
    deadline_subject=[]
    today_date = getTodayDate()
    empty = True
    for t in taskList:
        if (typekey != None):
            if t.subject.lower() == subjectkey.lower() and type_.lower() == t.type.lower() and isBefore(today_date, t.date):
                empty = False
                deadline_subject.append(t)
        else:
            if t.subject.lower() == subjectkey.lower() and isBefore(today_date, t.date):
                empty = False
                deadline_subject.append(t)
    if(not empty):
        for d in deadline_subject:
            print(str(d.id)+" - "+d.date+" - "+d.status)
    else:
        print("Kamu tidak memiliki deadline task!")

 # 2.b.i Periode DATE_1 sampai DATE_2
def DLFinderBetweenDates(line):
    dates = extractDate(line)
    type_ = extractType(line)
    empty = True
    if(not isBefore(dates[0], dates[1])):
        dates[1], dates[0] = dates[0], dates[1]

    for Task in taskList:
        if(isBefore(dates[0],Task.date) and isBefore(Task.date, dates[1])):
            empty = False
            if (type_  != None and type_  == type_.lower() == Task.type.lower()):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_  == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
    if(empty):
        print("Kamu tidak memiliki deadline task!")
                
def DLToday(line):
    type_ = extractType(line)
    empty = True
    for Task in taskList:
        if(Task.date == getTodayDate()):
            empty = False
            if(type_ != None and type_ == type_.lower() == Task.type.lower()):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif(type_ == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
    if(empty):
        print("Kamu tidak memiliki deadline task!")


def DLFinderByWeeks(line):
    type_ = extractType(line)
    daysToGo = getNweeks(line) * 7 + 1
    boundaryDate = (datetime.now() + timedelta(days=daysToGo)).date().strftime("%d/%m/%Y")
    today_date = getTodayDate()
    empty = True
    for Task in taskList:
        if(isBefore(Task.date, boundaryDate) and isBefore(today_date, Task.date)):
            empty = False
            if (type_ != None and type_.lower() == Task.type.lower()):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_ == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
    if(empty):
        print("Kamu tidak memiliki deadline task!")

def DLFinderByDays(line):
    type_ = extractType(line)
    daysToGo = getNdays(line) + 1
    boundaryDate = (datetime.now() + timedelta(days=daysToGo)).date().strftime("%d/%m/%Y")
    today_date = getTodayDate()
    empty = True
    for Task in taskList:
        if(isBefore(Task.date, boundaryDate) and isBefore(today_date, Task.date)):
            empty = False
            if (type_ != None and type_.lower() == Task.type.lower()):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_ == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
    if(empty):
        print("Kamu tidak memiliki deadline task!")


#===================================FUNGSI MARKFINISHED ========================================

def isMarkFinished(line):
    try:
        for w in finishkeywords:
            if(boyerMoore(line, w) != -1):
                return True
        return False
    except:
        pass

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
    try:
        for w in helpkeywords:
            if(boyerMoore(line, w) != -1):
                return True
        return False
    except:
        pass

def helpMenu():
    print("\n[FITUR]")
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
            
    print()
    print()
