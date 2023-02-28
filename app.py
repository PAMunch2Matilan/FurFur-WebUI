import time
import Take_Control
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests, json
from Services.Implant_Generation import Assembly_Gen
from Services.Implant_Generation import Basic_Gen
import Internals
import Utilities

app = Flask(__name__)

result_history = []

@app.route('/Authentification', methods=['POST'])
def authentification():  # put application's code here
    form_data = request.form
    ip = form_data.getlist("ip")[0]
    port = form_data.getlist("port")[0]
    req = requests.get("http://" + ip + ":" + port + "/Listeners")
    print(req)

    if req.status_code == 200:
        return render_template('index.html')
    else:
        return render_template('Authentification.html')

@app.route('/')
def authentification_page():  # put application's code here
    return render_template('Authentification.html')



@app.route('/index')
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

    req = requests.request("get", "http://172.24.192.28:8000/Listeners/" + name)
    return req.content


@app.route("/Listener/ShowListeners", methods=['POST'])
def show_listeners():
    req = requests.request("get", "http://172.24.192.28:8000/Listeners")
    return req.content


@app.route('/Listener/CreateListener/', methods=['POST'])
def create_listener():
    url = "http://172.24.192.28:8000/Listeners"

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
    url = "http://172.24.192.28:8000/Listeners/" + name
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


#Implants

@app.route("/Implant", methods=['GET'])
def implant_page(resultat =""):
    return render_template('Implant.html',resultat=resultat)

@app.route("/Implant/ShowImplant", methods=['POST'])
def show_implant():
     req = requests.request("get", "http://172.24.192.28:8000/Implants")
     return render_template('Implant.html',resultat=req.content)

@app.route("/Implant/ShowImplantByID", methods=['POST'])
def show_implant_by_id():

     form_data = request.form
     name = form_data.getlist("Name")[0]

     req = requests.request("get", "http://172.24.192.28:8000/Implants/" + name)
     return req.content

@app.route("/TakeControl/TakeControl", methods=['POST'])
def take_control():

     #form_data = request.form
#     name = form_data.getlist("id_implant")[0]
     id_implant = request.form['id_implant']
 #    mon_champ = request.form.get('id_implant')
     #return redirect(url_for('page_suivante', mon_param=id_implant))
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



    # #Split les arguments de la commande si il y en a
    # command_split = com.split(" ")
    # print("command_split : " + str(command_split))
    # if len(command_split) == 1 :
    #     print('ici')
    #     data = {'command': command_split[0]}
    # else :
    #     for i in range(0, len(command_split)):
    #         print('i = ' + str(i))
    #         if i == 0:
    #             command = command_split[i]
    #         else:
    #             arg.append(command_split[i])
    #     data = {'command': command, "arguments": arg}
    # # input()



    # print("data :  " + str(data))
    # input()
    hidden_value = request.form['id_implant']
    # headers = {"Content-Type": "application/json", "accept": "*/*"}
    #

    task = Take_Control.take_control_menu(hidden_value,com)
    # print(task)
    # response = requests.post('http://172.24.192.28:8000/Implants/' + hidden_value, json=data, headers=headers)
    # result = json.loads(response.content)
    # task = result["id"]
    print(task)

    response = requests.get('http://172.24.192.28:8000/Implants/' + hidden_value + '/tasks/' + task)
    content = response.text
    print("Content : " + content)
    time.sleep(2)

    # Attendre que la tâche soit terminée et récupérer le résultat
    while response.text == "task not found":

            response = requests.get('http://172.24.192.28:8000/Implants/'+hidden_value + '/tasks/'+ task )
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
    app.run()

