from flask import Flask, render_template
import subprocess

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

if __name__ == "__main__":
    app.run(debug=True)
