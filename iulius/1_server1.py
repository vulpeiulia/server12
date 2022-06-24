import time
import flask
import threading
import requests

queue = []
display_list = []
app = flask.Flask(__name__)


# Entrypoint for display
@app.get("/")
def display():
    global queue
    global display_list
    return flask.render_template("server1.html", queue=str(queue), display=str(display_list))

@app.get("/start/")
def start():
    global start_condition
    start_condition = True
    return flask.redirect(flask.url_for("display"))


@app.get("/stop/")
def stop():
    global start_condition
    start_condition = False

    return flask.redirect(flask.url_for("display"))


# Entrypoint for put
@app.put("/api/")
def put_func():
    global display_list
    display_list.insert(0, flask.request.json)
    if display_list.__len__() > 10:
        display_list.pop()
    return flask.jsonify({"status": "success"})

def generator_func():
    global queue
    global counter
    while True:
        while start_condition:
            queue.insert(0, f"{counter}")
            counter += 1
            time.sleep(1)
        time.sleep(3)

def queue_extractor():
    global queue
    # Extract the last entry from the queue and send it via a post
    while True:
        if len(queue) > 0:
            last_entry = queue.pop()
            requests.post("http://localhost:5001/api/", json=last_entry)
            print('abyrwalg')
            time.sleep(1)
        else:
            print('TryAgain')
            time.sleep(1)



counter = 0
start_condition = False
extractors = [threading.Thread(target=queue_extractor) for i in range(8)]
generators = [threading.Thread(target=generator_func) for i in range(2)]

if __name__ == '__main__':
    for thread in extractors:
        thread.start()
    for thread in generators:
        thread.start()
    app.run(host='127.0.0.1', port=5000)
