from functions import *

#////////////////////////////////
#Global vars
def inputIdentify(deadline, types, line):
    if(isUpdate(deadline, line)):
        return "UpdateDL"
    elif(isTask(types, line)):
        return "Task"
    elif(isDLFinder(line)):
        return "DLFinder"
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
    elif(command =="DLFinder"):
        print(DLFinder(taskList, line))