from functions import *


types, deadline, finishkeywords, helpkeywords, months, topickeywords, datekeywords, untilnowkeywords = generateKeywords(types, deadline, finishkeywords, 
                                                                                                            helpkeywords, months, topickeywords, datekeywords, untilnowkeywords)

taskList = makeTaskList(readFile("taskList.txt"))

#////////////////////////////////
def inputIdentify(deadline, types, line):
    if(isUpdate(deadline, line)):
        return "UpdateDL"
    elif(isTask(types, line)):
        return "Task"
    elif(isDLUntilNow(line)):
        return "DLUntilNow"
    elif(isDLFinderBySubject(line)):
        return "DLFinderBySubject"
    elif(isDLFinderBetweenDates(line)):
        return "DLFinderBetweenDates"
    elif(isDLFinderByWeeks(line)):
        return "DLFinderByWeeks"
    elif(isDLFinderByDays(line)):
        return "DLFinderByDays"
    elif(isDLToday(line)):
        return "DLToday"    
    elif(isMarkFinished(line)):
        return "MarkFinished"
    elif(isHelpMenu(line)):
        return "HelpMenu"
    else:
        print("Maaf, pesan tidak dikenali")

#/////////////////////////////

while(input!=0):
    line = input()
    command = inputIdentify(deadline, types, line)
    if(command == "UpdateDL"):
        idToUpdate = findID(line)
        updateDL(taskList, line, idToUpdate)
    elif(command == "Task"):
        T = Task(types, line)
        addTask(T)
        printAllTask()
    elif(command=="DLUntilNow"):
        printAllDeadline(line)
    elif(command =="DLFinderBySubject"):
        DLFinderBySubject(line)
    elif(command == "DLFinderBetweenDates"):
        DLFinderBetweenDates(line)
    elif(command == "DLFinderByWeeks"):
        DLFinderByWeeks(line)
    elif(command == "DLFinderByDays"):
        DLFinderByDays(line)
    elif(command =="DLToday"):
        DLToday(line)
    elif(command =="MarkFinished"):
        print(markFinished(line))
    elif(command == "HelpMenu"):
        helpMenu()