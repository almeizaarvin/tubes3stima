from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    return userText

@app.route('/contributors/')
def contributors():
    return render_template("contributors.html")
    
if __name__ == "__main__":
    app.run(debug = True) 