from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

Bootstrap5(app)

@app.route('/')
def index():
    return render_template('index.html', active_page="index")


# if __name__ == '__main__':
#     # The reloader will now restart the app without executing
#     # global pings twice
#     app.run(debug=True)
