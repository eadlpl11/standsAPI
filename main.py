import requests
import os
import json
from flask import Flask, redirect, url_for, render_template, request, flash

from requests import get

""" Funciones core del codigo """

def clear(): os.system('clear')
clear()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

""" GET """
@app.route("/characters",methods=["POST","GET"])
def get_all():
    try:
        stand = get("https://standapi.herokuapp.com/api/stands/").json()
        length = len(stand["all_stands"])
        print(length)
        return render_template("all.html", stand = stand, length=length )
    except:
        return render_template('fallo.html')

@app.route("/characters/<name>")
def get_name(name):
    try:
        stand = get("https://standapi.herokuapp.com/api/stands/").json()
        length = len(stand["all_stands"])

        for x in range(length):
            if stand["all_stands"][x]["name"] == name:
                print(stand["all_stands"][x]["name"])
                print(x)
                return render_template('individual.html',stand = stand, x = x)

        return render_template('notfound.html')
    except:
        return render_template('fallo.html')

@app.route("/characters/search",methods=["POST","GET"])
def search_name():
    if request.method == "POST":
        
        tarot_number = request.form["tarot_number"]

        
        print(tarot_number)

        stand = get("https://standapi.herokuapp.com/api/stands/").json()
        length = len(stand["all_stands"])
        
        
        for x in range(length):
            
            if stand["all_stands"][x]["tarot_number"] == tarot_number:
                print(stand["all_stands"][x]["tarot_number"])
                name = stand["all_stands"][x]["name"]
                url = '/characters/'+name
                return redirect(url)
    
    return render_template('obtener.html')

""" POST """
@app.route("/new",methods=["POST","GET"])
def add():
    try:
        if request.method == "POST":
            """ Jala los datos de la forma """
            nombre = request.form["nombre"]
            referencia = request.form["reference"]
            numero_tarot = request.form["tarot_number"]
            nombre_usuario = request.form["user_name"]
            llave = request.form["token"]
            imagen = request.form["img"]

            diccionarillo = {
                'img': imagen,
                'name': nombre,
                'reference': referencia,
                'tarot_number': numero_tarot,
                'user_name': nombre_usuario
                }

            if '' in diccionarillo.values():
                return render_template("crear.html")

            url = 'https://standapi.herokuapp.com/api/new_stand/'+llave

            respuesta = requests.post(url,json=diccionarillo)
            respuesta = respuesta.json()

            if respuesta['status'] == 200:
                return render_template('exito.html')
            else:
                return render_template('fallo.html')
        else:
            return render_template("crear.html")
    except:
        return render_template('fallo.html')


""" PUT """
@app.route('/update',methods=["PUT","GET","POST"])
def update():
    try:
        if request.method == "POST":
            """ Jala los datos de la forma """

            actualizar = request.form["tarot_number"]

            nombre = request.form["nombre"]
            referencia = request.form["reference"]
            numero_tarot = request.form["tarot_number2"]
            nombre_usuario = request.form["user_name"]
            llave = request.form["token"]
            imagen = request.form["img"]

            diccionarillo = {
                'img': imagen,
                'name': nombre,
                'reference': referencia,
                'tarot_number': numero_tarot,
                'user_name': nombre_usuario
            }

            url = 'https://standapi.herokuapp.com/api/stand/update/'+llave+'/'+actualizar+'/'

            if '' in diccionarillo.values() or actualizar == '':
                return render_template("actualizar.html")

            respuesta = requests.put(url,json = diccionarillo)
            respuesta = respuesta.json()

            print(diccionarillo)
            print(url)

            if respuesta['status'] == 200:
                return render_template('exito.html')
            else:
                return render_template('notfound.html')
        else:
            return render_template("actualizar.html")
    except:
        return render_template('fallo.html')

""" DELETE """
@app.route('/delete',methods=["DELETE","GET","POST"])
def delete():
    try:
        if request.method == "POST":
            """ Jala los datos de la forma """
            numero_tarot = request.form["tarot_number"]
            llave = request.form["token"]

            url = 'https://standapi.herokuapp.com/api/stand/del/'+llave+'/'+numero_tarot+'/'

            if numero_tarot == '' or llave == '': 
                return render_template('eliminar.html')

            respuesta = requests.delete(url)
            respuesta = respuesta.json()

            print("cosas "+numero_tarot+llave)
            print(url)

            if respuesta['status'] == 200:
                return render_template('exito.html')
            else:
                return render_template('notfound.html')
        else:
            return render_template("eliminar.html")
    except:
        return render_template('fallo.html')


@app.route("/test",methods=["POST","GET"])
def test():
    return 'test'

if __name__ == "__main__":
    app.run(debug=True)