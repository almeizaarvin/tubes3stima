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
    elif(isDLFinderBetweenDates(line)):
        return "DLFinderBetweenDates"
    elif(isDLUntilNow(line)):
        return "DLUntilNow"
    elif(isDLFinderBySubject(line)):
        return "DLFinderBySubject"
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

#while(input!=0):
    line = input()
    command = inputIdentify(deadline, types, line)
    if(command == "UpdateDL"):
        idToUpdate = findID(line)
        print(updateDL(taskList, line, idToUpdate))
    elif(command == "Task"):
        T = Task(types, line)
        print(addTask(T))
    elif(command=="DLUntilNow"):
        print(printAllDeadline(line))
    elif(command =="DLFinderBySubject"):
        print(DLFinderBySubject(line))
    elif(command == "DLFinderBetweenDates"):
        print(DLFinderBetweenDates(line))
    elif(command == "DLFinderByWeeks"):
        print(DLFinderByWeeks(line))
    elif(command == "DLFinderByDays"):
        print(DLFinderByDays(line))
    elif(command =="DLToday"):
        print(DLToday(line))
    elif(command =="MarkFinished"):
        print(markFinished(line))
    elif(command == "HelpMenu"):
        print(helpMenu())