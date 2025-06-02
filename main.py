from flask import Flask, render_template
import subprocess
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/start_wordle')
def start_wordle():
    subprocess.Popen(["python", "pygame_wordle.py"])
    return "Wordle стартира!"

@app.route('/start_aviator')
def start_aviator():
    subprocess.Popen(["python", "pygame_aviator.py"])
    return "Aviator стартира!"

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()  # Отваря браузъра автоматично
    app.run(debug=False)
