from flask import Flask, render_template
from flask_apscheduler import APScheduler
from updater import get_update
from pickle import load

class Config:
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()

@scheduler.task('cron', id='data_fetch', hour='*')
def scheduled_data_fetch():
    get_update()


app = Flask(__name__)
app.config.from_object(Config())

@app.route("/")
def handle():
    with open("stats/data.pickle", "rb") as fh:
        data = load(fh)
    with open("stats/world.pickle", "rb") as fh:
        world = load(fh)
    with open("stats/up-date.txt", "r") as fh:
        last_updated = fh.read()
    return render_template("home.html", data=data, world=world, last_updated=last_updated)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1,firefox=1'
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

scheduler.init_app(app)
scheduler.start()

if __name__=="__main__":
    app.run(debug=True)
