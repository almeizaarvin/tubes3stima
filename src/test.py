import re
from functions import *
import datetime

texttosearch = '''
22/3/2020
aodshfoiawdsf
21/02/2020
31/2/2021
'''

texttosearch2 = '''
30-Mei-2021
aodshfoiawdsf
2 April 2021
'''
texttosearch3 = '''
30-5-2021
aodshfoiawdsf
2-6-2021
'''

texttosearch3 = '''
30 5 2021
aodshfoiawdsf
2 6 2021
'''

months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
topickeywords = ["Topik", "Tentang", "BAB"]
datekeywords = ["Pada", "Tanggal"]

from datetime import date
today = date.today()
today = today.strftime("%d/%m/%Y")

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

def extractDate(line):
    pattern = extractDateFormat1(line)
    if(len(pattern) == 0):
        pattern = extractDateFormat2(line)
    if(len(pattern) > 0):
        for p in pattern:
            if (not isDateValid(p)):
                print("Tanggal tidak valid")
                return
    return pattern 


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
        datetime.datetime(int(year),int(month),int(day))
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

def writeFile(tasklist):
    f1=open('../test/taskList.txt', 'w')
    for task in tasklist:
        f1.write(task + "\n")

#text = "tubes IF2002 BAB 1 sampai 2 29/04/2021"
#date = extractDate(texttosearch3)
#date = extractDate(text)
#print(date)
#print(extractTopic(text))
""" print(changeFormatDate2(date[1]))
print(isDateValid(changeFormatDate2(date[1])))
print('29/02/2021')
print(isDateValid('29/02/2021')) """


task = ["1-10/05/2021-IF2222-Tubes-Bab 2-Unfinished" , "3-03/05/2021-IF5050-PR-abc-Unfinished"]

writeFile(task)

def makeTaskList(task):
    taskList = []
    for line in lines:
        pattern = re.findall(r'-\w-', line)
        topic = pattern[3]
        T = Task(types,task + " "+ topic)
        pattern = re.findall(r'-\w', line)
        T.status = pattern[len(pattern-1)]
        taskList.append(T)
    return taskList