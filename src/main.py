from functions import *

#////////////////////////////////
def inputIdentify(deadline, types, line):
    if(isUpdate(deadline, line)):
        return "UpdateDL"
    elif(isTask(types, line)):
        return "Task"
    elif(isDLUntilNow(line)):
        return "UntilNow"
    elif(isDLFinderBySubject(line)):
        return "DLFinderBySubject"
    elif(isDLFinderBetweenDates(line)):
        return "DLFinderBetweenDates"
    elif(isDLFinderByWeeks):
        return "DLFinderByWeeks"
    elif(isDLFinderByDays):
        return "DLFinderByDay"
    elif(isDLToday):
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
        printAllDeadline()
    elif(command =="DLFinderBySubject"):
        print(DLFinder(taskList, line))
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