from flask import Flask, render_template, request
from main import *
from functions import *

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get')
def get_bot_response():
    line = request.args.get('msg')
    command = inputIdentify(deadline, types, line)
    botmsg = ""
    if(command == "UpdateDL"):
        idToUpdate = findID(line)
        botmsg += updateDL(line, idToUpdate)
        writeFile(turnToArr(taskList))
    elif(command == "Task"):
        T = Task(types, line)
        botmsg += addTask(T)
        writeFile(turnToArr(taskList))
    elif(command=="DLUntilNow"):
        botmsg += printAllDeadline(line)
    elif(command =="DLFinderBySubject"):
        botmsg += DLFinderBySubject(line)
    elif(command == "DLFinderBetweenDates"):
        botmsg += DLFinderBetweenDates(line)
    elif(command == "DLFinderByWeeks"):
        botmsg += DLFinderByWeeks(line)
    elif(command == "DLFinderByDays"):
        botmsg += DLFinderByDays(line)
    elif(command =="DLToday"):
        botmsg += DLToday(line)
    elif(command =="MarkFinished"):
        botmsg += markFinished(line)
        writeFile(turnToArr(taskList))
    elif(command == "HelpMenu"):
        botmsg += helpMenu()
    else:
        botmsg = "Hah? Gimana? Ngomong apa? Coba ketik 'help' biar tau..."
    return botmsg

@app.route('/contributors/')
def contributors():
    return render_template("contributors.html")
    
if __name__ == "__main__":
    app.run(debug = True) 