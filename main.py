import subprocess
import psutil
import os
import sys
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

Bootstrap5(app)

def is_running(script_name):
    script_name = script_name.lower()

    for proc in psutil.process_iter(['cmdline']):
        try:
            cmd = proc.info['cmdline']
            if not cmd:
                continue

            # Normalize all parts
            normalized = [os.path.basename(part).lower() for part in cmd]

            # Check if script is in the command line
            if script_name in normalized:
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

@app.route('/')
def index():
    return render_template('index.html', active_page="index")

@app.route('/launch_speed_typing_test_gui')
def launch_speed_typing_test_gui():
    if is_running('typespeed.py'):
        print("typespeed GUI already running")
        return render_template('index.html')
    gui_path = os.path.join('gui_tkinter', 'typespeed.py')
    subprocess.Popen([sys.executable, gui_path])
    return render_template('index.html', active_page="index")

if __name__ == '__main__':
    # The reloader will now restart the app without executing
    # global pings twice
    app.run(debug=True)
