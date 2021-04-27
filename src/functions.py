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

#============================FUNGSI READFILE WRITEFILE============================
# Membaca masukan dari file txt
def readFile(filename):
    file = open(filename)
    lines = file.read().splitlines()
    return lines

def generateKeywords():
    types = readFile("types.txt")
    deadline = readFile("deadline.txt")
    finishkeywords = readFile("finishkeywords.txt")
    helpkeywords = readFile("helpkeywords.txt")
    months = readFile("months.txt")
    topickeywords = readFile("topickeywords.txt")
    datekeywords = readFile("datekeywords.txt")
    untilnowkeywords = readFile("untilnowkeywords.txt")

generateKeywords()
print(types, deadline, finishkeywords, helpkeywords, months, topickeywords, datekeywords, untilnowkeywords)
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
        self.topic= extractTopic(line)
        self.status="Unfinished"

def isTask(types, line):
    if(extractDate(line)!= None and extractSubject(line)!=None and extractType(line)!=None):
        return True
    else:
        return False

def addTask(Task):
    taskList.append(Task)

def printAllTask():
    for Task in taskList:
        print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)

def printAllDeadline():
    for Task in taskList:
        if Task.status == "Unfinished":
            print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)

def extractDate(line):
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

def extractSubject(line):
    pattern = re.search(r'\b[a-zA-z]{2}\d{4}\b', line)
    if (pattern != None):
        start = pattern.span()[0]
        stop = pattern.span()[1]
        subject = line[start:stop]
        return subject
    return None

def extractType(line):
    idx = -1
    for t in types:
        if (boyerMoore(line, t) != -1):
            idx = boyerMoore(line, t)
            keyword = t
            break

    if(idx != -1):
        return line[idx:idx+len(keyword)]
    return None

def extractTopic(line):
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
            satuan/10
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
            satuan/10
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
    pattern = re.findall(r'\b\d+[/ -]\d+[/ -]\d{4}\b', line)
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
            pattern = re.findall(r'\d+[/ -]'+raw_m+r'[/ -]\d{4}', line)
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
    


#==================================FUNGSI UPDATE TASK=======================================
def isUpdate(deadline, line):
    for w in deadline:
        if(boyerMoore(line, w) != -1):
            return True
    return False

def updateDL(taskList, line, id_):
    if (isIDValid(taskList, id_)):
        if(extractDate(line != None)):
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
    if(boyerMoore(line, "Deadline")!=-1):
        for w in untilnowkeywords:
            if (boyerMoore(line, w) != -1):
                return True
    return False


def isDLFinderBySubject(line):
    if(boyerMoore(line, "Deadline")!=-1 and extractSubject(line)!=None):
        return True
    else:
        return False

def isDLFinderBetweenDates(line):
    dates = extractDate(line)
    if (boyerMoore(line, "Deadline") != -1 and len(dates) == 2):
        return True
    return False

def isDLFinderByWeeks(line):
    if (boyerMoore(line) != 1 and getNweeks(line) != -1):
        return True
    return False
    
def isDLFinderByDays(line):
    if(boyerMoore(line,"Deadline")!= -1 and getNdays(line)!= -1):
        return True
    return False

def isDLToday(line):
    if(boyerMoore(line, "Deadline")!=-1 and boyerMoore(line, "hari")!=-1 and boyerMoore(line, "ini")!=-1):
        return True
    return False    


#########################
# 2. DL EXECUTORS

def DLFinderBySubject(line):
    deadlines=[]
    for t in taskList:
        if t.subject == subjectkey:
            deadlines += [t.date]

    for d in deadlines:
        print(d)

 # 2.b.i Periode DATE_1 sampai DATE_2
def DLFinderBetweenDates(line):
    dates = extractDate(line)
    type_ = extractType(line)
    if(not isBefore(dates[0], dates[1])):
        dates[1], dates[0] = dates[0], dates[1]

    
    for Task in taskList:
        if(isBefore(dates[0],Task.date) and isBefore(Task.date, dates[1])):
            if (type_  != None and type_  == Task.type):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_  == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
                
def DLToday():
    type_ = extractType(line)

    for Task in taskList:
        if(Task.date == getTodayDate()):
            if(type_ != None and type_ == Task.type):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif(type_ == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)


def DLFinderByWeeks(line):
    type_ = extractType(line)
    daysToGo = getNweeks(line) * 7
    boundaryDate = (datetime.now() + timedelta(days=daysToGo)).date().strftime("%d/%m/%Y")
    
    for Task in taskList:
        if(isBefore(Task.date, boundaryDate)):
            if (type_ != None and type_ == Task.type):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_ == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)

def DLFinderByDays(line):
    type_ = extractType(line)
    daysToGo = getNdays(line)
    boundaryDate = (datetime.now() + timedelta(days=daysToGo)).date().strftime("%d/%m/%Y")
    
    for Task in taskList:
        if(isBefore(Task.date, boundaryDate)):
            if (type_ != None and type_ == Task.type):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)
            elif (type_ == None):
                print(str(Task.id)+" - "+Task.date+" - "+Task.subject+" - "+Task.type+" - "+Task.topic+" - "+Task.status)




#===================================FUNGSI MARKFINISHED ========================================

def isMarkFinished(line):
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
    for w in helpkeywords:
        if(boyerMoore(line, w) != -1):
            return True
    return False

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
