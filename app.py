from flask import Flask, request, jsonify

app = Flask(__name__) #Esto nos permite crear una aplicación Flask

partidos = [] #Lista para almacenar los partidos en memoria

contador_partido = 1 #Contador para asignar IDs únicos a cada partido creado

@app.route("/partidos", methods=["POST"]) #Endpoint para crear un nuevo partido
def crear_partido():
    global contador_partido

    data = request.get_json() #Datos enviados por el usuario

    nuevo = { #Crea el nuevo partido con los datos recibidos y un ID único
        "id": contador_partido,
        "equipo_local": data.get("equipo_local"),
        "equipo_visitante": data.get("equipo_visitante"),
        "fecha": data.get("fecha"),
        "fase": data.get("fase"),
        "resultado": None 
    }

    partidos.append(nuevo) #Guardo el partido en la lista

    contador_partido += 1

    return jsonify(nuevo), 201 #Devuelve el partido creado con el código de estado 201 (creado)


@app.route('/partidos', methods=['GET']) #Endpoint para listar los partidos
def listar_partidos():
    return jsonify(partidos), 200

@app.route("/partidos/<int:id>", methods=["GET"]) #Endpoint para obtener un partido específico
def obtener_partido(id):
    for p in partidos:
        if p["id"] == id:
            return jsonify(p), 200
    return {"Error": "Partido no encontrado"}, 404

@app.route("/partidos/<int:id>", methods=["DELETE"]) #Endpoint para eliminar un partido
def eliminar_partido(id):
    global partidos

    for p in partidos:
        if p["id"] == id:
            partidos.remove(p)
            return {"Mensaje": "Partido eliminado"}, 200
    return {"Error": "Partido no encontrado"}, 404

@app.route("/partidos/<int:id>", methods=["PUT"]) #Endpoint para actualizar un partido completo
def actualizar_partido(id):
    for p in partidos:
        if p["id"] == id:
            data = request.get_json()

            p["equipo_local"] = data.get("equipo_local")
            p["equipo_visitante"] = data.get("equipo_visitante")
            p["fecha"] = data.get("fecha")
            p["fase"] = data.get("fase")

            return jsonify(p), 200
        
    return {"Error": "Partido no encontrado"}, 404

@app.route("/partidos/<int:id>/resultado", methods=["PUT"]) #Endpoint para actualizar solo el resultado de un partido
def actualizar_resultado(id):
    data = request.get_json()

    for p in partidos:
        if p["id"] == id:
            p["resultado"] = {
                "goles_local": data.get("goles_local"),
                "goles_visitante": data.get("goles_visitante")
            }
            return jsonify(p), 200
        
    return {"Error": "Partido no encontrado"}, 404

if __name__ == "__main__":
    app.run(debug=True)