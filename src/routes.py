from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bt')
def bt():
    return render_template('bt.html')

@app.route('/dist')
def dist():
    return render_template('dist.html')

@app.errorhandler(404)
def page_not_found(request, exception=None):
    return render_template(request, '404.html')