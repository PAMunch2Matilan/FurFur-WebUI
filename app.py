from flask import Flask, render_template, request
import requests
from Services.Implant_Generation import Assembly_Gen
from Services.Implant_Generation import Basic_Gen
import Internals
import Utilities

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


# Listener Section
@app.route("/Listener", methods=['GET'])
def listener_page():
    return render_template('Listener.html')


@app.route("/Listener/ShowListener", methods=['POST'])
def show_listener():
    form_data = request.form
    name = form_data.getlist("Name")[0]

    req = requests.request("get", "http://localhost:8000/Listeners/" + name)
    return req.content


@app.route("/Listener/ShowListeners", methods=['POST'])
def show_listeners():
    req = requests.request("get", "http://localhost:8000/Listeners")
    return req.content


@app.route('/Listener/CreateListener/', methods=['POST'])
def create_listener():
    url = "http://localhost:8000/Listeners"

    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"

    if request.method == 'POST':
        form_data = request.form

        name = form_data.getlist("Name")[0]
        port = form_data.getlist("Port")[0]

        data = {'name': name, 'bindPort': port}
        req = requests.post(url, json=data)

        if req.status_code == 201:
            return "<p>Listener Created</>"
        else:
            return "Error during listener creation"


@app.route('/Listener/DeleteListener', methods=['POST'])
def delete_listener():
    form_data = request.form
    name = form_data.getlist("Name")[0]
    url = "http://localhost:8000/Listeners/" + name
    req = requests.delete(url)
    if req.status_code == 204:
        return "<p>Listener " + name + " is deleted</p>"
    else:
        return "<p>Error during removing listener</p>"


# generate
@app.route("/Generate", methods=['GET'])
def generate_page():
    return render_template('Generate.html')


@app.route("/Generate/AssemblyGen", methods=['POST'])
def assembly_gen():
    form_data = request.form
    ip = form_data.getlist("TeamServerIP")[0]
    port = form_data.getlist("ListenerPort")[0]
    return Assembly_Gen.main(ip, port)


@app.route("/Generate/WindowsGen", methods=['POST'])
def windows_gen():
    form_data = request.form
    ip = form_data.getlist("TeamServerIP")[0]
    port = form_data.getlist("ListerPort")[1]

    return Basic_Gen.main("windows", ip, port)


if __name__ == '__main__':
    app.run()
