from flask import Flask, render_template, request
import sys
from io import StringIO
from pitscript import start

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    code = ""
    if request.method == 'POST':
        code = request.form['code']
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        mystdout = sys.stdout
        try:
            start(code)
        except Exception as e:
            print("Error: ", e)
        sys.stdout = old_stdout
        output = mystdout.getvalue()
    return render_template('index.html', code=code, output=output)
